"""Configuration access and registrator construction from DictConfig."""

from .builder import RegistratorBuilder
from .config_key import ConfigKey

__all__ = [
    "ConfigKey",
    "RegistratorBuilder",
]
