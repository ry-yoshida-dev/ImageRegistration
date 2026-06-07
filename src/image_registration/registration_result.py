from __future__ import annotations

from kp_matching import MatchResult
from optical_flow import FarnebackResult, LucasKanadeResult

from .ecc import ECCResult

type RegistrationDetailResult = MatchResult | FarnebackResult | LucasKanadeResult | ECCResult
