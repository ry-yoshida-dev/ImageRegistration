from __future__ import annotations

import numpy as np
from enum import Enum

from .registration_result import RegistrationDetailResult
from .registrator import Registrator
from .processors import (
    ECCRegistrationParameters,
    ECCRegistrator,
    FarnebackRegistrationParameters,
    FarnebackRegistrator,
    KPMatchingRegistration,
    KPMatchingRegistrationParameters,
    LucasKanadeRegistrationParameters,
    LucasKanadeRegistrator,
    MethodRegistrationParameters,
)


class RegistrationMethod(Enum):
    """
    Available image registration methods.
    """

    KP_MATCHING = "KPMatching"
    ECC = "ECC"
    FARBENACK_OPTICAL_FLOW = "Farneback"
    LK_OPTICAL_FLOW = "LucasKanade"

    def build_registrator(
        self,
        source_image: np.ndarray,
        registration_params: MethodRegistrationParameters,
        source_mask: np.ndarray | None = None,
    ) -> Registrator[RegistrationDetailResult]:
        """
        Build a registrator for this method using a typed parameter dataclass.

        Parameters
        ----------
        source_image : np.ndarray
            Source image used to initialize registration state.
        registration_params : MethodRegistrationParameters
            Method-specific parameter dataclass.
        source_mask : np.ndarray | None
            Optional mask for the source image.

        Returns
        -------
        Registrator
            Configured registrator instance.
        """
        match self:
            case RegistrationMethod.KP_MATCHING:
                if not isinstance(registration_params, KPMatchingRegistrationParameters):
                    raise TypeError(
                        "KP_MATCHING requires KPMatchingRegistrationParameters, "
                        + f"got {type(registration_params).__name__}"
                    )
                return KPMatchingRegistration(
                    source_image=source_image,
                    registration_params=registration_params,
                    source_mask=source_mask,
                )
            case RegistrationMethod.ECC:
                if not isinstance(registration_params, ECCRegistrationParameters):
                    raise TypeError(
                        "ECC requires ECCRegistrationParameters, "
                        + f"got {type(registration_params).__name__}"
                    )
                return ECCRegistrator(
                    source_image=source_image,
                    registration_params=registration_params,
                    source_mask=source_mask,
                )
            case RegistrationMethod.FARBENACK_OPTICAL_FLOW:
                if not isinstance(registration_params, FarnebackRegistrationParameters):
                    raise TypeError(
                        "FARBENACK_OPTICAL_FLOW requires FarnebackRegistrationParameters, "
                        + f"got {type(registration_params).__name__}"
                    )
                return FarnebackRegistrator(
                    source_image=source_image,
                    registration_params=registration_params,
                    source_mask=source_mask,
                )
            case RegistrationMethod.LK_OPTICAL_FLOW:
                if not isinstance(registration_params, LucasKanadeRegistrationParameters):
                    raise TypeError(
                        "LK_OPTICAL_FLOW requires LucasKanadeRegistrationParameters, "
                        + f"got {type(registration_params).__name__}"
                    )
                return LucasKanadeRegistrator(
                    source_image=source_image,
                    registration_params=registration_params,
                    source_mask=source_mask,
                )
