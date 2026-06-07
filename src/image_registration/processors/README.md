# processors

## Overview

This module contains image registration implementations organized by method. Each method sub-package provides a `registrator.py` and `parameter.py`. ECC additionally uses the top-level [`ecc/`](../ecc/) package for low-level processing.

## Components

| Component | Description |
| --------- | ----------- |
| [`ecc/`](./ecc/) | ECC pipeline registrator and registration parameters |
| [`kp_matching/`](./kp_matching/) | Keypoint detection and matching registration |
| [`lucas_kanade/`](./lucas_kanade/) | Pyramid Lucas-Kanade optical flow registration |
| [`farneback/`](./farneback/) | Farneback dense optical flow registration |

## Examples

```python
from image_registration import (
    ECCRegistrationParameters,
    RegistrationMethod,
)

registration_params = ECCRegistrationParameters()
registrator = RegistrationMethod.ECC.build_registrator(
    source_image=frame,
    registration_params=registration_params,
)
motion_matrix, detail_result = registrator.run_registration_pipeline(next_frame)
```
