from __future__ import annotations

import numpy as np
import pytest
from projective import PerspectiveTransformationMethod, register_perspective_matrix

from image_registration.ecc import ECCParameters, ECCProcessor


def test_ecc_processor_returns_identity_on_non_convergence() -> None:
    """ECC should return an identity matrix when optimization does not converge."""
    blank_image = np.zeros((64, 64), dtype=np.uint8)
    processor = ECCProcessor(
        params=ECCParameters(
            transform_type=PerspectiveTransformationMethod.AFFINE,
            max_iter=1,
            eps=1e-12,
        ),
    )

    motion_matrix, ecc_result = processor.run(blank_image, blank_image)

    expected_identity = register_perspective_matrix(
        matrix=None,
        transform_type=PerspectiveTransformationMethod.AFFINE,
    )
    np.testing.assert_allclose(motion_matrix.value, expected_identity.value, atol=1e-6)
    assert ecc_result.is_converged is False
    assert ecc_result.correlation_coefficient == 0.0


def test_ecc_processor_rejects_invalid_scale_factor(image_size: tuple[int, int]) -> None:
    """ECC rescaling should fail fast when scale_factor yields invalid dimensions."""
    height, width = image_size
    image = np.zeros((height, width), dtype=np.uint8)
    processor = ECCProcessor(
        params=ECCParameters(
            transform_type=PerspectiveTransformationMethod.AFFINE,
            scale_factor=0.001,
        ),
    )

    with pytest.raises(ValueError):
        processor.run(image, image)
