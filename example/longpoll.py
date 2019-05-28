from sys import argv
from vkpore import Vkpore
from vkpore.events import MessageNew


token = argv[1]

app = Vkpore([token])

@app.on("vk:message_new")
async def _(event: MessageNew):
    await event.response(event.text)

app.run()
