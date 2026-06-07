from __future__ import annotations

import cv2
import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar

from kp_detection import KPDetector
from projective import (
    PerspectiveMatrix,
    register_perspective_matrix,
)

from .data import RegistratorPreprocessedData
from .parameter import ImageRegistrationParameters

DetailResultT = TypeVar("DetailResultT")


@dataclass(kw_only=True)
class Registrator[DetailResultT](ABC):
    """
    Abstract base dataclass for image registration.
    """

    source_image: np.ndarray
    source_mask: np.ndarray | None = None
    keypoint_detector: KPDetector | None = field(default=None, init=False)
    source_data: RegistratorPreprocessedData = field(init=False, repr=False)
    motion_matrix: PerspectiveMatrix = field(init=False, repr=False)
    previous_motion_matrix: PerspectiveMatrix = field(init=False, repr=False)

    @property
    @abstractmethod
    def params(self) -> ImageRegistrationParameters:
        """Return common registration parameters for this registrator."""

    def __post_init__(self) -> None:
        self.previous_motion_matrix = register_perspective_matrix(
            matrix=None,
            transform_type=self.params.transform_type,
        )
        self.motion_matrix = register_perspective_matrix(
            matrix=None,
            transform_type=self.params.transform_type,
        )
        self.source_data = self.preprocess(
            self.source_image,
            mask=self.source_mask,
        )

    def preprocess(
        self,
        image: np.ndarray,
        mask: np.ndarray | None = None,
    ) -> RegistratorPreprocessedData:
        """
        Convert an input image to grayscale and detect keypoints.

        Image rescaling is delegated to downstream packages such as
        ``kp_detection`` and ``optical_flow`` via their ``scale_factor`` fields.

        Parameters
        ----------
        image : np.ndarray
            Input image in grayscale or BGR format.
        mask : np.ndarray | None
            Optional mask aligned with ``image``.

        Returns
        -------
        RegistratorPreprocessedData
            Grayscale image, keypoints, descriptors, and optional mask.
        """
        grayscale_image = (
            image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        )

        if self.keypoint_detector is None:
            keypoints: list[cv2.KeyPoint] = []
            descriptors = np.array([])
        else:
            detection_result = self.keypoint_detector.detect(
                grayscale_image,
                mask=mask,
            )
            keypoints = list(detection_result.keypoints)
            descriptors = (
                detection_result.descriptors
                if detection_result.descriptors is not None
                else np.array([])
            )

        return RegistratorPreprocessedData(
            image=grayscale_image,
            keypoints=keypoints,
            descriptors=descriptors,
            mask=mask,
        )

    def run_registration_pipeline(
        self,
        target_image: np.ndarray,
        target_mask: np.ndarray | None = None,
        initial_motion_matrix: PerspectiveMatrix | None = None,
    ) -> tuple[PerspectiveMatrix, DetailResultT]:
        """
        Run the full registration pipeline and return the motion matrix.

        Parameters
        ----------
        target_image : np.ndarray
            Target image to register against the source.
        target_mask : np.ndarray | None
            Optional mask for the target image.
        initial_motion_matrix : PerspectiveMatrix | None
            Optional initial motion matrix in original image coordinates.

        Returns
        -------
        tuple[PerspectiveMatrix, DetailResultT]
            Motion matrix in original image coordinates and method-specific
            registration details.
        """
        target_data = self.preprocess(
            image=target_image,
            mask=target_mask,
        )
        combined_mask = self.create_combined_mask(
            target_mask=target_data.mask,
            source_mask=self.source_data.mask,
        )
        return self.compute_motion_matrix(
            target_data=target_data,
            combined_mask=combined_mask,
            initial_motion_matrix=initial_motion_matrix,
        )

    @abstractmethod
    def create_combined_mask(
        self,
        target_mask: np.ndarray | None,
        source_mask: np.ndarray | None,
    ) -> np.ndarray | None:
        """
        Create a combined mask from the target mask and the source mask.
        """

    @abstractmethod
    def compute_motion_matrix(
        self,
        target_data: RegistratorPreprocessedData,
        combined_mask: np.ndarray | None = None,
        initial_motion_matrix: PerspectiveMatrix | None = None,
    ) -> tuple[PerspectiveMatrix, DetailResultT]:
        """
        Compute the motion matrix from the target data and the combined mask.

        Parameters
        ----------
        target_data : RegistratorPreprocessedData
            Preprocessed target image data.
        combined_mask : np.ndarray | None
            Optional combined mask aligned with ``target_data.image``.
        initial_motion_matrix : PerspectiveMatrix | None
            Optional initial motion matrix in original image coordinates.

        Returns
        -------
        tuple[PerspectiveMatrix, DetailResultT]
            Motion matrix in original image coordinates and method-specific
            registration details.
        """
