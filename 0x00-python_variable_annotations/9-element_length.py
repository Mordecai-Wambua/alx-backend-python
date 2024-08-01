#!/usr/bin/env python3
"""Function to give the length of elements."""
from typing import List, Iterable, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Return a list of tuples each containig an element and its length."""
    return [(i, len(i)) for i in lst]
