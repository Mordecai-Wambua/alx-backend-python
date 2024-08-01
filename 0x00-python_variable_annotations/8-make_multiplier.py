#!/usr/bin/env python3
"""Function that takes a float argument and returns a function."""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Return a Callable function."""
    return lambda x: x * multiplier
