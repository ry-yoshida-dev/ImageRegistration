"""Resolve registration methods to parameter dataclass and config key pairs."""

from __future__ import annotations

from ...method import RegistrationMethod
from ...processors import (
    ECCRegistrationParameters,
    FarnebackRegistrationParameters,
    KPMatchingRegistrationParameters,
    LucasKanadeRegistrationParameters,
)
from ..config_key import ConfigKey
from .method_with_key import MethodWithKey


class KeyNameResolver:
    """
    Resolve a registration method to its parameter dataclass and config key.
    """

    @staticmethod
    def resolve(method: RegistrationMethod) -> MethodWithKey:
        """
        Resolve the parameter dataclass and config key for a registration method.

        Parameters
        ----------
        method : RegistrationMethod
            Registration method selected in the configuration.

        Returns
        -------
        MethodWithKey
            Parameter dataclass type and configuration key for ``method``.

        Raises
        ------
        ValueError
            If ``method`` is not registered.
        """
        match method:
            case RegistrationMethod.KP_MATCHING:
                return MethodWithKey(
                    parameter_cls=KPMatchingRegistrationParameters,
                    config_key=ConfigKey.KP_MATCHING,
                )
            case RegistrationMethod.ECC:
                return MethodWithKey(
                    parameter_cls=ECCRegistrationParameters,
                    config_key=ConfigKey.ECC,
                )
            case RegistrationMethod.FARNEBACK_OPTICAL_FLOW:
                return MethodWithKey(
                    parameter_cls=FarnebackRegistrationParameters,
                    config_key=ConfigKey.FARNEBACK,
                )
            case RegistrationMethod.LK_OPTICAL_FLOW:
                return MethodWithKey(
                    parameter_cls=LucasKanadeRegistrationParameters,
                    config_key=ConfigKey.LUCAS_KANADE,
                )
