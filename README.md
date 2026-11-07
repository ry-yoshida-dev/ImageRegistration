# image-registration

## Overview

A typed Python library for image registration. It estimates a perspective motion matrix (a `PerspectiveMatrix` from [`projective`](https://github.com/ry-yoshida-dev/Projective)) between a source frame and a target frame, together with method-specific detail results. `SequentialImageRegistrator` applies it frame by frame to video.

| Method | Enum | Parameter class |
| ------ | ---- | --------------- |
| ECC | `RegistrationMethod.ECC` | `ECCRegistrationParameters` |
| Keypoint matching | `RegistrationMethod.KP_MATCHING` | `KPMatchingRegistrationParameters` |
| Farneback optical flow | `RegistrationMethod.FARNEBACK_OPTICAL_FLOW` | `FarnebackRegistrationParameters` |
| Lucas-Kanade optical flow | `RegistrationMethod.LK_OPTICAL_FLOW` | `LucasKanadeRegistrationParameters` |

## Installation

```bash
pip install git+https://github.com/ry-yoshida-dev/ImageRegistration.git
```

## Usage

```python
import cv2

from image_registration import (
    ECCRegistrationParameters,
    FarnebackRegistrationParameters,
    RegistrationMethod,
    SequentialImageRegistrator,
)

source = cv2.imread("frame_0.png")
target = cv2.imread("frame_1.png")

registrator = RegistrationMethod.ECC.build_registrator(
    source_image=source,
    registration_params=ECCRegistrationParameters(),
)
motion_matrix, detail_result = registrator.run_registration_pipeline(target)

frames = [cv2.imread(f"frame_{i}.png") for i in range(10)]
sequential = SequentialImageRegistrator(
    method=RegistrationMethod.FARNEBACK_OPTICAL_FLOW,
    previous_image=frames[0],
    registration_params=FarnebackRegistrationParameters(),
)
for frame in frames[1:]:
    motion_matrix, detail_result = sequential.update(frame)
```

A registrator can also be built from an OmegaConf DictConfig; see [config](src/image_registration/config/README.md).

```python
from omegaconf import OmegaConf

from image_registration import RegistratorBuilder

cfg = OmegaConf.create({"method": "ECC", "ECC": {"transform_type": "Affine"}})
registrator = RegistratorBuilder.from_config(cfg).build(source_image=source)
```
