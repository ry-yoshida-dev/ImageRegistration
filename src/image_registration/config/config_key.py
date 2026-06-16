"""Configuration key paths for image registration DictConfig access."""

from __future__ import annotations

from enum import StrEnum


class ConfigKey(StrEnum):
    """
    Dot-notation paths for accessing image registration configuration.

    Use these keys with ``DictConfigHandler`` to read nested OmegaConf sections.
    """

    # Top-level keys
    _IMAGE_REGISTRATION = "ImageRegistration"

    METHOD = f"{_IMAGE_REGISTRATION}.method"

    # Method-specific parameter sections
    _KP_MATCHING = f"{_IMAGE_REGISTRATION}.KPMatching"
    _ECC = f"{_IMAGE_REGISTRATION}.ECC"
    _FARNEBACK = f"{_IMAGE_REGISTRATION}.Farneback"
    _LUCAS_KANADE = f"{_IMAGE_REGISTRATION}.LucasKanade"

    KP_MATCHING = _KP_MATCHING
    ECC = _ECC
    FARNEBACK = _FARNEBACK
    LUCAS_KANADE = _LUCAS_KANADE
