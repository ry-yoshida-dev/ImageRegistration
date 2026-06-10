"""Shared type aliases used across image registration."""

from __future__ import annotations

from .array import UInt8Image, UInt8Mask
from .result import RegistrationDetailResult

__all__ = [
    "RegistrationDetailResult",
    "UInt8Image",
    "UInt8Mask",
]
