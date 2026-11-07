# registration

## Overview

Image registration API: method selection, shared parameters, the abstract registrator, and sequential registration over image streams.

## Components

| Component | Description |
| --------- | ----------- |
| [`types/`](./types/README.md) | Shared type aliases for images, masks, and registration detail results |
| [`data.py`](./data.py) | Preprocessed image data used during registration |
| [`registrator.py`](./registrator.py) | Abstract base registrator returning motion matrix and detail result |
| [`parameter.py`](./parameter.py) | Common registration parameters shared by all methods |
| [`ecc/`](./ecc/README.md) | Low-level ECC algorithm processor |
| [`method.py`](./method.py) | Enumeration of available registration methods with factory method |
| [`config/`](./config/README.md) | Config keys and `RegistratorBuilder` for building a registrator from a DictConfig |
| [`sequential_image_registration.py`](./sequential_image_registration.py) | Sequential registration for processing image sequences |
| [`processors/`](./processors/README.md) | Method-specific registrators and parameters |
