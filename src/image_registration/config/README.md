# config

## Overview

This package provides typed DictConfig access for image registration. Configuration keys are defined as dot-notation ``StrEnum`` members, and ``RegistratorBuilder`` uses ``DictConfigHandler`` and ``DataclassInitializer`` to deserialize method-specific parameter dataclasses and construct registrators.

## Components

| Component | Description |
| --------- | ----------- |
| [`config_key.py`](./config_key.py) | ``ConfigKey`` enum with dot-notation paths into the root config |
| [`utils/`](./utils/) | Internal helpers for mapping methods to parameter dataclasses and config keys |
| [`builder.py`](./builder.py) | ``RegistratorBuilder`` that builds any registrator from DictConfig |

## Examples

Pass a DictConfig with ``method`` and a method-specific section to
``RegistratorBuilder.from_config``.

Set ``method`` to one of ``"KPMatching"``, ``"ECC"``, ``"Farneback"``, or
``"LucasKanade"``, then place method-specific parameters in a subsection with
the same name. Use ``"Affine"`` or ``"Homography"`` for ``transform_type``.

Each snippet below is self-contained: it synthesizes random grayscale frames and
can be pasted into a Python REPL or script as-is.

### ECC

```python
import numpy as np
from omegaconf import OmegaConf

from image_registration.config import RegistratorBuilder

rng = np.random.default_rng(0)
source_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)
target_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)

cfg = OmegaConf.create(
    {
        "method": "ECC",
        "ECC": {
            "transform_type": "Affine",
            "ransac_th": 3.0,
            "ecc_parameters": {
                "transform_type": "Affine",
                "scale_factor": 1.0,
                "max_iter": 100,
            },
        },
    }
)

registrator = RegistratorBuilder.from_config(cfg).build(source_image=source_image)
motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)
```

### KPMatching

```python
import numpy as np
from omegaconf import OmegaConf

from image_registration.config import RegistratorBuilder

rng = np.random.default_rng(0)
source_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)
target_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)

cfg = OmegaConf.create(
    {
        "method": "KPMatching",
        "KPMatching": {
            "transform_type": "Affine",
            "ransac_th": 3.0,
            "kp_detection_parameters": {
                "method": "SIFT",
                "scale_factor": 0.25,
            },
            "kp_matching_parameters": {
                "common_params": {
                    "detection_method": "SIFT",
                    "method": "kNN",
                    "knn": 2,
                },
            },
        },
    }
)

registrator = RegistratorBuilder.from_config(cfg).build(source_image=source_image)
motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)
```

`kp_detection_parameters.method` and `kp_matching_parameters.common_params.detection_method` must match.
Use ``"kNN"`` (not ``"KNN"``) for k-nearest-neighbor matching.

### Farneback

```python
import numpy as np
from omegaconf import OmegaConf

from image_registration.config import RegistratorBuilder

rng = np.random.default_rng(0)
source_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)
target_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)

cfg = OmegaConf.create(
    {
        "method": "Farneback",
        "Farneback": {
            "transform_type": "Affine",
            "optical_flow_parameters": {
                "scale_factor": 0.5,
                "pyr_scale": 0.5,
                "levels": 3,
                "winsize": 15,
            },
            "kp_detection_parameters": {
                "max_corners": 1000,
                "quality_level": 0.01,
            },
        },
    }
)

registrator = RegistratorBuilder.from_config(cfg).build(source_image=source_image)
motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)
```

### LucasKanade

```python
import numpy as np
from omegaconf import OmegaConf

from image_registration.config import RegistratorBuilder

rng = np.random.default_rng(0)
source_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)
target_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)

cfg = OmegaConf.create(
    {
        "method": "LucasKanade",
        "LucasKanade": {
            "transform_type": "Affine",
            "optical_flow_parameters": {
                "scale_factor": 0.5,
            },
            "kp_detection_parameters": {
                "max_corners": 500,
                "min_distance": 5,
            },
        },
    }
)

registrator = RegistratorBuilder.from_config(cfg).build(source_image=source_image)
motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)
```

### Defaults only

When a method section is omitted, ``RegistratorBuilder`` falls back to dataclass defaults:

```python
import numpy as np
from omegaconf import OmegaConf

from image_registration.config import RegistratorBuilder

rng = np.random.default_rng(0)
source_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)
target_image = rng.integers(0, 256, size=(240, 320), dtype=np.uint8)

cfg = OmegaConf.create({"method": "ECC"})

builder = RegistratorBuilder.from_config(cfg)
registration_params = builder.build_registration_params()
registrator = builder.build(source_image=source_image)
motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)
```
