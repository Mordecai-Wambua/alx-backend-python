#!/usr/bin/env python3
"""Fuction that returns a asyncio.Task."""
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int):
    """Return a asyncio.Task."""
    return asyncio.create_task(wait_random(max_delay))
