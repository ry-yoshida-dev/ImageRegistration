# tests

## Overview

Pytest suite for the `image_registration` package. Tests cover parameter validation, factory wiring, preprocessing, affine registration accuracy on synthetic images, sequential frame updates, and ECC failure handling.

## Components

| Component | Description |
| --------- | ----------- |
| [`conftest.py`](./conftest.py) | Shared synthetic image fixtures |
| [`helpers.py`](./helpers.py) | Matrix comparison utilities for registration assertions |
| [`test_parameter.py`](./test_parameter.py) | Parameter dataclass validation |
| [`test_method_factory.py`](./test_method_factory.py) | `RegistrationMethod.build_registrator` type checks |
| [`test_preprocess.py`](./test_preprocess.py) | Image preprocessing behavior |
| [`test_registration_affine.py`](./test_registration_affine.py) | End-to-end affine registration for all methods |
| [`test_sequential.py`](./test_sequential.py) | `SequentialImageRegistrator` state management |
| [`test_ecc_processor.py`](./test_ecc_processor.py) | Low-level ECC processor edge cases |

## Examples

```bash
uv pip install -e ".[dev]"
pytest
```
