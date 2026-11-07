# tests

## Overview

Pytest suite for `image_registration`.

## Components

| Component | Description |
| --------- | ----------- |
| [`conftest.py`](./conftest.py) | Shared synthetic image fixtures |
| [`helpers.py`](./helpers.py) | Matrix comparison utilities for registration assertions |
| [`test_parameter.py`](./test_parameter.py) | Parameter dataclass validation |
| [`test_method_factory.py`](./test_method_factory.py) | `RegistrationMethod.build_registrator` type checks |
| [`test_config_builder.py`](./test_config_builder.py) | `RegistratorBuilder` DictConfig deserialization and construction |
| [`test_preprocess.py`](./test_preprocess.py) | Image preprocessing behavior |
| [`test_registration_affine.py`](./test_registration_affine.py) | End-to-end affine registration for all methods |
| [`test_sequential.py`](./test_sequential.py) | `SequentialImageRegistrator` state management |
| [`test_ecc_processor.py`](./test_ecc_processor.py) | Low-level ECC processor edge cases |
