from __future__ import annotations

import cv2
import numpy as np
import pytest

from image_registration import UInt8Image


@pytest.fixture
def image_size() -> tuple[int, int]:
    """Return the default synthetic image size as (height, width)."""
    return 240, 320


@pytest.fixture
def source_image(image_size: tuple[int, int]) -> UInt8Image:
    """Return a grayscale source image with distinct local features."""
    height, width = image_size
    image = np.zeros((height, width), dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (120, 80), 200, thickness=-1)
    cv2.circle(image, (200, 150), 40, 180, thickness=-1)
    cv2.circle(image, (80, 180), 25, 120, thickness=-1)

    rng = np.random.default_rng(42)
    for _ in range(30):
        center_x = int(rng.integers(0, width))
        center_y = int(rng.integers(0, height))
        radius = int(rng.integers(3, 8))
        color = int(rng.integers(50, 255))
        cv2.circle(image, (center_x, center_y), radius, color, thickness=-1)
    return image


@pytest.fixture
def affine_transform() -> np.ndarray:
    """Return a known 2x3 partial affine transform matrix."""
    return np.array(
        [
            [1.00480775, 0.04361939, 8.0],
            [-0.04361939, 1.00480775, -4.0],
        ],
        dtype=np.float64,
    )


@pytest.fixture
def target_image(
    source_image: UInt8Image,
    affine_transform: np.ndarray,
) -> UInt8Image:
    """Return the source image warped by ``affine_transform``."""
    height, width = source_image.shape
    return cv2.warpAffine(
        source_image,
        affine_transform,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE,
    )


@pytest.fixture
def source_image_bgr(source_image: UInt8Image) -> UInt8Image:
    """Return a BGR version of the grayscale source image."""
    return cv2.cvtColor(source_image, cv2.COLOR_GRAY2BGR)

