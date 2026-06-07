# ecc

## Overview

This module integrates ECC into the shared `Registrator` pipeline. Low-level ECC execution lives in the top-level [`ecc/`](../../ecc/) package.

## Components

| Component | Description |
| --------- | ----------- |
| [`registrator.py`](./registrator.py) | Pipeline-integrated ECC registrator |
| [`parameter.py`](./parameter.py) | ECC registration parameters |

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
```
