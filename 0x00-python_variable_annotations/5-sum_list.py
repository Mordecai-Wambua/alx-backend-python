#!/usr/bin/env python3
"""Function to find the sum of a list of floats."""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """Return the sum of the floats."""
    sum: float = 0
    for x in input_list:
        sum += x
    return sum
