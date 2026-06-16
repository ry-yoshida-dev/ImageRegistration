# config/utils

## Overview

Internal helpers for mapping ``RegistrationMethod`` values to parameter dataclasses and ``ConfigKey`` paths.

## Components

| Component | Description |
| --------- | ----------- |
| [`method_with_key.py`](./method_with_key.py) | ``MethodWithKey`` dataclass pairing a parameter type with a config key |
| [`key_name_resolver.py`](./key_name_resolver.py) | ``KeyNameResolver`` that resolves ``RegistrationMethod`` to ``MethodWithKey`` |
