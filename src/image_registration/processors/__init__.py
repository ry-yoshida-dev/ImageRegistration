from ..ecc import ECCParameters, ECCProcessor
from .ecc import ECCRegistrationParameters, ECCRegistrator
from .farneback import FarnebackRegistrationParameters, FarnebackRegistrator
from .kp_matching import KPMatchingRegistration, KPMatchingRegistrationParameters
from .lucas_kanade import LucasKanadeRegistrationParameters, LucasKanadeRegistrator

MethodRegistrationParameters = (
    KPMatchingRegistrationParameters
    | ECCRegistrationParameters
    | LucasKanadeRegistrationParameters
    | FarnebackRegistrationParameters
)

__all__ = [
    "ECCParameters",
    "ECCProcessor",
    "ECCRegistrationParameters",
    "ECCRegistrator",
    "FarnebackRegistrationParameters",
    "FarnebackRegistrator",
    "KPMatchingRegistration",
    "KPMatchingRegistrationParameters",
    "LucasKanadeRegistrationParameters",
    "LucasKanadeRegistrator",
    "MethodRegistrationParameters",
]
