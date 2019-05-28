"""Useful helpers"""

from typing import Awaitable
import asyncio


async def wait_with_stopped(awaitable: Awaitable, stopped: Awaitable, loop=None):
    """
    Wait for awaitable or stopped to complete. If stopped was
    completed - awaitable is cancelled and None is returned. Otherwise
    return awaitable's result.
    """

    done, pending = await asyncio.wait(
        {awaitable, stopped}, return_when=asyncio.FIRST_COMPLETED, loop=loop,
    )

    if stopped in done:
        if pending:
            pending.pop().cancel()
        return None

    return done.pop().result()


def read_only_properties(*attrs):
    """Make passed attributes read-only"""
    def decorator(cls):
        original_setattr = cls.__setattr__

        def modified_setattr(self, name, value):
            if name in attrs and getattr(self, name, None) is not None:
                raise AttributeError("Can't modify '{}'".format(name))
            original_setattr(self, name, value)

        cls.__setattr__ = modified_setattr

        return cls
    return decorator
