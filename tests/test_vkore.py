# pylint: disable=missing-docstring,protected-access,redefined-outer-name
import asyncio
import pytest

from vkpore import Vkpore
from vkpore.events import MessageNew
from .testing_tools import Session


@pytest.fixture
def app(event_loop):
    app = Vkpore(["token"], session=Session(), loop=event_loop)

    yield app

def test_initialization():
    app = Vkpore(["token"])

    with pytest.raises(ValueError):
        app.run_until_complete(app.start())

    app.run_until_complete(app._session.close())


def test_no_clients(app):
    assert app.get_client(0) is None


@pytest.mark.asyncio
async def test_no_callbakcs(app):
    events = []

    @app.on("unknown_type")
    async def _(event):
        events.append(event)

    app.dispatch(MessageNew(1, {}))

    await app.stop()

    assert not events


@pytest.mark.asyncio
async def test_longpoll(app):
    complete = asyncio.Event()

    events = []

    @app.on("vk:raw")
    async def _(event):
        events.append(event)
        complete.set()

    await app.start()
    await complete.wait()
    await app.stop()

    assert events
    assert sorted(e.source for e in events) == [1, 2, 3]


MESSAGE_SOURCE = {
    "date": 1506592697, "from_id": 170831732, "id": 1, "out": 0,
    "peer_id": 2000000107, "text": "кста", "conversation_message_id": 38965,
    "fwd_messages": [], "important": False, "random_id": 0, "attachments":[],
    "is_hidden": False,
}

@pytest.mark.asyncio
async def test_response(app):
    @app.on("vk:message_new")
    async def _(event: MessageNew):
        response_id = await event.response("hey")
        assert response_id == 7347

    await app.start()

    app.dispatch(MessageNew(1, MESSAGE_SOURCE))

    await app.stop()

    found = 0

    for call in app._session.calls:
        if not call[0].endswith("execute"):
            continue

        if 'API.messages.send({"message": "hey", "peer_id": 2000000107' in call[1]["code"]:
            found += 1

    assert found == 1


@pytest.mark.asyncio
async def test_message_new_event(app):
    events = []

    @app.on("vk:message_new")
    async def _(event):
        events.append(event)

        with pytest.raises(AttributeError):
            event.out = True

        assert event.id == 1
        assert event.from_id == 170831732
        assert event.peer_id == 2000000107
        assert event.text == "кста"
        assert not event.important
        assert event.random_id == 0
        assert event.payload == ""
        assert not event.out

    await app.start()

    app.dispatch(MessageNew(1, MESSAGE_SOURCE))

    await app.stop()

    assert len(events) == 1
