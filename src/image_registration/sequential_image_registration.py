from __future__ import annotations

from dataclasses import dataclass, field

from projective import PerspectiveMatrix, register_perspective_matrix

from .types import RegistrationDetailResult, UInt8Image, UInt8Mask
from .data import RegistratorPreprocessedData
from .registrator import Registrator
from .method import RegistrationMethod
from .processors import MethodRegistrationParameters


@dataclass(kw_only=True)
class SequentialImageRegistrator:
    """
    Sequential image registration for frame-by-frame processing.
    """

    method: RegistrationMethod
    previous_image: UInt8Image
    registration_params: MethodRegistrationParameters
    previous_mask: UInt8Mask | None = None
    normal_registrator: Registrator[RegistrationDetailResult] = field(init=False, repr=False)
    previous_data: RegistratorPreprocessedData = field(init=False, repr=False)
    previous_motion_matrix: PerspectiveMatrix = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.normal_registrator = self.method.build_registrator(
            source_image=self.previous_image,
            registration_params=self.registration_params,
            source_mask=self.previous_mask,
        )
        self.previous_data = self.normal_registrator.source_data
        self.previous_motion_matrix = register_perspective_matrix(
            matrix=None,
            transform_type=self.normal_registrator.params.transform_type,
        )

    def update(
        self,
        current_image: UInt8Image,
        current_mask: UInt8Mask | None = None,
    ) -> tuple[PerspectiveMatrix, RegistrationDetailResult]:
        """
        Register the current frame against the previous frame and advance state.

        Parameters
        ----------
        current_image : UInt8Image
            Frame to register.
        current_mask : UInt8Mask | None
            Optional mask for the current frame.

        Returns
        -------
        tuple[PerspectiveMatrix, RegistrationDetailResult]
            Motion matrix in original image coordinates and method-specific
            registration details.
        """
        current_data = self.normal_registrator.preprocess(
            image=current_image,
            mask=current_mask,
        )
        combined_mask = self.normal_registrator.create_combined_mask(
            target_mask=current_data.mask,
            source_mask=self.previous_data.mask,
        )
        motion_matrix, detail_result = self.normal_registrator.compute_motion_matrix(
            target_data=current_data,
            combined_mask=combined_mask,
            initial_motion_matrix=self.previous_motion_matrix,
        )

        self.normal_registrator.source_data = current_data
        self.previous_data = current_data
        self.previous_motion_matrix = motion_matrix
        return motion_matrix, detail_result

    def register_image(
        self,
        image: UInt8Image,
        mask: UInt8Mask | None = None,
    ) -> None:
        """
        Replace the reference frame without computing a motion matrix.

        Parameters
        ----------
        image : UInt8Image
            New reference image.
        mask : UInt8Mask | None
            Optional mask for the new reference image.
        """
        current_data = self.normal_registrator.preprocess(
            image=image,
            mask=mask,
        )
        self.normal_registrator.source_data = current_data
        self.previous_data = current_data
