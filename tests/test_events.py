# pylint: disable=missing-docstring,protected-access,redefined-outer-name
import pytest

from vkpore.events import Event, MessageData

@pytest.mark.asyncio
async def test_initialization():
    event = Event("", 1, {})

    async def bad_callback(event):
        raise RuntimeError

    event.initialize(None, [bad_callback])

    with pytest.raises(RuntimeError):
        await event.next()

def test_message_data_with_all_attachments():
    message_data = MessageData("name", 7, {
        "date": 1559038192, "from_id": 87641997, "id": 0, "out": 1,
        "peer_id": 87641997, "text": "Hi", "conversation_message_id": 5065,
        "important": False, "random_id": 1400449560, "is_hidden": False,
        "action": {
            "type": "chat_title_update",
            "text": "высокоинтеллектуальная укороченная"
        },
        "fwd_messages": [
            {
                "date": 1558817411,
                "from_id": 87641997,
                "text": "Hello",
                "attachments": [],
                "conversation_message_id": 5061,
                "peer_id": 87641997,
                "id": 1336352
            }
        ],
        "attachments": [
            {
                "type": "photo",
                "photo": {
                    "id": 456266978, "album_id": -15, "text":"",
                    "date": 1557741741, "access_key": "7738f58sd80b6537a",
                    "owner_id": 87641997, "sizes":[
                        {"type": "m", "url": "xx1", "width": 130, "height": 73},
                        {"type": "o", "url": "xx2", "width": 130, "height": 87},
                        {"type": "p", "url": "xx3", "width": 200, "height": 133},
                        {"type": "q", "url": "xx4", "width": 320, "height": 213},
                        {"type": "r", "url": "xx5", "width": 512, "height": 340},
                        {"type": "s", "url": "xx6", "width": 75, "height": 42},
                        {"type": "x", "url": "xx7", "width": 604, "height": 340},
                        {"type": "y", "url": "xx8", "width": 807, "height": 454},
                        {"type": "z", "url": "xx9", "width": 1080, "height": 607},
                    ]
                }
            },
            {
                "type": "video",
                "video": {
                    "id": 456239964, "owner_id": 87641997, "title": "ay",
                    "duration": 12, "description": "", "date": 1546723675,
                    "comments": 1, "views": 33, "width": 1920, "height": 1080,
                    "photo_130": "xx1", "photo_320": "xx2",
                    "photo_800": "xx3", "photo_1280": "xx4",
                    "first_frame_320": "yy1", "first_frame_160": "yy2",
                    "first_frame_130": "yy3", "first_frame_1280": "yy4",
                    "first_frame_800": "yy5",
                    "is_favorite": False, "access_key": "5c14aasdf06f304c18e7",
                    "can_edit": 1, "can_add": 1
                }
            },
            {
                "type": "audio",
                "audio": {
                    "id": 456243266, "owner_id": 87641997, "artist": "cassimm",
                    "title": "never mind", "duration": 413, "date": 1559053423,
                    "url": "xxx", "genre_id": 5, "is_hq": True,
                    "track_code": "8a59a899qbGJ-6ij6CS0BBNJIB0",
                    "is_explicit": False
                }
            },
            {
                "type": "doc",
                "doc": {
                    "id": 505630202, "owner_id": 87641997,
                    "title": "ari",
                    "size": 67920, "ext": "pdf", "url": "xxx",
                    "date": 1558972877, "type": 1,
                    "access_key": "72sdf5df6casdad0466"
                }
            },
            {
                "type": "link",
                "link": {
                    "url": "https://www.michaelkrukov.ru/",
                    "title": "Michael Krukov", "caption": "michaelkrukov.ru",
                    "description": "Developer and a good person",
                    "is_favorite": False,
                    "photo": {
                        "id": 456272380, "album_id": -25, "text": "",
                        "owner_id": 2000052311, "date": 1559064851,
                        "sizes": [
                            {"type": "s", "url": "xxx", "width": 75, "height": 33},
                            {"type": "m", "url": "xxx", "width": 130, "height": 58},
                            {"type": "x", "url": "xxx", "width": 604, "height": 270},
                            {"type": "y", "url": "xxx", "width": 765, "height": 342},
                            {"type": "o", "url": "xxx", "width": 130, "height": 87},
                            {"type": "p", "url": "xxx", "width": 200, "height": 133},
                            {"type": "q", "url": "xxx", "width": 320, "height": 213},
                            {"type": "r", "url": "xxx", "width": 510, "height": 340},
                            {"type": "l", "url": "xxx", "width": 537, "height": 240}
                        ],
                    },
                }
            },
            {
                "type": "sticker",
                "sticker": {
                    "product_id": 281, "sticker_id": 9068,
                    "images": [
                        {"url": "xxx", "width": 64, "height": 64},
                        {"url": "xxx", "width": 128, "height": 128},
                        {"url": "xxx", "width": 256, "height": 256},
                    ],
                    "images_with_background": [
                        {"url": "yyy", "width": 64, "height": 64},
                        {"url": "yyy", "width": 128, "height": 128},
                        {"url": "yyy", "width": 256, "height": 256},
                    ]
                }
            },
            {
                "type": "gift",
                "gift": {"id": 1, "thumb_256": "xxx"}
            },
            {
                "type": "wall",
                "wall": {
                    "id": 24383, "from_id": -83038692, "to_id": -83038692,
                    "date": 1559066406, "post_type": "post",
                    "is_favorite": False, "access_key": "ffd2dbdfs843f66a81",
                    "text": "#koreanmodel #KimShinYeong Kim Shin Yeong",
                    "marked_as_ads": 0, "post_source": {"type": "vk"},
                    "attachments": [
                        {
                            "type": "photo",
                            "photo": {
                                "id": 456268179, "album_id": -7, "text": "",
                                "owner_id": -83038692, "user_id": 100,
                                "date": 1559060751,
                                "access_key": "638df279e16269s124",
                                "sizes": [
                                    {
                                        "type": "z", "url": "xxx", "width": 723, "height": 1080
                                    }
                                ],
                            }
                        }
                    ],
                    "comments": {
                        "count": 0, "can_post": 1, "groups_can_post": True
                    },
                    "likes": {
                        "count": 10, "user_likes": 0, "can_like": 1, "can_publish": 1
                    },
                    "reposts": {
                        "count": 0, "user_reposted": 0
                    },
                    "views": {
                        "count": 161
                    },
                    "copy_history": [{
                        "id": 46592, "owner_id": -140849182,
                        "from_id": -140849182, "date": 1559057400,
                        "post_type": "post", "text": "Model: jeong.woo.joo",
                        "attachments": [
                            {
                                "type": "photo",
                                "photo": {
                                    "id": 456268179, "album_id": -7, "text": "",
                                    "owner_id": -83038692, "user_id": 100,
                                    "date": 1559060751,
                                    "access_key": "638df279e16269s124",
                                    "sizes": [
                                        {
                                            "type": "z", "url": "xxx", "width": 723, "height": 1080
                                        }
                                    ],
                                }
                            }
                        ],
                        "post_source": {
                            "type": "vk"
                        }
                    }]
                }
            }
        ],
        "reply_message": {
            "date": 1558817411, "from_id": 87641997, "text": "Wes Anderson",
            "attachments": [], "conversation_message_id": 5061,
            "peer_id": 87641997, "id": 1336352
        }
    })

    assert message_data.name == "name"

    assert message_data.text == "Hi"

    assert message_data.reply_message
    assert message_data.reply_message.text == "Wes Anderson"

    assert message_data.fwd_messages
    assert message_data.fwd_messages[0].text == "Hello"

    assert message_data.action
    assert message_data.action.type == "chat_title_update"
    assert message_data.action.text == "высокоинтеллектуальная укороченная"

    assert len(message_data.attachments) == 8

    attachment = message_data.attachments[0]
    assert attachment.type == "photo"
    assert not attachment.content.uploaded_by_group
    assert attachment.content.prepared == \
        "photo87641997_456266978_7738f58sd80b6537a"

    attachment = message_data.attachments[1]
    assert attachment.type == "video"
    assert attachment.content.first_frame == "yy4"
    assert attachment.content.photo == "xx4"

    attachment = message_data.attachments[2]
    assert attachment.type == "audio"
    assert attachment.content.title == "never mind"
    assert attachment.content.artist == "cassimm"
    assert not attachment.content.is_explicit

    attachment = message_data.attachments[3]
    assert attachment.type == "doc"
    assert attachment.content.title == "ari"
    assert attachment.content.url == "xxx"

    attachment = message_data.attachments[4]
    assert attachment.type == "link"
    assert attachment.content.title == "Michael Krukov"
    assert attachment.content.photo.id == 456272380

    attachment = message_data.attachments[5]
    assert attachment.type == "sticker"
    assert attachment.content.sticker_id == 9068
    assert len(attachment.content.images) == 3
    assert attachment.content.images_with_background[0].url == "yyy"

    attachment = message_data.attachments[6]
    assert attachment.type == "gift"
    assert attachment.content.id == 1

    attachment = message_data.attachments[7]
    assert attachment.type == "wall"
    assert attachment.content.id == 24383
    assert attachment.content.attachments[0].content.id == 456268179
    assert attachment.content.likes_count == 10
    assert attachment.content.copy_history[0].type == "wall"
    assert attachment.content.copy_history[0].id == 46592
    assert attachment.content.copy_history[0].attachments[0].content.id == 456268179
