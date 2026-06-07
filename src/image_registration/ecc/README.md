# ecc

## Overview

This module provides the Enhanced Correlation Coefficient (ECC) registration algorithm. `ECCProcessor` aligns two grayscale images and returns a motion matrix from the `projective` package together with an `ECCResult` in original image coordinates. Image rescaling is configured via `ECCParameters.scale_factor`.

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
