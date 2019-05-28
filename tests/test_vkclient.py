# pylint: disable=missing-docstring,protected-access,redefined-outer-name
import pytest
import aiohttp

from vkpore.vkclient import VkClient
from .testing_tools import Session

@pytest.mark.asyncio
async def test_initialization():
    client = VkClient("token", session=Session())

    await client.initialize()

    assert client.group_id == 1
    assert client.group_name == "Group"

    assert client._session.calls == [
        (
            "https://api.vk.com/method/groups.getById",
            {"v": "5.92", "access_token": "token"}
        ),
        (
            "https://api.vk.com/method/groups.setLongPollSettings",
            {
                "v": "5.92", "access_token": "token", "group_id": 1,
                "api_version": "5.92", "enabled": 1
            }
        )
    ]

@pytest.mark.asyncio
async def test_loop_twice():
    client = VkClient("token", session=Session())

    client.start()

    with pytest.raises(RuntimeError):
        client.start()

    await client.stop()

@pytest.mark.asyncio
async def test_request():
    client = VkClient("token", session=Session())

    client.start()

    response = await client.request(
        "messages.send", user_id=1, message="hey",
    )

    assert response == 7347

    assert client._session.calls[0] == (
        "https://api.vk.com/method/execute",
        {
            "v": "5.92", "access_token": "token",
            "code": 'return [API.messages.send({"user_id": 1, "message": "hey"}),];',
        }
    )

    await client.stop()


@pytest.mark.asyncio
async def test_request_without_loop():
    client = VkClient("token", session=Session())

    with pytest.raises(RuntimeError):
        await client.request("method", arg1="arg1")

@pytest.mark.asyncio
async def test_request_fail():
    client = VkClient("token", session=Session(execute_fail=True))

    client.start()

    response = await client.request(
        "messages.send", user_id=1, message="hey",
    )

    assert response is None

    await client.stop()

@pytest.mark.asyncio
async def test_raw_request():
    client = VkClient("token", session=Session())

    response = await client.raw_request(
        "messages.send", user_id=1, message="hey",
    )

    assert response == 7347

    assert client._session.calls == [
        (
            "https://api.vk.com/method/messages.send",
            {"v": "5.92", "access_token": "token", "message": "hey", "user_id": 1},
        ),
    ]

@pytest.mark.asyncio
async def test_exception():
    client = VkClient("token", session=Session(aiohttp.ClientError))

    response = await client.raw_request(
        "messages.send", user_id=1, message="hey",
    )

    assert response is None

@pytest.mark.asyncio
async def test_longpoll():
    client = VkClient("token", session=Session())

    await client.initialize()

    get_updates = client.longpoll()

    client.start()

    updates = await get_updates() + await get_updates()

    assert updates == [
        {"type": "no", "object": 1}, {"type": "no", "object": 2},
        {"type": "no", "object": 3}, {"type": "no", "object": 1},
        {"type": "no", "object": 2}, {"type": "no", "object": 3},
    ]

    await client.stop()

@pytest.mark.asyncio
async def test_longpoll_failed():
    client = VkClient("token", session=Session(longpoll_failed=2))

    await client.initialize()

    get_updates = client.longpoll()

    client.start()

    updates = await get_updates()

    assert updates is None

    await client.stop()

@pytest.mark.asyncio
async def test_longpoll_exception():
    client = VkClient("token", session=Session())

    await client.initialize()

    client._session.exception = aiohttp.ClientError

    get_updates = client.longpoll({"key": "a", "server": "x.x", "ts": 0})

    client.start()

    updates = await get_updates()

    assert updates is None

    await client.stop()
