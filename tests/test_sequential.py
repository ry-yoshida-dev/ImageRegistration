from __future__ import annotations

import cv2
import numpy as np
from projective import PerspectiveTransformationMethod

from image_registration import (
    LucasKanadeRegistrationParameters,
    RegistrationMethod,
    SequentialImageRegistrator,
)

from tests.helpers import assert_affine_matrix_close


def test_sequential_update_advances_reference_frame(
    source_image: np.ndarray,
    target_image: np.ndarray,
    affine_transform: np.ndarray,
) -> None:
    """Sequential registration should return a motion matrix and advance state."""
    registration_params = LucasKanadeRegistrationParameters(
        transform_type=PerspectiveTransformationMethod.AFFINE,
    )
    sequential = SequentialImageRegistrator(
        method=RegistrationMethod.LK_OPTICAL_FLOW,
        previous_image=source_image,
        registration_params=registration_params,
    )

    motion_matrix, _ = sequential.update(target_image)
    assert_affine_matrix_close(motion_matrix, affine_transform, tolerance=0.5)
    np.testing.assert_array_equal(
        sequential.previous_data.image,
        sequential.normal_registrator.preprocess(target_image).image,
    )


def test_register_image_replaces_reference_without_motion_estimation(
    source_image: np.ndarray,
    target_image: np.ndarray,
) -> None:
    """register_image should replace the reference frame without estimation."""
    registration_params = LucasKanadeRegistrationParameters(
        transform_type=PerspectiveTransformationMethod.AFFINE,
    )
    sequential = SequentialImageRegistrator(
        method=RegistrationMethod.LK_OPTICAL_FLOW,
        previous_image=source_image,
        registration_params=registration_params,
    )
    sequential.update(target_image)

    new_reference = cv2.GaussianBlur(target_image, (5, 5), 0)
    sequential.register_image(new_reference)

    expected_data = sequential.normal_registrator.preprocess(new_reference)
    np.testing.assert_array_equal(
        sequential.previous_data.image,
        expected_data.image,
    )
