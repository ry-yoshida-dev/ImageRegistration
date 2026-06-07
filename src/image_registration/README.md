# registration

## Overview

This module provides image registration functionality. Each registration method is a dataclass that accepts typed parameters and a source image at construction time.

Perspective transforms (`PerspectiveMatrix`, `PerspectiveTransformationMethod`, etc.) are provided by the external `projective` package (see `requirements.txt`).

## Components

| Component | Description |
| --------- | ----------- |
| [`data.py`](./data.py) | Preprocessed image data used during registration |
| [`registrator.py`](./registrator.py) | Abstract base registrator returning motion matrix and detail result |
| [`parameter.py`](./parameter.py) | Common registration parameters shared by all methods |
| [`registration_result.py`](./registration_result.py) | Union type alias for method-specific registration detail results |
| [`ecc/`](./ecc/) | Low-level ECC algorithm processor |
| [`builder.py`](./builder.py) | Factory function for building registration processors |
| [`method.py`](./method.py) | Enumeration of available registration methods |
| [`sequential_image_registration.py`](./sequential_image_registration.py) | Sequential registration for processing image sequences |
| [`processors/`](./processors/) | Method-specific registrators and parameters |

## Examples

```python
from image_registration import (
    ECCRegistrationParameters,
    RegistrationMethod,
    build_registrator,
)

registration_params = ECCRegistrationParameters()
registrator = build_registrator(
    method=RegistrationMethod.ECC,
    source_image=frame,
    registration_params=registration_params,
)
motion_matrix, detail_result = registrator.run_registration_pipeline(next_frame)
```
