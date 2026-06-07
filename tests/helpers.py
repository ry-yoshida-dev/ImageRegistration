from __future__ import annotations

import numpy as np
from projective import PerspectiveMatrix


def assert_affine_matrix_close(
    estimated: PerspectiveMatrix,
    expected: np.ndarray,
    tolerance: float,
) -> None:
    """
    Assert that an estimated affine matrix is close to the expected matrix.

    Parameters
    ----------
    estimated : PerspectiveMatrix
        Estimated motion matrix.
    expected : np.ndarray
        Ground-truth 2x3 affine matrix.
    tolerance : float
        Maximum allowed absolute element-wise difference.
    """
    difference = float(np.max(np.abs(estimated.value - expected)))
    assert difference <= tolerance, (
        f"Matrix difference {difference} exceeds tolerance {tolerance}.\n"
        + f"Estimated:\n{estimated.value}\nExpected:\n{expected}"
    )
