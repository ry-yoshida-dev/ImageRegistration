from __future__ import annotations

import cv2
from dataclasses import dataclass
from functools import cached_property
from projective import PerspectiveTransformationMethod


@dataclass
class ECCParameters:
    """
    Parameters for the Enhanced Correlation Coefficient (ECC) image registration.

    Attributes
    ----------
    transform_type : PerspectiveTransformationMethod
        Type of transformation to apply.
    scale_factor : float
        Image scale multiplier applied before ECC computation.
    eps : float
        Termination epsilon for the ECC algorithm.
    max_iter : int
        Maximum number of iterations for the ECC algorithm.
    gaussFiltSize : int
        Gaussian filter size for the ECC algorithm.
    """

    transform_type: PerspectiveTransformationMethod = PerspectiveTransformationMethod.AFFINE
    scale_factor: float = 1.0
    eps: float = 1e-5
    max_iter: int = 100
    gaussFiltSize: int = 1

    def __post_init__(self) -> None:
        if self.scale_factor <= 0:
            raise ValueError("scale_factor must be a positive number")

    @cached_property
    def inverse_scale_factor(self) -> float:
        """
        Multiplier that maps scaled coordinates back to the original image.

        Returns
        -------
        float
            ``1.0 / scale_factor`` when scaling is enabled, otherwise ``1.0``.
        """
        if self.scale_factor == 1.0:
            return 1.0
        return 1.0 / self.scale_factor

    def define_criteria(self) -> tuple[int, int, float]:
        """
        Define the criteria for the ECC algorithm.

        Returns
        -------
        tuple[int, int, float]
            Criteria tuple passed to ``cv2.findTransformECC``.
        """
        return (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, self.max_iter, self.eps)

    @property
    def cv2_motion_type(self) -> int:
        """
        Get the CV2 motion type for the ECC algorithm.

        Returns
        -------
        int
            OpenCV motion type constant.
        """
        return self.transform_type.to_cv2_motion_type
