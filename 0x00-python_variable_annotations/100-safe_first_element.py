#!/usr/bin/env python3
"""Function to produce the first element of any sequence type if it exists."""
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Return first sequence element."""
    if lst:
        return lst[0]
    else:
        return None
