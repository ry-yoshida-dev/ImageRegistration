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

`method` must match a ``RegistrationMethod`` value: ``"KPMatching"``, ``"ECC"``, ``"Farneback"``, or ``"LucasKanade"``. Each method reads parameters from the section with the same name under ``ImageRegistration``.

### ECC

```python
from omegaconf import OmegaConf

from image_registration.config import ConfigKey, RegistratorBuilder

cfg = OmegaConf.create(
    {
        ConfigKey._IMAGE_REGISTRATION: {
            "method": "ECC",
            "ECC": {
                "transform_type": "AFFINE",
                "ransac_th": 3.0,
                "ecc_parameters": {
                    "transform_type": "AFFINE",
                    "scale_factor": 1.0,
                    "max_iter": 100,
                },
            },
        },
    }
)

registrator = RegistratorBuilder.from_config(cfg).build(source_image=frame)
motion_matrix, detail_result = registrator.run_registration_pipeline(next_frame)
```

### KPMatching

```python
cfg = OmegaConf.create(
    {
        ConfigKey._IMAGE_REGISTRATION: {
            "method": "KPMatching",
            "KPMatching": {
                "transform_type": "AFFINE",
                "ransac_th": 3.0,
                "kp_detection_parameters": {
                    "method": "SIFT",
                    "scale_factor": 0.25,
                },
                "kp_matching_parameters": {
                    "common_params": {
                        "detection_method": "SIFT",
                        "method": "KNN",
                        "knn": 2,
                    },
                },
            },
        },
    }
)

registrator = RegistratorBuilder.from_config(cfg).build(source_image=frame)
```

`kp_detection_parameters.method` and `kp_matching_parameters.common_params.detection_method` must match.

### Farneback

```python
cfg = OmegaConf.create(
    {
        ConfigKey._IMAGE_REGISTRATION: {
            "method": "Farneback",
            "Farneback": {
                "transform_type": "AFFINE",
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
        },
    }
)

registrator = RegistratorBuilder.from_config(cfg).build(source_image=frame)
```

### LucasKanade

```python
cfg = OmegaConf.create(
    {
        ConfigKey._IMAGE_REGISTRATION: {
            "method": "LucasKanade",
            "LucasKanade": {
                "transform_type": "AFFINE",
                "optical_flow_parameters": {
                    "scale_factor": 0.5,
                },
                "kp_detection_parameters": {
                    "max_corners": 500,
                    "min_distance": 5,
                },
            },
        },
    }
)

registrator = RegistratorBuilder.from_config(cfg).build(source_image=frame)
```

### Defaults only

When a method section is omitted, ``RegistratorBuilder`` falls back to dataclass defaults:

```python
cfg = OmegaConf.create(
    {
        ConfigKey._IMAGE_REGISTRATION: {
            "method": "ECC",
        },
    }
)

registration_params = RegistratorBuilder.from_config(cfg).build_registration_params()
registrator = RegistratorBuilder.from_config(cfg).build(source_image=frame)
```
