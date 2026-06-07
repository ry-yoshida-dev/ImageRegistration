from __future__ import annotations

from kp_matching import PairedDetectionResult
from optical_flow import FarnebackResult, LucasKanadeResult

from .ecc import ECCResult

type RegistrationDetailResult = (
    PairedDetectionResult | FarnebackResult | LucasKanadeResult | ECCResult
)
