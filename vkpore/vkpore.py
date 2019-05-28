"""Module with core class for organizing event flow."""

from typing import List, Dict, Awaitable, Optional, Iterable, Tuple
from random import choice
from asyncio import AbstractEventLoop as AEL
import asyncio
import logging

from aiohttp import ClientSession

from .vkclient import VkClient
from .events import Event, Callback, MessageNew, EventRaw
from .utils import wait_with_stopped


class Vkpore():
    """
    Class for receiving events, calling methods, callback registration
    and execution. You can specify loop and session to use.
    """

    def __init__(self, tokens: Iterable[str], loop: AEL = None,
                 session: ClientSession = None):
        self._loop: AEL = loop or asyncio.get_event_loop()
        self._callbacks: Dict[str, List[Callback]] = {}
        self._futures: List[asyncio.Future] = []

        self._tokens: Tuple[str, ...] = tuple(tokens)
        self._clients: Dict[int, List[VkClient]] = {}

        self._stopped: asyncio.Event = asyncio.Event()
        self._stopped.set()

        self._session: Optional[ClientSession] = session

    def get_client(self, group_id):
        """Return random client for specified group_id."""

        clients = self._clients.get(group_id)

        if not clients:
            return None

        return choice(clients)

    @staticmethod
    def _get_event_class(update_type):  # pragma: no cover
        if update_type == "message_new":
            return MessageNew

        return EventRaw

    async def _longpoll_loop(self, group_id):
        get_updates = self.get_client(group_id).longpoll()

        stopped = asyncio.Task(self._stopped.wait())

        while True:
            updates = await wait_with_stopped(get_updates(), stopped)

            if updates is None:
                break

            for update in updates:
                event_class = self._get_event_class(update["type"])

                self.dispatch(event_class(group_id, update["object"]))

    async def start(self):
        """Start application related loops and perform initializations."""

        if self._session is None:
            self._session = ClientSession()

        # Create and inititalize clients
        for token in self._tokens:
            client = VkClient(token, self._session, self._loop)

            await client.initialize()

            if client.group_id not in self._clients:
                self._clients[client.group_id] = []

            self._clients[client.group_id].append(client)

        # Application not is considered running
        self._stopped.clear()

        # Create and start loops for receiving updates for groups
        for group_id in self._clients:
            self._futures.append(
                asyncio.ensure_future(
                    self._longpoll_loop(group_id),
                    loop=self._loop
                )
            )

        # Start execute loops for clients
        for clients in self._clients.values():
            for client in clients:
                client.start()

        logging.info("Started")

    async def stop(self):
        """
        Stop client loops, wait for all tasks to complete and close
        sessions.
        """

        logging.info("Stopping")

        self._stopped.set()

        # Wait for running callbacks to stop
        await asyncio.gather(*self._futures)

        # Wait for running loops to stop
        tasks = []

        for group in self._clients.values():
            for client in group:
                tasks.append(client.stop())

        await asyncio.gather(*tasks)

        # Close session
        if self._session:
            await self._session.close()

        logging.info("Stopped")

    def on(self, event: str):
        """Return decorator for subscribing callback to event."""

        def decorator(function: Callback):
            if event not in self._callbacks:
                self._callbacks[event] = []

            self._callbacks[event].append(function)

        return decorator

    def dispatch(self, event: Event):
        """Call callbacks for event."""

        callbacks = self._callbacks.get(event.name)

        if not callbacks or self._stopped.is_set():
            return None

        event.initialize(self, callbacks)

        future = asyncio.ensure_future(event.next(), loop=self._loop)

        self._futures.append(future)

        logging.debug("Dispatched event: %s", event)

        return future

    def run_until_complete(self, awaitable: Awaitable):  # pragma: no cover
        """Run specified awaitable in application's loop."""
        self._loop.run_until_complete(awaitable)

    def run(self):  # pragma: no cover
        """Run application and stop on KeyboardInterrupt."""
        try:
            self._loop.run_until_complete(self.start())
            self._loop.run_forever()
        except KeyboardInterrupt:
            self.run_until_complete(self.stop())
