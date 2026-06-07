from __future__ import annotations

from dataclasses import dataclass, field
from typing import override

import numpy as np

from kp_detection import KPDetector
from kp_matching import KPMatchingProcessor, MatchResult
from projective import PerspectiveMatrix

from ...data import RegistratorPreprocessedData
from ...registrator import Registrator
from ...parameter import ImageRegistrationParameters
from .parameter import KPMatchingRegistrationParameters


@dataclass(kw_only=True)
class KPMatchingRegistrator(Registrator[MatchResult]):
    """
    Keypoint-matching image registration processor.
    """

    registration_params: KPMatchingRegistrationParameters
    processor: KPMatchingProcessor = field(init=False, repr=False)

    @property
    @override
    def params(self) -> ImageRegistrationParameters:
        return self.registration_params

    def __post_init__(self) -> None:
        self.keypoint_detector: KPDetector | None = (
            self.registration_params.kp_detection_parameters.build_detector()
        )
        self.processor = KPMatchingProcessor(
            params=self.registration_params.kp_matching_parameters
        )
        super().__post_init__()

    @override
    def create_combined_mask(
        self,
        target_mask: np.ndarray | None,
        source_mask: np.ndarray | None,
    ) -> np.ndarray | None:
        if target_mask is None or source_mask is None:
            return None
        return target_mask & source_mask

    @override
    def compute_motion_matrix(
        self,
        target_data: RegistratorPreprocessedData,
        combined_mask: np.ndarray | None = None,
        initial_motion_matrix: PerspectiveMatrix | None = None,
    ) -> tuple[PerspectiveMatrix, MatchResult]:
        """
        Compute the motion matrix from matched keypoint correspondences.

        Parameters
        ----------
        target_data : RegistratorPreprocessedData
            Preprocessed target image data.
        combined_mask : np.ndarray | None
            Unused for keypoint matching; kept for interface compatibility.
        initial_motion_matrix : PerspectiveMatrix | None
            Unused for keypoint matching; kept for interface compatibility.

        Returns
        -------
        tuple[PerspectiveMatrix, MatchResult]
            Motion matrix in original image coordinates and keypoint match
            details.
        """
        del combined_mask, initial_motion_matrix

        match_result = self.processor.match(
            self.source_data.descriptors,
            target_data.descriptors,
        )
        matched_source_kps = np.array(
            [self.source_data.keypoints[match.queryIdx].pt for match in match_result.matches],
            dtype=np.float32,
        )
        matched_target_kps = np.array(
            [target_data.keypoints[match.trainIdx].pt for match in match_result.matches],
            dtype=np.float32,
        )
        transform_type = self.params.transform_type
        motion_matrix, _ = transform_type.perspective_class.create_from_points(
            origin_points=matched_source_kps,
            destination_points=matched_target_kps,
            ransac_th=self.params.ransac_th,
        )
        return motion_matrix, match_result
