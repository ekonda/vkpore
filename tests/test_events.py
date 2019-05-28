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

def test_message_data():
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
                    "date": 1557741741, "access_key": "7738f5807780b6537a",
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

    assert message_data.attachments
    assert message_data.attachments[0].type == "photo"
    assert not message_data.attachments[0].content.uploaded_by_group
    assert message_data.attachments[0].content.prepared == \
        "photo87641997_456266978_7738f5807780b6537a"
