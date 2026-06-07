from __future__ import annotations

from dataclasses import dataclass, field

from kp_detection import ShiTomashiParameters
from optical_flow import PyrLKParameters

from ...parameter import ImageRegistrationParameters


@dataclass
class LucasKanadeRegistrationParameters(ImageRegistrationParameters):
    """
    Parameters for Lucas-Kanade optical flow registration.

    Attributes
    ----------
    transform_type : PerspectiveTransformationMethod
        Type of transformation to apply.
    ransac_th : float
        RANSAC threshold for outlier rejection.
    optical_flow_parameters : PyrLKParameters
        Pyramid Lucas-Kanade optical flow parameters.
    kp_detection_parameters : ShiTomashiParameters
        Shi-Tomasi keypoint detector parameters.
    """

    optical_flow_parameters: PyrLKParameters = field(default_factory=PyrLKParameters)
    kp_detection_parameters: ShiTomashiParameters = field(
        default_factory=ShiTomashiParameters
    )
