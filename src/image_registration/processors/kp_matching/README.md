# kp_matching

## Overview

This module provides keypoint-matching image registration using external `kp_detection` and `kp_matching` packages. Image rescaling is configured via `kp_detection_parameters.scale_factor`.

## Components

| Component | Description |
| --------- | ----------- |
| [`registrator.py`](./registrator.py) | Keypoint-matching registrator |
| [`parameter.py`](./parameter.py) | Keypoint-matching registration parameters |

## Examples

```python
from kp_detection import KPDetectionMethod, KPDetectionParameters
from kp_matching import KPMatchCommonParameters, KPMatchingParameters
from image_registration import (
    KPMatchingRegistrationParameters,
    RegistrationMethod,
)

registration_params = KPMatchingRegistrationParameters(
    kp_detection_parameters=KPDetectionParameters(
        method=KPDetectionMethod.SIFT,
        scale_factor=0.25,
    ),
    kp_matching_parameters=KPMatchingParameters(
        common_params=KPMatchCommonParameters(
            detection_method=KPDetectionMethod.SIFT,
        ),
    ),
)
registrator = RegistrationMethod.KP_MATCHING.build_registrator(
    source_image=frame,
    registration_params=registration_params,
)
```
