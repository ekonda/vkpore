"""Module with possible events and classes/functions related to that."""

from typing import List, Dict, Callable, Tuple, Awaitable, Optional, Union
from random import random
from abc import ABC
import logging


Callback = Callable[["Event"], Awaitable]


# ----------------------------------------------------------------------------
# Helpers


_SLOTS: Tuple[str, ...] = ()


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

# ----------------------------------------------------------------------------
# [Vkontakte objcet](https://vk.com/dev)


@read_only_properties("type", "content")  # pylint: disable=too-few-public-methods
class Attachment:
    """Class for storing information about attachment."""

    __slots__ = ("type", "content", "content_raw",)

    def __init__(self, source: Dict):
        #: Attachment type.
        self.type: str = source.get("type", "")
        #: Raw object.
        self.content_raw: Dict = source.get(self.type, {})
        #: Supported attachment content class or None.
        self.content: Union[None, Photo] = None

        if self.type == "photo":
            self.content = Photo(self.content_raw)

@read_only_properties("type")  # pylint: disable=too-few-public-methods
class AttachmentContent(ABC):
    """Class for storing information about attachment's content"""

    def __init__(self, _type: str):
        #: Content's type
        self.type: str = _type


_SLOTS = (
    "id", "album_id", "owner_id", "user_id", "text",
    "date", "sizes", "type", "access_key",
)

@read_only_properties(*_SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Photo(AttachmentContent):
    """Class for storing information about photo in attachment."""

    __slots__ = _SLOTS

    def __init__(self, source: Dict):
        super().__init__("photo")

        #: Photo id.
        self.id: int = int(source.get("id", 0))
        #: Photo's album id.
        self.album_id: int = int(source.get("album_id", 0))
        #: Photo's owner id.
        self.owner_id: int = int(source.get("owner_id", 0))
        #: Photo's access_key if present.
        self.access_key: str = source.get("access_key", "")
        #: Uploader's id (100 if uploaded by group)
        self.user_id: int = int(source.get("user_id", 0))
        #: Photo's description
        self.text: str = source.get("text", "")
        #: Date of adding in Unixtime
        self.date: int = source.get("date", "")
        #: Tuple with photo's sizes
        self.sizes: Tuple[PhotoSize, ...] = tuple(
            PhotoSize(s) for s in source.get("sizes", ())
        )

    @property
    def prepared(self) -> str:
        """
        Return string in format "<type><owner_id>_<media_id>".
        If attachment has "access_key" fields - it will be properly appended.
        """
        template = "{}{}_{}"

        if self.access_key:
            template = "{}{}_{}_" + self.access_key

        return template.format(self.type, self.owner_id, self.id)

    @property
    def uploaded_by_group(self) -> bool:
        """Return True if photo was uploaded by user."""
        return self.user_id == 100


@read_only_properties("type", "url", "width", "height")  # pylint: disable=too-few-public-methods
class PhotoSize:
    """
    Class for string information about photo size. Documentation:
    https://vk.com/dev/photo_sizes
    """

    __slots__ = ("type", "url", "width", "height")

    def __init__(self, source: Dict):
        #: Size type
        self.type = source.get("type", "")
        #: Image url
        self.url = source.get("url", "")
        #: Image width
        self.width = int(source.get("width", 0))
        #: Image height
        self.height = int(source.get("height", 0))


@read_only_properties("type", "member_id", "text", "email", "photo")  # pylint: disable=too-few-public-methods
class Action:
    """Class for storing information about action in "message_new" event."""

    __slots__ = ("type", "member_id", "text", "email", "photo")

    def __init__(self, source: Dict):
        #: Action type
        self.type: str = source.get("type", "")
        #: Member id if action related to users
        self.member_id: int = int(source.get("member_id", 0))
        #: New title
        self.text: str = source.get("text", "")
        #: Invited person's email (if memeber_id < 0)
        self.email: str = source.get("email", "")
        #: Three sizes of new cover
        self.photo: Dict[str, str] = source.get("photo", {})


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
