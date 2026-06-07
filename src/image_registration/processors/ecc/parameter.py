from __future__ import annotations

from dataclasses import dataclass, field

from ...ecc.parameter import ECCParameters
from ...parameter import ImageRegistrationParameters


@dataclass
class ECCRegistrationParameters(ImageRegistrationParameters):
    """
    Parameters for ECC image registration.

    Attributes
    ----------
    transform_type : PerspectiveTransformationMethod
        Type of transformation to apply.
    ransac_th : float
        RANSAC threshold for outlier rejection.
    ecc_parameters : ECCParameters
        ECC algorithm parameters.
    """

    ecc_parameters: ECCParameters = field(default_factory=ECCParameters)
