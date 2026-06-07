from __future__ import annotations

from dataclasses import dataclass, field

from kp_detection import KPDetectionMethod, KPDetectionParameters
from kp_matching import KPMatchCommonParameters, KPMatchingParameters

from ...parameter import ImageRegistrationParameters

DEFAULT_DETECTION_METHOD = KPDetectionMethod.SIFT

@dataclass
class KPMatchingRegistrationParameters(ImageRegistrationParameters):
    """
    Parameters for keypoint-matching image registration.

    Attributes
    ----------
    transform_type : PerspectiveTransformationMethod
        Type of transformation to apply.
    ransac_th : float
        RANSAC threshold for outlier rejection.
    kp_matching_parameters : KPMatchingParameters
        Keypoint matcher parameters.
    kp_detection_parameters : KPDetectionParameters
        Keypoint detector parameters used during preprocessing.
    """

    kp_matching_parameters: KPMatchingParameters = field(
        default_factory=lambda: KPMatchingParameters(
            common_params=KPMatchCommonParameters(
                detection_method=DEFAULT_DETECTION_METHOD,
            ),
        ),
    )
    kp_detection_parameters: KPDetectionParameters = field(
        default_factory=lambda: KPDetectionParameters(method=DEFAULT_DETECTION_METHOD),
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        if (
            self.kp_matching_parameters.common_params.detection_method
            != self.kp_detection_parameters.method
        ):
            raise ValueError(
                "kp_matching_parameters.common_params.detection_method must match "
                + "kp_detection_parameters.method: "
                + f"{self.kp_matching_parameters.common_params.detection_method.value} != "
                + f"{self.kp_detection_parameters.method.value}"
            )
