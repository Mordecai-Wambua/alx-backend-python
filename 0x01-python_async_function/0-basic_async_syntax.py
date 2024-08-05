#!/usr/bin/env python3
"""Function that waits for a random delay."""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Return the random delay."""
    number: float = random.uniform(0, max_delay)
    await asyncio.sleep(number)
    return number
