from __future__ import annotations

import numpy as np

from image_registration import (
    ECCRegistrationParameters,
    KPMatchingRegistrationParameters,
    RegistrationMethod,
)


def test_preprocess_converts_bgr_to_grayscale(
    source_image_bgr: np.ndarray,
) -> None:
    """Registrator preprocessing should accept BGR images and convert them."""
    registrator = RegistrationMethod.ECC.build_registrator(
        source_image=source_image_bgr,
        registration_params=ECCRegistrationParameters(),
    )
    assert registrator.source_data.image.ndim == 2


def test_preprocess_detects_keypoints_for_kp_matching(
    source_image: np.ndarray,
) -> None:
    """Keypoint-based registrators should populate keypoints during preprocessing."""
    registrator = RegistrationMethod.KP_MATCHING.build_registrator(
        source_image=source_image,
        registration_params=KPMatchingRegistrationParameters(),
    )
    assert len(registrator.source_data.keypoints) > 0
    assert registrator.source_data.descriptors.size > 0
    assert registrator.source_data.detection_result is not None


def test_preprocess_keeps_grayscale_image_unchanged(
    source_image: np.ndarray,
) -> None:
    """Grayscale input should be stored without channel conversion."""
    registrator = RegistrationMethod.ECC.build_registrator(
        source_image=source_image,
        registration_params=ECCRegistrationParameters(),
    )
    np.testing.assert_array_equal(registrator.source_data.image, source_image)
