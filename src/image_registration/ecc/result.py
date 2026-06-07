from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ECCResult:
    """
    Result of an ECC registration run.

    Attributes
    ----------
    correlation_coefficient : float
        Final correlation coefficient returned by OpenCV ECC.
    is_converged : bool
        Whether ECC optimization converged successfully.
    """

    correlation_coefficient: float
    is_converged: bool
