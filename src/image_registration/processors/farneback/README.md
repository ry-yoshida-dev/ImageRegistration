# farneback

## Overview

This module provides Farneback dense optical flow registration.

## Components

| Component | Description |
| --------- | ----------- |
| [`registrator.py`](./registrator.py) | Farneback optical flow registrator |
| [`parameter.py`](./parameter.py) | Farneback registration parameters |

## Examples

```python
from image_registration import (
    FarnebackRegistrationParameters,
    RegistrationMethod,
)

registration_params = FarnebackRegistrationParameters()
registrator = RegistrationMethod.FARNEBACK_OPTICAL_FLOW.build_registrator(
    source_image=frame,
    registration_params=registration_params,
)
```
