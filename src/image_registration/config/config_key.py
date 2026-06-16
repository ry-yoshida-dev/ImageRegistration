"""Configuration key paths for image registration DictConfig access."""

from __future__ import annotations

from enum import StrEnum


class ConfigKey(StrEnum):
    """
    Dot-notation paths for accessing image registration configuration.

    Use these keys with ``DictConfigHandler`` to read nested OmegaConf sections.
    Keys are relative to the section passed to ``RegistratorBuilder.from_config``.
    """

    METHOD = "method"

    KP_MATCHING = "KPMatching"
    ECC = "ECC"
    FARNEBACK = "Farneback"
    LUCAS_KANADE = "LucasKanade"
