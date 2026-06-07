# image-registration

## Overview

A typed Python library for image registration. It estimates a perspective motion matrix between a source frame and a target frame using one of four algorithms: ECC, keypoint matching, Farneback optical flow, or pyramid Lucas-Kanade optical flow.

Each method is configured through a dedicated parameter dataclass and returns a `PerspectiveMatrix` from the external [`projective`](https://github.com/ry-yoshida-dev/Projective) package together with method-specific detail results.

## Features

- **Multiple registration methods** — ECC, keypoint matching, Farneback, and Lucas-Kanade
- **Typed parameters** — method-specific dataclasses with shared common parameters
- **Sequential processing** — `SequentialImageRegistrator` for frame-by-frame video registration
- **Low-level ECC access** — `ECCProcessor` for direct ECC algorithm control
- **Strict typing** — ships with `py.typed` for static analysis support

## Installation

```bash
pip install git+https://github.com/ry-yoshida-dev/ImageRegistrator.git
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install -e .
```

## Quick Start

### Single-frame registration

```python
import cv2

from image_registration import (
    ECCRegistrationParameters,
    RegistrationMethod,
)

source = cv2.imread("frame_0.png")
target = cv2.imread("frame_1.png")

registration_params = ECCRegistrationParameters()
registrator = RegistrationMethod.ECC.build_registrator(
    source_image=source,
    registration_params=registration_params,
)
motion_matrix, detail_result = registrator.run_registration_pipeline(target)
```

### Sequential frame registration

```python
import cv2

from image_registration import (
    FarnebackRegistrationParameters,
    RegistrationMethod,
    SequentialImageRegistrator,
)

frames = [cv2.imread(f"frame_{i}.png") for i in range(10)]

sequential = SequentialImageRegistrator(
    method=RegistrationMethod.FARNEBACK_OPTICAL_FLOW,
    previous_image=frames[0],
    registration_params=FarnebackRegistrationParameters(),
)

for frame in frames[1:]:
    motion_matrix, detail_result = sequential.update(frame)
```

## Registration Methods

| Method | Enum | Parameter class |
| ------ | ---- | --------------- |
| ECC | `RegistrationMethod.ECC` | `ECCRegistrationParameters` |
| Keypoint matching | `RegistrationMethod.KP_MATCHING` | `KPMatchingRegistrationParameters` |
| Farneback optical flow | `RegistrationMethod.FARNEBACK_OPTICAL_FLOW` | `FarnebackRegistrationParameters` |
| Lucas-Kanade optical flow | `RegistrationMethod.LK_OPTICAL_FLOW` | `LucasKanadeRegistrationParameters` |

## Project Structure

| Path | Description |
| ---- | ----------- |
| [`src/image_registration/`](./src/image_registration/) | Core registration API and sequential registrator |
| [`src/image_registration/processors/`](./src/image_registration/processors/) | Method-specific registrators and parameters |
| [`src/image_registration/ecc/`](./src/image_registration/ecc/) | Low-level ECC algorithm processor |

See each directory's `README.md` for component-level details.

## Dependencies

| Package | Role |
| ------- | ---- |
| [`projective`](https://github.com/ry-yoshida-dev/Projective) | Perspective matrix types and transformation utilities |
| [`opencv-keypoint`](https://github.com/ry-yoshida-dev/OpenCVKeypoint) | Keypoint detection, matching, and optical flow |
| [`opencv-utility`](https://github.com/ry-yoshida-dev/OpenCVUtility) | OpenCV helper utilities |
| `opencv-contrib-python` | OpenCV bindings |
| `numpy` | Array operations |

## License

MIT License — see [LICENSE](./LICENSE).
