# types

## Overview

Shared type aliases for image registration. Import from `image_registration.types` or the package root re-exports.

## Components

| Component | Description |
| --------- | ----------- |
| [`array.py`](./array.py) | ``uint8`` image and mask array aliases |
| [`result.py`](./result.py) | Union alias for method-specific registration detail results |

## Examples

```python
from image_registration import UInt8Image, UInt8Mask, RegistrationDetailResult
```
