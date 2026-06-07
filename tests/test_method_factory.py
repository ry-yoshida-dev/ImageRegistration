from __future__ import annotations

import numpy as np
import pytest

from image_registration import (
    ECCRegistrationParameters,
    FarnebackRegistrationParameters,
    KPMatchingRegistrationParameters,
    RegistrationMethod,
)


def test_build_registrator_rejects_mismatched_parameter_type(
    source_image: np.ndarray,
) -> None:
    """Each registration method should require its own parameter dataclass."""
    with pytest.raises(TypeError, match="ECC requires ECCRegistrationParameters"):
        RegistrationMethod.ECC.build_registrator(
            source_image=source_image,
            registration_params=FarnebackRegistrationParameters(),
        )

    with pytest.raises(TypeError, match="KP_MATCHING requires KPMatchingRegistrationParameters"):
        RegistrationMethod.KP_MATCHING.build_registrator(
            source_image=source_image,
            registration_params=ECCRegistrationParameters(),
        )

    with pytest.raises(TypeError, match="FARNEBACK_OPTICAL_FLOW requires"):
        RegistrationMethod.FARNEBACK_OPTICAL_FLOW.build_registrator(
            source_image=source_image,
            registration_params=KPMatchingRegistrationParameters(),
        )

    with pytest.raises(TypeError, match="LK_OPTICAL_FLOW requires"):
        RegistrationMethod.LK_OPTICAL_FLOW.build_registrator(
            source_image=source_image,
            registration_params=ECCRegistrationParameters(),
        )
