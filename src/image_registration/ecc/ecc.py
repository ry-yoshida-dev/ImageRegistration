from __future__ import annotations

import cv2
import numpy as np
from dataclasses import dataclass, field
from typing import cast

from projective import PerspectiveMatrix, register_perspective_matrix

from ..types.array import UInt8Image, UInt8Mask
from .parameter import ECCParameters
from .result import ECCResult

_EMPTY_ECC_MASK: UInt8Mask = np.empty((0, 0), dtype=np.uint8)


@dataclass
class ECCProcessor:
    """
    Enhanced Correlation Coefficient (ECC) image registration processor.

    Attributes
    ----------
    params : ECCParameters
        Parameters for the ECC algorithm.
    criteria : tuple[int, int, float]
        Termination criteria for the ECC algorithm.
    """

    params: ECCParameters
    criteria: tuple[int, int, float] = field(init=False)

    def __post_init__(self) -> None:
        self.criteria = self.params.define_criteria()

    def run(
        self,
        source_image: UInt8Image,
        target_image: UInt8Image,
        previous_motion_matrix: PerspectiveMatrix | None = None,
        mask: UInt8Mask | None = None,
    ) -> tuple[PerspectiveMatrix, ECCResult]:
        """
        Run ECC registration between two frames.

        Parameters
        ----------
        source_image : UInt8Image
            Source frame used as the ECC template.
        target_image : UInt8Image
            Target frame to align with the source frame.
        previous_motion_matrix : PerspectiveMatrix | None
            Optional initial motion matrix in original image coordinates.
        mask : UInt8Mask | None
            Optional mask restricting the registration region.

        Returns
        -------
        tuple[PerspectiveMatrix, ECCResult]
            Motion matrix in original image coordinates and ECC optimization
            details. Returns an identity matrix when ECC fails to converge.
        """
        try:
            motion_matrix, correlation_coefficient = self._find_motion_matrix(
                source_image=self._rescale_image(source_image),
                target_image=self._rescale_image(target_image),
                warp_matrix=self._resolve_warp_matrix(previous_motion_matrix),
                mask=self._rescale_mask(mask),
            )
            matrix = register_perspective_matrix(
                matrix=motion_matrix,
                transform_type=self.params.transform_type,
            )
            if self.params.scale_factor != 1.0:
                matrix = matrix.scale_correction(scale=self.params.scale_factor)
            ecc_result = ECCResult(
                correlation_coefficient=correlation_coefficient,
                is_converged=True,
            )
            return matrix, ecc_result
        except cv2.error as error:
            message = str(error)
            if "Iterations do not converge" in message:
                identity_matrix = register_perspective_matrix(
                    matrix=None,
                    transform_type=self.params.transform_type,
                )
                ecc_result = ECCResult(
                    correlation_coefficient=0.0,
                    is_converged=False,
                )
                return identity_matrix, ecc_result
            raise ValueError(f"ECC algorithm failed: {message}") from error

    def _rescale_image(self, image: UInt8Image) -> UInt8Image:
        """
        Resize an image according to ``params.scale_factor``.

        Parameters
        ----------
        image : UInt8Image
            Input grayscale image.

        Returns
        -------
        UInt8Image
            Resized image. Returns ``image`` unchanged when ``scale_factor == 1.0``.
        """
        if self.params.scale_factor == 1.0:
            return image

        height = cast(int, image.shape[0])
        width = cast(int, image.shape[1])
        new_width = int(width * self.params.scale_factor)
        new_height = int(height * self.params.scale_factor)
        if new_width <= 0 or new_height <= 0:
            raise ValueError(
                "scale_factor="
                + f"{self.params.scale_factor} produces invalid size "
                + f"({new_height}, {new_width}) from input shape {image.shape}"
            )
        return cast(
            UInt8Image,
            cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR),
        )

    def _rescale_mask(self, mask: UInt8Mask | None) -> UInt8Mask | None:
        """
        Resize a mask according to ``params.scale_factor``.

        Parameters
        ----------
        mask : UInt8Mask | None
            Boolean or numeric mask aligned with the input image.

        Returns
        -------
        UInt8Mask | None
            Resized mask. Returns ``mask`` unchanged when it is None or
            ``scale_factor == 1.0``.
        """
        if mask is None or self.params.scale_factor == 1.0:
            return mask

        if mask.ndim != 2:
            raise ValueError(f"mask must be a 2D array, got shape {mask.shape}")

        height = cast(int, mask.shape[0])
        width = cast(int, mask.shape[1])
        new_width = int(width * self.params.scale_factor)
        new_height = int(height * self.params.scale_factor)
        if new_width <= 0 or new_height <= 0:
            raise ValueError(
                "scale_factor="
                + f"{self.params.scale_factor} produces invalid mask size "
                + f"({new_height}, {new_width}) from input shape {mask.shape}"
            )
        return cast(
            UInt8Mask,
            cv2.resize(mask, (new_width, new_height), interpolation=cv2.INTER_NEAREST),
        )

    def _resolve_warp_matrix(
        self,
        previous_motion_matrix: PerspectiveMatrix | None,
    ) -> np.ndarray:
        """
        Resolve the warp matrix for the ECC algorithm.

        Returns
        -------
        np.ndarray
            Warp matrix in ECC working image coordinates.
        """
        if previous_motion_matrix is None:
            return register_perspective_matrix(
                matrix=None,
                transform_type=self.params.transform_type,
            ).value

        if self.params.scale_factor == 1.0:
            return previous_motion_matrix.value

        return previous_motion_matrix.scale_correction(
            scale=1.0 / self.params.scale_factor,
        ).value

    def _find_motion_matrix(
        self,
        source_image: UInt8Image,
        target_image: UInt8Image,
        warp_matrix: np.ndarray,
        mask: UInt8Mask | None,
    ) -> tuple[np.ndarray, float]:
        """
        Find the motion matrix for the ECC algorithm.

        Parameters
        ----------
        source_image : UInt8Image
            Source image for ECC in working coordinates.
        target_image : UInt8Image
            Target image for ECC in working coordinates.
        warp_matrix : np.ndarray
            Initial warp matrix updated in place by OpenCV.
        mask : UInt8Mask | None
            Optional registration mask in working coordinates.

        Returns
        -------
        tuple[np.ndarray, float]
            Updated warp matrix after ECC optimization and the final correlation
            coefficient.

        NOTE
        --------
        ``warp_matrix`` is updated in place by OpenCV function ``cv2.findTransformECC``.
        """
        input_mask = _EMPTY_ECC_MASK if mask is None else mask
        warp_matrix_f32 = np.asarray(warp_matrix, dtype=np.float32)
        correlation_coefficient, _ = cv2.findTransformECC(
            source_image,
            target_image,
            warp_matrix_f32,
            self.params.cv2_motion_type,
            self.criteria,
            input_mask,
            self.params.gaussFiltSize,
        )
        return warp_matrix_f32.copy(), float(correlation_coefficient)
