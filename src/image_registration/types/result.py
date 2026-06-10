"""Registration detail result type aliases."""

from __future__ import annotations

from kp_matching import PairedDetectionResult
from optical_flow import FarnebackResult, LucasKanadeResult

from ..ecc.result import ECCResult

type RegistrationDetailResult = (
    PairedDetectionResult | FarnebackResult | LucasKanadeResult | ECCResult
)
"""Method-specific registration detail returned with a motion matrix."""
