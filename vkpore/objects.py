"""Module with vkontakte API objects."""
from typing import Dict, Union, Optional, Tuple
from abc import ABC

from .utils import read_only_properties


SLOTS: Tuple[str, ...] = ()


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
        self.content: Union[
            None, Photo, Video, Audio, Doc, Link, Sticker, Gift, Wall
        ] = None

        if self.type == "photo":
            self.content = Photo(self.content_raw)
        elif self.type == "video":
            self.content = Video(self.content_raw)
        elif self.type == "audio":
            self.content = Audio(self.content_raw)
        elif self.type == "doc":
            self.content = Doc(self.content_raw)
        elif self.type == "link":
            self.content = Link(self.content_raw)
        elif self.type == "sticker":
            self.content = Sticker(self.content_raw)
        elif self.type == "gift":
            self.content = Gift(self.content_raw)
        elif self.type == "wall":
            self.content = Wall(self.content_raw)


SLOTS = (
    "type", "source", "id", "owner_id", "access_key",
)


@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods
class AttachmentContent(ABC):
    """Class for storing information about attachment's content"""

    __slots__ = tuple(SLOTS)

    def __init__(self, _type: str, source: Dict):
        #: Content's type
        self.type: str = _type

        #: ID.
        self.id: int = int(source.get("id", 0))
        #: Owner id.
        self.owner_id: int = int(source.get("owner_id", 0))
        #: Access key if present.
        self.access_key: str = source.get("access_key", "")

        #: Raw source of content
        self.source: Dict = source

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


SLOTS = (
    "album_id", "user_id", "text", "date", "sizes",
)

@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Photo(AttachmentContent):
    """
    Class for storing information about photo in attachment.
    Documentation: https://vk.com/dev/objects/photo
    """

    __slots__ = tuple(SLOTS)

    def __init__(self, source: Dict):
        super().__init__("photo", source)

        #: Album id.
        self.album_id: int = int(source.get("album_id", 0))
        #: Uploader's id (100 if uploaded by group)
        self.user_id: int = int(source.get("user_id", 0))
        #: Description
        self.text: str = source.get("text", "")
        #: Date of adding in Unixtime
        self.date: int = source.get("date", "")
        #: Tuple with photo's sizes
        self.sizes: Tuple[PhotoSize, ...] = tuple(
            PhotoSize(s) for s in source.get("sizes", ())
        )

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


SLOTS = (
    "title", "description", "duration", "date",
    "adding_date", "views", "comments", "player",
    "first_frame", "photo",
)

@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Video(AttachmentContent):
    """
    Class for storing information about photo in attachment.
    https://vk.com/dev/objects/video
    """

    __slots__ = tuple(SLOTS)

    def __init__(self, source: Dict):
        super().__init__("video", source)

        #: Title
        self.title: str = source.get("title", "")
        #: Description
        self.description: str = source.get("description", "")
        #: Duration in seconds
        self.duration: int = int(source.get("duration", 0))
        #: Upload date in unixtime
        self.date: int = int(source.get("date", 0))
        #: Adding date in unixtime
        self.adding_date: int = int(source.get("adding_date", 0))
        #: Views count
        self.views: int = int(source.get("views", 0))
        #: Comments count
        self.comments: int = int(source.get("comments", 0))
        #: Player url
        self.player: str = source.get("player", "")
        #: Url to larges first frame
        self.first_frame: str = (
            source.get("first_frame_1280", "")
            or source.get("first_frame_800", "")
            or source.get("first_frame_640", "")
            or source.get("first_frame_320", "")
            or source.get("first_frame_130", "")
        )
        #: Url to largest cover
        self.photo: str = (
            source.get("photo_1280", "")
            or source.get("photo_800", "")
            or source.get("photo_640", "")
            or source.get("photo_320", "")
            or source.get("photo_130", "")
        )


SLOTS = (
    "artist", "title", "duration", "url", "lyrics_id", "album_id", "genre_id",
    "date", "is_hq", "is_explicit",
)

@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Audio(AttachmentContent):
    """
    Class for storing information about photo in attachment.
    https://vk.com/dev/objects/audio
    """

    __slots__ = tuple(SLOTS)

    def __init__(self, source: Dict):
        super().__init__("audio", source)

        #: Title
        self.title: str = source.get("title", "")
        #: Artist
        self.artist: str = source.get("artist", "")
        #: Duration in seconds
        self.duration: int = int(source.get("duration", 0))
        #: Upload date in unixtime
        self.date: int = int(source.get("date", 0))
        #: Album id
        self.album_id: int = int(source.get("album_id", 0))
        #: Url to .mo3 file
        self.url: str = source.get("url", "")
        #: Lyrics ID if present
        self.lyrics_id: int = int(source.get("lyrics_id", 0))
        #: Genre ID
        self.genre_id: int = int(source.get("genre_id", 0))
        #: High quality flag
        self.is_hq: bool = source.get("is_hq", False)
        #: Explicit flag
        self.is_explicit: bool = source.get("is_explicit", False)


SLOTS = (
    "title", "size", "ext", "url", "date", "file_type", "preview",
)

