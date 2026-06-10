from __future__ import annotations

from dataclasses import dataclass, field
from typing import override

from kp_detection import KPDetector
from optical_flow import LucasKanadeResult, PyrLKFlow
from projective import PerspectiveMatrix

from ...types import UInt8Mask
from ...data import RegistratorPreprocessedData
from ...registrator import Registrator
from ...parameter import ImageRegistrationParameters
from .parameter import LucasKanadeRegistrationParameters


@dataclass(kw_only=True)
class LucasKanadeRegistrator(Registrator[LucasKanadeResult]):
    """
    Pyramid Lucas-Kanade optical flow registration processor.
    """

    registration_params: LucasKanadeRegistrationParameters
    processor: PyrLKFlow = field(init=False, repr=False)

    @property
    @override
    def params(self) -> ImageRegistrationParameters:
        return self.registration_params

    def __post_init__(self) -> None:
        self.keypoint_detector: KPDetector | None = (
            self.registration_params.kp_detection_parameters.build_detector()
        )
        self.processor = PyrLKFlow(
            params=self.registration_params.optical_flow_parameters,
            keypoint_params=self.registration_params.kp_detection_parameters,
        )
        super().__post_init__()

    @override
    def create_combined_mask(
        self,
        target_mask: UInt8Mask | None,
        source_mask: UInt8Mask | None,
    ) -> UInt8Mask | None:
        if target_mask is None or source_mask is None:
            return None
        return source_mask

    @override
    def compute_motion_matrix(
        self,
        target_data: RegistratorPreprocessedData,
        combined_mask: UInt8Mask | None = None,
        initial_motion_matrix: PerspectiveMatrix | None = None,
    ) -> tuple[PerspectiveMatrix, LucasKanadeResult]:
        """
        Compute the motion matrix from Lucas-Kanade optical flow correspondences.

        Parameters
        ----------
        target_data : RegistratorPreprocessedData
            Preprocessed target image data.
        combined_mask : UInt8Mask | None
            Unused for Lucas-Kanade registration; kept for interface compatibility.
        initial_motion_matrix : PerspectiveMatrix | None
            Unused for Lucas-Kanade registration; kept for interface compatibility.

        Returns
        -------
        tuple[PerspectiveMatrix, LucasKanadeResult]
            Motion matrix in original image coordinates and Lucas-Kanade flow
            details.
        """
        del combined_mask, initial_motion_matrix

        flow_result = self.processor.run(
            source_image=self.source_data.image,
            target_image=target_data.image,
        )
        transform_type = self.params.transform_type
        motion_matrix, _ = transform_type.perspective_class.create_from_points(
            origin_points=flow_result.filtered_source_keypoints,
            destination_points=flow_result.filtered_target_keypoints,
            ransac_th=self.params.ransac_th,
        )
        return motion_matrix, flow_result
