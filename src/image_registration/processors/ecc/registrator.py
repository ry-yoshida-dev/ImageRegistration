from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import override

import numpy as np

from kp_detection import KPDetector
from projective import PerspectiveMatrix

from ...data import RegistratorPreprocessedData
from ...registrator import Registrator
from ...ecc import ECCProcessor, ECCResult
from ...parameter import ImageRegistrationParameters
from .parameter import ECCRegistrationParameters


@dataclass(kw_only=True)
class ECCRegistrator(Registrator[ECCResult]):
    """
    ECC-based image registration processor.

    Attributes
    ----------
    registration_params : ECCRegistrationParameters
        Parameters for the ECC algorithm.
    processor : ECCProcessor
        Processor for the ECC algorithm.
    """

    registration_params: ECCRegistrationParameters
    processor: ECCProcessor = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.keypoint_detector: KPDetector | None = None
        self.processor = ECCProcessor(
            params=replace(
                self.registration_params.ecc_parameters,
                transform_type=self.registration_params.transform_type,
            ),
        )
        super().__post_init__()

    @property
    @override
    def params(self) -> ImageRegistrationParameters:
        return self.registration_params

    @override
    def create_combined_mask(
        self,
        target_mask: np.ndarray | None,
        source_mask: np.ndarray | None,
    ) -> np.ndarray | None:
        if target_mask is None or source_mask is None:
            return None
        return target_mask & source_mask

    @override
    def compute_motion_matrix(
        self,
        target_data: RegistratorPreprocessedData,
        combined_mask: np.ndarray | None = None,
        initial_motion_matrix: PerspectiveMatrix | None = None,
    ) -> tuple[PerspectiveMatrix, ECCResult]:
        return self.processor.run(
            self.source_data.image,
            target_data.image,
            previous_motion_matrix=initial_motion_matrix,
            mask=combined_mask,
        )
