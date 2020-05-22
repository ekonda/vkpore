"""Module with classes related to interacting with Vkontakte."""

from typing import List, Dict, Union, Awaitable, Optional, Callable
from asyncio import Future, AbstractEventLoop as AEL
import asyncio
import logging
import json

from aiohttp import ClientSession, ClientError

from .utils import wait_with_stopped


class Request(Future):
    """Request in queue for execution."""

    __slots__ = ("method", "arguments")

    def __init__(self, method, arguments):
        super().__init__()

        self.method: str = method
        self.arguments: Dict[str, Union[str, int]] = arguments


class VkClient:  #pylint: disable=too-many-instance-attributes
    """Class for interacting with Vkontakte."""

    def __init__(self, token: str, session: ClientSession = None, loop: AEL = None):
        self._token: str = token
        self._loop: AEL = loop or asyncio.get_event_loop()
        self._session: ClientSession = session or ClientSession()
        self._api_url: str = "https://api.vk.com/method/{method}"
        self._version: str = "5.92"
        self._loop_pause: float = 1 / 19

        self._queue: asyncio.Queue = asyncio.Queue()
        self._running_loop: Optional[Awaitable] = None

        self._stopped: asyncio.Event = asyncio.Event()
        self._stopped.set()

        self._group_id: int = 0
        self._group_name: str = ""

    async def _execute_loop(self):
        stopped = asyncio.Task(self._stopped.wait())

        while True:
            await asyncio.sleep(self._loop_pause)

            request = await wait_with_stopped(self._queue.get(), stopped)

            if request is None:
                break

            requests: List[Request] = [request]

            for _ in range(24):
                try:
                    requests.append(self._queue.get_nowait())
                except asyncio.QueueEmpty:
                    break

            code = ["return ["]

            for request in requests:
                code.append("API.{}({}),".format(
                    request.method,
                    json.dumps(request.arguments, ensure_ascii=False),
                ))

            code.append("];")

            responses = await self.raw_request("execute", code="".join(code))

            if responses is None:
                responses = [False] * len(requests)

            for response, request in zip(responses, requests):
                try:
                    if response is False:
                        request.set_result(None)
                    else:
                        request.set_result(response)
                except asyncio.InvalidStateError:  # pragma: no cover
                    pass

    @property
    def group_id(self):
        """Client's group id"""
        return self._group_id

    @property
    def group_name(self):
        """Client's group name"""
        return self._group_name

    async def initialize(self, enable_longpoll=True):
        """Check token and get information about group."""

        resp = await self.raw_request("groups.getById")

        if not resp:
            raise ValueError("Initialization failed")

        self._group_id = resp[0]["id"]
        self._group_name = resp[0]["name"]

        logging.info(
            'Initialized "%s" [ https://vk.com/club%s ]',
            self.group_name, self.group_id,
        )

        if enable_longpoll:
            await self.raw_request(
                "groups.setLongPollSettings",
                group_id=self._group_id,
                api_version=self._version,
                enabled=1,
            )

    def start(self):
        """
        Start loop for executing requests with `request` method. Loop
        allows usage of batching and `execute` method. Returns awaitable
        with loop. Only one loop cann run for instance of client.
        """

        if self._running_loop:
            raise RuntimeError("Loop already running!")

        self._stopped.clear()

        self._running_loop = asyncio.ensure_future(
            self._execute_loop(), loop=self._loop
        )

        return self._running_loop

    async def stop(self):
        """
        Attempts to stop background loop and waits for it to actually stop.
        """

        self._stopped.set()

        if self._running_loop:
            await self._running_loop
            self._running_loop = None

    async def request(self, method: str, **kwargs):
        """
        Perform a request to method with arguments. Access token and version
        added explicitly, but you can override it with your arguments. Request
        if performed from background loop and is batched in order to use
        `execute` method. Returns response or None if error occured.
        """

        if not self._running_loop:
            raise RuntimeError("Loop for requests is not running!")

        request = Request(method, kwargs)
        await self._queue.put(request)
        return await request

    async def raw_request(self, method: str, **kwargs):
        """
        Perform a request to method with arguments. Access token and version
        added explicitly, but you can override it with your arguments.
        Returns response or None if error occured.
        """

        logging.debug("Request: [%s %s]", method, str(kwargs))

        arguments = {
            "v": self._version,
            "access_token": self._token,
            **{k: v for k, v in kwargs.items() if v is not None}
        }

        url = self._api_url.format(method=method)

        try:
            async with self._session.post(url, data=arguments) as raw_response:
                response = await raw_response.json(content_type=None)

                if not response or response.get("response", None) is None:
                    return None

                return response["response"]
        except (json.JSONDecodeError, ClientError):
            logging.exception("Performing raw request")
            return None

    def longpoll(self, default_longpoll=None) -> Callable[[], Callable[[], List[Dict]]]:
        """
        Return coroutine for receiving updates for current group from
        vkontakte using Bots Longpoll API.
        """

        if default_longpoll is None:
            longpoll: Dict[str, Union[int, str]] = {}
        else:
            longpoll = {**default_longpoll}

        async def refresh():
            """Get new values for longpolling."""

            response = await self.request(
                "groups.getLongPollServer", group_id=self.group_id
            )

            if response is not None:
                longpoll["server"] = response["server"]
                longpoll["key"] = response["key"]
                longpoll["ts"] = response["ts"]

        async def get():
            """Request new updates from Vkontakte."""

            while not longpoll:
                await refresh()

            arguments = {
                "ts": longpoll["ts"],
                "act": "a_check",
                "key": longpoll["key"],
                "wait": 25,
            }

            try:
                post = self._session.post(longpoll["server"], data=arguments)

                async with post as raw_response:
                    response = await raw_response.json(content_type=None)

            except (json.JSONDecodeError, ClientError):
                logging.exception("Longpoll request")
                longpoll.clear()
                return

            if "ts" in response:
                longpoll["ts"] = response["ts"]

            if "failed" in response:
                if response["failed"] != 1:
                    longpoll.clear()
                return

            return response["updates"]

        return get

    async def close_session(self):  # pragma: no cover
        """Close this client's session."""
        if self._session:
            await self._session.close()
