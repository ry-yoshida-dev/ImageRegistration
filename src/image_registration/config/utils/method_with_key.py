"""Parameter dataclass paired with its DictConfig key path."""

from __future__ import annotations

from dataclasses import dataclass

from ...processors import RegistrationMethodParameters
from ..config_key import ConfigKey


@dataclass(frozen=True)
class MethodWithKey:
    """
    Parameter dataclass paired with its DictConfig key path.

    Attributes
    ----------
    parameter_cls : type[RegistrationMethodParameters]
        Dataclass type used to deserialize method parameters.
    config_key : ConfigKey
        DictConfig path for the method-specific parameter section.
    """

    parameter_cls: type[RegistrationMethodParameters]
    config_key: ConfigKey
