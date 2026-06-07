from __future__ import annotations

import cv2
import numpy as np
from dataclasses import dataclass
from typing import override


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
    mask : np.ndarray | None
        Optional mask aligned with ``image``.
    """

    image: np.ndarray
    keypoints: list[cv2.KeyPoint]
    descriptors: np.ndarray
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
