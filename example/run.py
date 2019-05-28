"""
Example "echo" application with Vkpore.
"""

from sys import argv

from vkpore import Vkpore
from vkpore.events import MessageNew


app = Vkpore([argv[1]])

@app.on("vk:message_new")
async def _(event: MessageNew):
    await event.response(event.text)

app.run()
