"""Build registrators from OmegaConf configuration."""

from __future__ import annotations

from dataclasses import dataclass

from dictconfig_handler import DictConfigHandler
from omegaconf import DictConfig

from ..method import RegistrationMethod
from ..processors import RegistrationMethodParameters
from ..registrator import Registrator
from ..types import RegistrationDetailResult, UInt8Image, UInt8Mask
from .config_key import ConfigKey
from .utils.key_name_resolver import KeyNameResolver


@dataclass
class RegistratorBuilder:
    """
    Build a ``Registrator`` from a DictConfig-backed handler.

    Attributes
    ----------
    handler : DictConfigHandler
        Handler that exposes typed access to the root configuration.
    """

    handler: DictConfigHandler

    @classmethod
    def from_config(cls, cfg: DictConfig) -> RegistratorBuilder:
        """
        Create a builder from a registration DictConfig.

        Parameters
        ----------
        cfg : DictConfig
            Registration configuration containing ``method`` and a method-specific
            section (for example ``ECC`` or ``KPMatching``).

        Returns
        -------
        RegistratorBuilder
            Builder bound to ``cfg``.
        """
        return cls(handler=DictConfigHandler(cfg=cfg))

    def resolve_method(self) -> RegistrationMethod:
        """
        Read and parse the configured registration method.

        Returns
        -------
        RegistrationMethod
            Method specified at ``ConfigKey.METHOD``.

        Raises
        ------
        ValueError
            If the method key is missing or its value is invalid.
        """
        method_value = self.handler.get_value(key=ConfigKey.METHOD)
        if not isinstance(method_value, str):
            raise ValueError(
                f"Configuration key '{ConfigKey.METHOD}' must be a string, "
                + f"got {type(method_value).__name__}"
            )
        return RegistrationMethod(method_value)

    def build_registration_params(
        self,
        method: RegistrationMethod | None = None,
        *,
        is_empty_allowed: bool = True,
    ) -> RegistrationMethodParameters:
        """
        Deserialize method-specific registration parameters from the configuration.

        Parameters
        ----------
        method : RegistrationMethod | None
            Registration method to deserialize. When ``None``, the method is
            read from ``ConfigKey.METHOD``.
        is_empty_allowed : bool
            If ``True``, missing method sections fall back to dataclass defaults.

        Returns
        -------
        RegistrationMethodParameters
            Instantiated parameter dataclass for the selected method.
        """
        resolved_method = method if method is not None else self.resolve_method()
        method_with_key = KeyNameResolver.resolve(resolved_method)
        return self.handler.build_dataclass(
            cls_=method_with_key.parameter_cls,
            key=method_with_key.config_key,
            is_empty_allowed=is_empty_allowed,
        )

    def build(
        self,
        source_image: UInt8Image,
        source_mask: UInt8Mask | None = None,
        *,
        method: RegistrationMethod | None = None,
        is_empty_allowed: bool = True,
    ) -> Registrator[RegistrationDetailResult]:
        """
        Build a registrator for the configured registration method.

        Parameters
        ----------
        source_image : UInt8Image
            Source image used to initialize registration state.
        source_mask : UInt8Mask | None
            Optional mask for the source image.
        method : RegistrationMethod | None
            Optional method override. When ``None``, the method is read from
            ``ConfigKey.METHOD``.
        is_empty_allowed : bool
            If ``True``, missing method sections fall back to dataclass defaults.

        Returns
        -------
        Registrator[RegistrationDetailResult]
            Configured registrator instance.
        """
        resolved_method = method if method is not None else self.resolve_method()
        registration_params = self.build_registration_params(
            method=resolved_method,
            is_empty_allowed=is_empty_allowed,
        )
        return resolved_method.build_registrator(
            source_image=source_image,
            registration_params=registration_params,
            source_mask=source_mask,
        )
