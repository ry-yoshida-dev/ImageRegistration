"""NumPy array type aliases used across image registration."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

UInt8Image = npt.NDArray[np.uint8]
"""Grayscale or BGR image array with ``uint8`` pixel values."""

UInt8Mask = npt.NDArray[np.uint8]
"""Binary or numeric mask array aligned with an image, stored as ``uint8``."""
