# ecc

## Overview

Low-level Enhanced Correlation Coefficient (ECC) processor that aligns two grayscale images without the shared registrator pipeline.

## Components

| Component | Description |
| --------- | ----------- |
| [`ecc.py`](./ecc.py) | ECC registration processor |
| [`parameter.py`](./parameter.py) | ECC algorithm parameters |
| [`result.py`](./result.py) | ECC optimization result |

## Examples

```python
from image_registration.ecc import ECCParameters, ECCProcessor

processor = ECCProcessor(params=ECCParameters(max_iter=200, scale_factor=0.25))
motion_matrix, ecc_result = processor.run(
    source_image=source_gray,
    target_image=target_gray,
    mask=optional_mask,
)
```
