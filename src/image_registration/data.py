from __future__ import annotations

import cv2
import numpy as np
from dataclasses import dataclass
from typing import override

from kp_detection import DetectionResultUnion


@dataclass
class RegistratorPreprocessedData:
    """
    Preprocessed image data used during registration.

    Attributes
    ----------
    image : np.ndarray
        Grayscale image in original image coordinates.
    keypoints : list[cv2.KeyPoint]
        Detected keypoints in original image coordinates.
    descriptors : np.ndarray
        Descriptor matrix aligned with ``keypoints``.
    detection_result : DetectionResultUnion | None
        Full keypoint detection result when a detector is configured.
    mask : np.ndarray | None
        Optional mask aligned with ``image``.
    """

    image: np.ndarray
    keypoints: list[cv2.KeyPoint]
    descriptors: np.ndarray
    detection_result: DetectionResultUnion | None = None
    mask: np.ndarray | None = None

    @override
    def __str__(self) -> str:
        mask_shape: str = (
            str(self.mask.shape) if self.mask is not None else "None"
        )
        return (
            "RegistratorPreprocessedData("
            + f"image.shape={self.image.shape}, "
            + f"keypoints.length={len(self.keypoints)}, "
            + f"descriptors.shape={self.descriptors.shape}, "
            + f"mask.shape={mask_shape})"
        )
