from sys import argv
from asyncio import  get_event_loop
from vkpore import VkClient

token = argv[1]

async def application():
    client = VkClient(token)

    users = await client.raw_request("users.get", user_id=188149294)

    if users:
        print(users[0])

    await client.close_session()

get_event_loop().run_until_complete(application())
