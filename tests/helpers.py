from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from projective import PerspectiveMatrix


def assert_affine_matrix_close(
    estimated: PerspectiveMatrix,
    expected: NDArray[np.float64],
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
    difference = float(np.abs(estimated.value - expected).max())
    assert difference <= tolerance, (
        f"Matrix difference {difference} exceeds tolerance {tolerance}.\n"
        + f"Estimated:\n{estimated.value}\nExpected:\n{expected}"
    )
