#!/usr/bin/env python3
"""Function to fins the sum of a list of integers and floats."""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Return the sum of list elements."""
    sum: float = 0
    for x in mxd_lst:
        sum += x
    return sum
