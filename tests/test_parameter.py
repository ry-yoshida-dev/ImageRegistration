from __future__ import annotations

import pytest

from image_registration import ImageRegistrationParameters
from image_registration.ecc import ECCParameters
from image_registration.processors import KPMatchingRegistrationParameters
from kp_detection import KPDetectionMethod, KPDetectionParameters
from kp_matching import KPMatchCommonParameters, KPMatchingParameters


def test_image_registration_parameters_rejects_non_positive_ransac_threshold() -> None:
    """RANSAC threshold validation should fail fast for non-positive values."""
    with pytest.raises(ValueError, match="RANSAC threshold must be greater than 0"):
        ImageRegistrationParameters(ransac_th=0.0)


def test_ecc_parameters_reject_non_positive_scale_factor() -> None:
    """ECC scale factor validation should fail fast for non-positive values."""
    with pytest.raises(ValueError, match="scale_factor must be a positive number"):
        ECCParameters(scale_factor=0.0)


def test_kp_matching_parameters_reject_mismatched_detection_methods() -> None:
    """Detector and matcher detection methods must stay aligned."""
    with pytest.raises(ValueError, match="detection_method must match"):
        KPMatchingRegistrationParameters(
            kp_matching_parameters=KPMatchingParameters(
                common_params=KPMatchCommonParameters(
                    detection_method=KPDetectionMethod.SIFT,
                ),
            ),
            kp_detection_parameters=KPDetectionParameters(method=KPDetectionMethod.ORB),
        )
