from dataclasses import dataclass
from projective import PerspectiveTransformationMethod


@dataclass
class ImageRegistrationParameters:
    """
    Parameters for image registration.

    Attributes
    ----------
    transform_type : PerspectiveTransformationMethod
        Type of transformation to apply.
    ransac_th : float
        RANSAC threshold for outlier rejection.
    """

    transform_type: PerspectiveTransformationMethod = (
        PerspectiveTransformationMethod.HOMOGRAPHY
    )
    ransac_th: float = 3.0

    def __post_init__(self) -> None:
        if self.ransac_th <= 0:
            raise ValueError("RANSAC threshold must be greater than 0")
