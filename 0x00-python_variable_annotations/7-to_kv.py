#!/usr/bin/env python3
"""Function to produce a tuple of the arguments."""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Return the formed tuple."""
    return (k, v**2)
