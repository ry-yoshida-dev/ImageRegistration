# registration

## Overview

This module provides image registration functionality. Each registration method is a dataclass that accepts typed parameters and a source image at construction time.

Perspective transforms (`PerspectiveMatrix`, `PerspectiveTransformationMethod`, etc.) are provided by the external `projective` package (see `requirements.txt`).

## Components

| Component | Description |
| --------- | ----------- |
| [`types/`](./types/) | Shared type aliases for images, masks, and registration detail results |
| [`data.py`](./data.py) | Preprocessed image data used during registration |
| [`registrator.py`](./registrator.py) | Abstract base registrator returning motion matrix and detail result |
| [`parameter.py`](./parameter.py) | Common registration parameters shared by all methods |
| [`ecc/`](./ecc/) | Low-level ECC algorithm processor |
| [`method.py`](./method.py) | Enumeration of available registration methods with factory method |
| [`config/`](./config/) | DictConfig keys and ``RegistratorBuilder`` for config-driven construction |
| [`sequential_image_registration.py`](./sequential_image_registration.py) | Sequential registration for processing image sequences |
| [`processors/`](./processors/) | Method-specific registrators and parameters |

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

Config-driven construction:

```python
import numpy as np
from omegaconf import OmegaConf

from image_registration import RegistratorBuilder

rng = np.random.default_rng(0)
source_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)
target_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)

cfg = OmegaConf.create(
    {
        "method": "ECC",
        "ECC": {"transform_type": "Affine"},
    }
)
registrator = RegistratorBuilder.from_config(cfg).build(source_image=source_image)
motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)
```
