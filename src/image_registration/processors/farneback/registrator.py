from __future__ import annotations

from dataclasses import dataclass, field
from typing import override

import numpy as np

from kp_detection import KPDetector
from optical_flow import FarnebackFlow, FarnebackResult
from projective import PerspectiveMatrix

from ...data import RegistratorPreprocessedData
from ...registrator import Registrator
from ...parameter import ImageRegistrationParameters
from .parameter import FarnebackRegistrationParameters


@dataclass(kw_only=True)
class FarnebackRegistrator(Registrator[FarnebackResult]):
    """
    Farneback dense optical flow registration processor.
    """

    registration_params: FarnebackRegistrationParameters
    processor: FarnebackFlow = field(init=False, repr=False)

    @property
    @override
    def params(self) -> ImageRegistrationParameters:
        return self.registration_params

    def __post_init__(self) -> None:
        self.keypoint_detector: KPDetector | None = (
            self.registration_params.kp_detection_parameters.build_detector()
        )
        self.processor = FarnebackFlow(
            params=self.registration_params.optical_flow_parameters
        )
        super().__post_init__()

    @override
    def create_combined_mask(
        self,
        target_mask: np.ndarray | None,
        source_mask: np.ndarray | None,
    ) -> np.ndarray | None:
        """
        Create a combined mask for Farneback registration.

        Returns
        -------
        np.ndarray | None
            Source mask when both masks are provided.
        """
        if target_mask is None or source_mask is None:
            return None
        return source_mask

    @override
    def compute_motion_matrix(
        self,
        target_data: RegistratorPreprocessedData,
        combined_mask: np.ndarray | None = None,
        initial_motion_matrix: PerspectiveMatrix | None = None,
    ) -> tuple[PerspectiveMatrix, FarnebackResult]:
        """
        Compute the motion matrix from Farneback optical flow correspondences.

        Parameters
        ----------
        target_data : RegistratorPreprocessedData
            Preprocessed target image data.
        combined_mask : np.ndarray | None
            Optional mask applied during flow estimation and keypoint detection.
        initial_motion_matrix : PerspectiveMatrix | None
            Unused for Farneback registration; kept for interface compatibility.

        Returns
        -------
        tuple[PerspectiveMatrix, FarnebackResult]
            Motion matrix in original image coordinates and Farneback flow
            details.
        """
        del initial_motion_matrix

        if self.keypoint_detector is None:
            raise ValueError("Keypoint detector is not initialized.")

        flow_result = self.processor.run(
            source_image=self.source_data.image,
            target_image=target_data.image,
            mask=combined_mask,
        )
        flow = flow_result.flow
        previous_kp_result = self.keypoint_detector.detect(
            self.source_data.image,
            mask=combined_mask,
        )

        if len(previous_kp_result) == 0:
            raise ValueError("No keypoints were detected on the source image.")

        previous_points = previous_kp_result.coordinates.astype(np.float32)
        row_indices = previous_points[:, 1].astype(np.intp)
        col_indices = previous_points[:, 0].astype(np.intp)
        destination_points = previous_points + flow[row_indices, col_indices]

        transform_type = self.params.transform_type
        motion_matrix, _ = transform_type.perspective_class.create_from_points(
            origin_points=previous_points,
            destination_points=destination_points,
            ransac_th=self.params.ransac_th,
        )
        return motion_matrix, flow_result
