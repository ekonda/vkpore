# pylint: disable=missing-docstring,protected-access,redefined-outer-name
import pytest

from vkpore.events import Event

@pytest.mark.asyncio
async def test_initialization():
    event = Event(1, {})

    async def bad_callback(event):
        raise RuntimeError

    event.initialize(None, [bad_callback])

    with pytest.raises(RuntimeError):
        await event.next()
