# lucas_kanade

## Overview

This module provides pyramid Lucas-Kanade sparse optical flow registration.

## Components

| Component | Description |
| --------- | ----------- |
| [`registrator.py`](./registrator.py) | Lucas-Kanade optical flow registrator |
| [`parameter.py`](./parameter.py) | Lucas-Kanade registration parameters |

## Examples

```python
from image_registration import (
    LucasKanadeRegistrationParameters,
    RegistrationMethod,
)

registration_params = LucasKanadeRegistrationParameters()
registrator = RegistrationMethod.LK_OPTICAL_FLOW.build_registrator(
    source_image=frame,
    registration_params=registration_params,
)
```
