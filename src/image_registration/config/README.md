# config

## Overview

Builds registrators from an OmegaConf DictConfig. `method` names the method (`ECC`, `KPMatching`, `Farneback`, or `LucasKanade`), and a section of the same name holds its parameters; omitted parameters keep their defaults.

## Components

| Component | Description |
| --------- | ----------- |
| [`config_key.py`](./config_key.py) | `ConfigKey`: dot-notation paths into the config |
| [`builder.py`](./builder.py) | `RegistratorBuilder`: builds the parameters and registrator of the configured method |
| [`utils/`](./utils/README.md) | Mapping of each method to its parameter class and config key |

## Examples

```python
from omegaconf import OmegaConf

from image_registration import RegistratorBuilder

cfg = OmegaConf.create({"method": "ECC", "ECC": {"transform_type": "Affine"}})
registrator = RegistratorBuilder.from_config(cfg).build(source_image=source_image)
motion_matrix, detail_result = registrator.run_registration_pipeline(target_image)
```