@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Doc(AttachmentContent):
    """
    Class for storing information about photo in attachment.
    Documentation: https://vk.com/dev/objects/doc
    """

    __slots__ = tuple(SLOTS)

    def __init__(self, source: Dict):
        super().__init__("doc", source)

        #: Title
        self.title: str = source.get("title", "")
        #: Size in bytes
        self.size: int = int(source.get("size", 0))
        #: File extension
        self.ext: str = source.get("ext", "")
        #: Url for downloading
        self.url: str = source.get("url", "")
        #: Upload date in unixtime
        self.date: int = int(source.get("date", 0))
        #: File type
        self.file_type: int = int(source.get("type", 0))
        #: Object with photo, graffiti or audio_message data for displaying
        #: preview for document. It's raw dictionary.
        self.preview: Dict = source.get("preview", {})


SLOTS = (
    "url", "title", "caption", "description", "photo",
)

@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Link(AttachmentContent):
    """
    Class for storing information about photo in attachment.
    Documentation: https://vk.com/dev/objects/link
    """

    __slots__ = tuple(SLOTS)

    def __init__(self, source: Dict):
        super().__init__("link", source)

        #: Url
        self.url: str = source.get("url", "")
        #: Title
        self.title: str = source.get("title", "")
        #: Caption if present
        self.caption: str = source.get("caption", "")
        #: Description
        self.description: str = source.get("description", "")
        #: Preview' if present
        self.photo: Optional[Photo] = None
        if "photo" in source:
            self.photo = Photo(source["photo"])


SLOTS = (
    "product_id", "sticker_id", "images", "images_with_background",
)

@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Sticker(AttachmentContent):
    """
    Class for storing information about photo in attachment.
    Documentation: https://vk.com/dev/objects/sticker
    """

    __slots__ = tuple(SLOTS)

    def __init__(self, source: Dict):
        super().__init__("sticker", source)

        #: Sticker pack's id
        self.product_id: int = int(source.get("product_id", 0))
        #: ID
        self.sticker_id: int = int(source.get("sticker_id", 0))
        #: Tuple with images without background
        self.images: Tuple[StickerSize, ...] = tuple(
            StickerSize(s) for s in source.get("images", ())
        )
        #: Tuple with images with background
        self.images_with_background: Tuple[StickerSize, ...] = tuple(
            StickerSize(s) for s in source.get("images_with_background", ())
        )


@read_only_properties("url", "width", "height")  # pylint: disable=too-few-public-methods
class StickerSize:
    """Class for storing information about sticker image."""

    def __init__(self, source):
        # Url
        self.url: str = source.get("url", "")
        # Width
        self.width: int = int(source.get("width", 0))
        # Height
        self.height: int = int(source.get("height", 0))


SLOTS = (
    "thumb_256", "thumb_96", "thumb_48"
)

@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Gift(AttachmentContent):
    """
    Class for storing information about photo in attachment.
    Documentation: https://vk.com/dev/objects/gift
    """

    __slots__ = tuple(SLOTS)

    def __init__(self, source: Dict):
        super().__init__("gift", source)

        #: Url to image with size 256x256
        self.thumb_256: str = source.get("thumb_256", "")
        #: Url to image with size 96x96
        self.thumb_96: str = source.get("thumb_96", "")
        #: Url to image with size 48x48
        self.thumb_48: str = source.get("thumb_48", "")


SLOTS = (
    "from_id", "date", "text", "reply_owner_id", "reply_post_id",
    "comments_count", "likes_count", "reposts_count", "views_count",
    "post_type", "post_source", "attachments", "copy_history",
)

@read_only_properties(*SLOTS)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Wall(AttachmentContent):
    """
    Class for storing information about photo in attachment.
    Documentation: https://vk.com/dev/objects/post
    """

    __slots__ = SLOTS

    def __init__(self, source: Dict):
        super().__init__("wall", source)

        #: Post author
        self.from_id: int = int(source.get("from_id", 0))
        #: Publication date in unixtime
        self.date: int = int(source.get("date", 0))
        #: Text content
        self.text: str = source.get("text", "")
        #: In post is replying to post, it's owner id
        self.reply_owner_id: int = int(source.get("reply_owner_id", 0))
        #: In post is replying to post, it's post id
        self.reply_post_id: int = int(source.get("reply_post_id", 0))
        #: Comments count
        self.comments_count: int = int(source.get("comments", {}).get("count", 0))
        #: Likes count
        self.likes_count: int = int(source.get("likes", {}).get("count", 0))
        #: Reposts count
        self.reposts_count: int = int(source.get("reposts", {}).get("count", 0))
        #: Views count
        self.views_count: int = int(source.get("views", {}).get("count", 0))
        #: Post type
        self.post_type: str = source.get("post", "")
        #: Raw object with post source
        self.post_source: Dict = source.get("post_source", {})

        #: List of attachments
        self.attachments: Tuple[Attachment, ...] = tuple(
            Attachment(s) for s in source.get("attachments", ())
        )

        #: History of reposts
        self.copy_history: Tuple["Wall", ...] = tuple(
            Wall(s) for s in source.get("copy_history", ())
        )


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
