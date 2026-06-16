from __future__ import annotations

import numpy as np
import pytest
from omegaconf import OmegaConf
from projective import PerspectiveTransformationMethod

from image_registration import RegistrationMethod, UInt8Image
from image_registration.config import ConfigKey, RegistratorBuilder
from image_registration.ecc import ECCResult
from image_registration.processors import ECCRegistrator

from tests.helpers import assert_affine_matrix_close

AFFINE_TRANSFORM_TYPE = PerspectiveTransformationMethod.AFFINE


def test_registrator_builder_builds_ecc_from_config(
    source_image: UInt8Image,
    target_image: UInt8Image,
    affine_transform: np.ndarray,
) -> None:
    """RegistratorBuilder should deserialize ECC parameters and build a registrator."""
    cfg = OmegaConf.create(
        {
            ConfigKey._IMAGE_REGISTRATION: {
                "method": RegistrationMethod.ECC.value,
                "ECC": {
                    "transform_type": AFFINE_TRANSFORM_TYPE.value,
                    "ecc_parameters": {
                        "transform_type": AFFINE_TRANSFORM_TYPE.value,
                    },
                },
            },
        }
    )

    registrator = RegistratorBuilder.from_config(cfg).build(source_image=source_image)

    assert isinstance(registrator, ECCRegistrator)
    motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)
    assert_affine_matrix_close(motion_matrix, affine_transform, tolerance=0.05)
    assert isinstance(detail_result, ECCResult)
    assert detail_result.is_converged is True


def test_registrator_builder_uses_defaults_for_missing_method_section(
    source_image: UInt8Image,
) -> None:
    """Missing method sections should fall back to dataclass defaults."""
    cfg = OmegaConf.create(
        {
            ConfigKey._IMAGE_REGISTRATION: {
                "method": RegistrationMethod.ECC.value,
            },
        }
    )

    registrator = RegistratorBuilder.from_config(cfg).build(source_image=source_image)

    assert isinstance(registrator, ECCRegistrator)
    assert registrator.params.transform_type == PerspectiveTransformationMethod.HOMOGRAPHY


def test_registrator_builder_raises_when_method_key_is_missing() -> None:
    """The builder should fail fast when the method key is absent."""
    cfg = OmegaConf.create({ConfigKey._IMAGE_REGISTRATION: {}})

    with pytest.raises(ValueError, match="Configuration key"):
        RegistratorBuilder.from_config(cfg).resolve_method()
