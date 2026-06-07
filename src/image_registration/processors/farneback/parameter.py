from __future__ import annotations

from dataclasses import dataclass, field

from kp_detection import ShiTomashiParameters
from optical_flow import FarnebackParameters

from ...parameter import ImageRegistrationParameters


@dataclass
class FarnebackRegistrationParameters(ImageRegistrationParameters):
    """
    Parameters for Farneback optical flow registration.

    Attributes
    ----------
    transform_type : PerspectiveTransformationMethod
        Type of transformation to apply.
    ransac_th : float
        RANSAC threshold for outlier rejection.
    optical_flow_parameters : FarnebackParameters
        Farneback dense optical flow parameters.
    kp_detection_parameters : ShiTomashiParameters
        Shi-Tomasi keypoint detector parameters.
    """

    optical_flow_parameters: FarnebackParameters = field(
        default_factory=FarnebackParameters
    )
    kp_detection_parameters: ShiTomashiParameters = field(
        default_factory=ShiTomashiParameters
    )
