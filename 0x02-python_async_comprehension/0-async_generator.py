#!/usr/bin/env python3
"""
Coroutine that loops 10 times, each time asynchronously wait 1 second.

then yield a random number between 0 and 10.
"""
import random
import asyncio
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """Yiels a random number between 0 and 10."""
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
