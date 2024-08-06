#!/usr/bin/env python3
"""Coroutine to collect 10 random numbers using  an async comprehension."""
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """Return the 10 random numbers."""
    return [i async for i in async_generator()]
