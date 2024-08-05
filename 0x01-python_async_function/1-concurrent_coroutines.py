#!/usr/bin/env python3
"""Function / Coroutine to spawn wait_random a speciied number o times."""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Return a list of delays in ascending order."""
    tasks = [wait_random(max_delay) for _ in range(n)]
    delay = [await task for task in asyncio.as_completed(tasks)]
    return delay
