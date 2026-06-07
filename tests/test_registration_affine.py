from __future__ import annotations

import numpy as np
import pytest
from projective import PerspectiveTransformationMethod

from image_registration import (
    ECCRegistrationParameters,
    FarnebackRegistrationParameters,
    KPMatchingRegistrationParameters,
    LucasKanadeRegistrationParameters,
    RegistrationMethod,
)
from image_registration.ecc import ECCParameters, ECCResult

from tests.helpers import assert_affine_matrix_close

AFFINE_TRANSFORM_TYPE = PerspectiveTransformationMethod.AFFINE


@pytest.mark.parametrize(
    ("method", "registration_params", "tolerance"),
    [
        pytest.param(
            RegistrationMethod.ECC,
            ECCRegistrationParameters(
                transform_type=AFFINE_TRANSFORM_TYPE,
                ecc_parameters=ECCParameters(transform_type=AFFINE_TRANSFORM_TYPE),
            ),
            0.05,
            id="ecc",
        ),
        pytest.param(
            RegistrationMethod.KP_MATCHING,
            KPMatchingRegistrationParameters(transform_type=AFFINE_TRANSFORM_TYPE),
            0.5,
            id="kp_matching",
        ),
        pytest.param(
            RegistrationMethod.FARNEBACK_OPTICAL_FLOW,
            FarnebackRegistrationParameters(transform_type=AFFINE_TRANSFORM_TYPE),
            1.0,
            id="farneback",
        ),
        pytest.param(
            RegistrationMethod.LK_OPTICAL_FLOW,
            LucasKanadeRegistrationParameters(transform_type=AFFINE_TRANSFORM_TYPE),
            0.5,
            id="lucas_kanade",
        ),
    ],
)
def test_affine_registration_recovers_known_transform(
    source_image: np.ndarray,
    target_image: np.ndarray,
    affine_transform: np.ndarray,
    method: RegistrationMethod,
    registration_params: (
        ECCRegistrationParameters
        | KPMatchingRegistrationParameters
        | FarnebackRegistrationParameters
        | LucasKanadeRegistrationParameters
    ),
    tolerance: float,
) -> None:
    """Each method should estimate a motion matrix close to the synthetic warp."""
    registrator = method.build_registrator(
        source_image=source_image,
        registration_params=registration_params,
    )
    motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)

    assert_affine_matrix_close(motion_matrix, affine_transform, tolerance)

    if method is RegistrationMethod.ECC:
        assert isinstance(detail_result, ECCResult)
        assert detail_result.is_converged is True
        assert detail_result.correlation_coefficient > 0.9
