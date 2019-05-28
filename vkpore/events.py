"""Module with possible events and classes/functions related to that."""

from typing import List, Dict, Callable, Tuple, Awaitable, Optional
from random import random
from abc import ABC
import logging

from .utils import read_only_properties
from .objects import Action, Attachment


Callback = Callable[["Event"], Awaitable]


_SLOTS: Tuple[str, ...] = ()


# ----------------------------------------------------------------------------
# Basic events


@read_only_properties("name", "group_id", "source")
class Event(ABC):
    """Base class for possible events."""

    __slots__ = (
        "_app", "_callbacks", "_callbacks_index",
        "name", "group_id", "source",
    )

    def __init__(self, name: str, group_id: int, source: Dict):
        self._app = None
        self._callbacks: List[Callback] = []
        self._callbacks_index: int = -1

        #: Event's internal name (like "vk:<event's name>")
        self.name: str = name

        #: Event's group id.
        self.group_id = group_id
        #: Raw object of event.
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

    def __init__(self, group_id, source: Dict):
        super().__init__("vk:raw", group_id, source)


_SLOTS = (
    "id", "date", "peer_id", "from_id", "text", "random_id",
    "important", "payload", "out", "attachments", "action", "reply_message",
    "fwd_messages"
)

@read_only_properties(*_SLOTS)  #pylint: disable=too-many-instance-attributes
class MessageData(Event):
    """
    Class for storing data about personal message in vkontakte.
    Documentation: https://vk.com/dev/objects/message
    """

    __slots__ = _SLOTS

    def __init__(self, name, group_id, source: Dict):
        super().__init__(name, group_id, source)

        #: Message id
        self.id: int = source.get("id", 0)
        #: Message date in unixtime
        self.date: int = source.get("date", 0)
        #: Message peer id
        self.peer_id: int = source.get("peer_id", 0)
        #: Message from id
        self.from_id: int = source.get("from_id", 0)
        #: Message text if present
        self.text: str = source.get("text", "")
        #: Message random id
        self.random_id: int = source.get("random_id", 0)
        #: Message important flag
        self.important: bool = source.get("important", False)
        #: Message payload
        self.payload: str = source.get("payload", "")
        #: Message out flag
        self.out: bool = source.get("out", False)

        #: Message action if present
        self.action: Optional["Action"] = None
        if "action" in source:
            self.action = Action(source["action"])

        #: Message reply message if present
        self.reply_message: Optional[MessageData] = None
        if "reply_message" in source:
            self.reply_message = MessageData("", 0, source["reply_message"])

        #: Forwarded messages
        self.fwd_messages: Tuple[MessageData, ...] = tuple(
            MessageData("", 0, s) for s in source.get("fwd_messages", ())
        )

        #: Message attachments
        self.attachments: Tuple[Attachment, ...] = tuple(
            Attachment(s) for s in source.get("attachments", ())
        )

    async def response(self, message: str):
        """Response to channel event was received from."""

        return await self.request(
            "messages.send",
            message=message,
            peer_id=self.peer_id,
            random_id=int(random() * 4294967296) - 2147483648
        )


# ----------------------------------------------------------------------------
# [Vkontakte events](https://vk.com/dev/groups_events)


class MessageNew(MessageData):
    """Vkontakte "message_new" event."""

    def __init__(self, group_id, source: Dict):
        super().__init__("vk:message_new", group_id, source)
