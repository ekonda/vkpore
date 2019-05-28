"""Module with possible events and classes/functions related to that."""

from typing import List, Callable, Awaitable
from random import random
from abc import ABC
import logging


Callback = Callable[["Event"], Awaitable]


# ----------------------------------------------------------------------------
# Helpers


EVENT_FIELDS = ("name", "group_id", "source",)
MESSAGE_DATA_FIELDS = (
    "id", "date", "peer_id", "from_id", "text", "random_id",
    "important", "payload", "out",
)


class _Base(ABC):  # pylint: disable=too-few-public-methods,invalid-name
    __slots__ = [
        # Event
        "_app", "_callbacks", "_callbacks_index", *EVENT_FIELDS,

        # MessageData
        *MESSAGE_DATA_FIELDS,
    ]


def read_only_properties(*attrs):
    """Make passed attributes read-only"""
    def decorator(cls):
        class _Class(cls):  # pylint: disable=too-few-public-methods
            def __setattr__(self, name, value):
                if name in attrs and getattr(self, name, None) is not None:
                    raise AttributeError("Can't modify '{}'".format(name))
                super().__setattr__(name, value)
        return _Class
    return decorator


# ----------------------------------------------------------------------------
# Basic events


@read_only_properties(*EVENT_FIELDS)
class Event(_Base, ABC):
    """Base class for possible events."""

    def __init__(self, group_id, source):
        self._app: "Vkpore" = None
        self._callbacks: List[Callback] = []
        self._callbacks_index: int = -1

        self.name = None

        self.group_id = group_id
        self.source = source

    def __str__(self):  # pragma: no cover
        return "<{}[{}] from {}>".format(
            self.__class__.__name__, self.name, self.group_id,
        )

    def initialize(self, app, callbacks: List[Callback]):
        """Set app amd callbacks that will process this event."""
        self._app = app
        self._callbacks = callbacks

    async def request(self, method, **kwargs):
        """Proxy for VkClient's `request`."""

        return await self._app.get_client(self.group_id).request(method, **kwargs)

    async def next(self):
        """Call next callback from the list."""

        self._callbacks_index += 1

        try:
            await self._callbacks[self._callbacks_index](self)
        except Exception:
            logging.exception("Callback for update")
            raise


class EventRaw(Event):
    """Raw event from vkontakte. Used for passing unknown events."""
    def __init__(self, group_id, source):
        super().__init__(group_id, source)
        self.name = "vk:raw"

# ----------------------------------------------------------------------------
# [Vkontakte events](https://vk.com/dev/groups_events)


@read_only_properties(*MESSAGE_DATA_FIELDS)  # #pylint: disable=too-many-instance-attributes
class EventWithMessageData(Event):
    """Class for storing data about personal message in vkontakte."""

    def __init__(self, group_id, source):
        super().__init__(group_id, source)

        self.id: int = source.get("id", 0)
        self.date: int = source.get("date", 0)
        self.peer_id: int = source.get("peer_id", 0)
        self.from_id: int = source.get("from_id", 0)
        self.text: str = source.get("text")
        self.random_id: int = source.get("random_id", 0)
        self.important: bool = source.get("important", False)
        self.payload: str = source.get("payload", "")
        self.out: bool = source.get("out", False)

        # TODO: Attachments, actions, forwarded

    async def response(self, message: str):
        """Response to channel event was received from."""

        return await self.request(
            "messages.send",
            message=message,
            peer_id=self.peer_id,
            random_id=int(random() * 4294967296) - 2147483648
        )


class MessageNew(EventWithMessageData):
    """Vkontakte "message_new" event."""

    def __init__(self, group_id, source):
        super().__init__(group_id, source)

        self.name = "vk:message_new"
