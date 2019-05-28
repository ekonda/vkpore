# Vkpore

[![Build Status](https://travis-ci.com/ekonda/vkpore.svg?branch=master)](https://travis-ci.com/ekonda/vkpore)
[![codecov](https://codecov.io/gh/ekonda/vkpore/branch/master/graph/badge.svg)](https://codecov.io/gh/ekonda/vkpore)
[![Documentation Status](https://readthedocs.org/projects/vkpore/badge/?version=latest)](https://vkpore.readthedocs.io/en/latest/?badge=latest)
[![CodeFactor](https://www.codefactor.io/repository/github/ekonda/vkpore/badge)](https://www.codefactor.io/repository/github/ekonda/vkpore)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/66e342d2507247dcbc5b9a3c7f2fca30)](https://www.codacy.com/app/michaelkrukov/vkpore?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ekonda/vkpore&amp;utm_campaign=Badge_Grade)
[![codebeat badge](https://codebeat.co/badges/709259fe-147c-41da-8df5-bdbe2d89f67f)](https://codebeat.co/projects/github-com-ekonda-vkpore-master)

Asynchronous library for organizing interactions with
[Vkontakte](https://vk.com/dev) api.

## Documentation

Documentation is available [here](https://vkpore.readthedocs.io/).

## Features

- Direct requests to Vkontakte API
- Requests to Vkontakte API using [execute](https://vk.com/dev/execute)
- Straightforward usage and API
- Heavily annotated types
- Extensive testing
- Supports multiple groups at the same time
- Small overhead
- Build on experience and many known use cases

### Supported attachments

You can use these classes from `vkpore.objects` to parse source data into
instances. If you need something not supported by the library, every
instance has `.source` field with raw source data.

- `Sticker` (type: `sticker`)
- `Video` (type: `video`)
- `Photo` (type: `photo`)
- `Audio` (type: `audio`)
- `Link` (type: `link`)
- `Wall` (type: `wall`)
- `Gift` (type: `gift`)
- `Doc` (type: `doc`)

### Supported events

You can use these classes from `vkpore.events` to parse source data into
instances. If you need something not supported by the library, every
instance has `.source` field with raw source data.

- `MessageNew` (type: `message_new`)

## Usage

### Longpoll

You can use class `Vkpore` to create a manager and subscribe callbacks to
events. When the manager receives event, it will call registered callback
for type `vk:<vkontakte-event-name>`. The callback will receive an event
instance through which you can interact with Vkontakte.

To start the manager, just call `.run()` method. If you want to run
manager in backgroudn, you can use use coroutine `.start()`.

#### Example

```py
app = Vkpore(["token"])

@app.on("vk:message_new")
async def _(event: MessageNew):  # Echo callback
    await event.response(event.text)

app.run()
```

### Client

You can use class `VkClient` to perform requests in a loop with `execute`
or directly.

> `VkClient` uses `aiohttp.ClientSession`, so you need to
> clean up before exiting your application, if your don't
> want to see the warnings

#### Example without loop

```py
async def application():
    client = VkClient("token")

    users = await client.raw_request("users.get", user_id=188149294)

    if users:
        print(users[0])

    await client.close_session()

get_event_loop().run_until_complete(application())
```

#### Example with loop

- Use `.request()` to utilize batching with `execute` and respect limits
- Place your calls to `.request()` between `.start()` and `.stop()`

> You still have to close the session

```py
async def application():
    client = VkClient("token")
    client.start()

    # ...

    await client.stop()

get_event_loop().run_until_complete(application())
```

## FAQ

- **Is there plugins?** No. `Vkpore` is a library for aiding in developing
  your solutions with organizing and using Vkontakte API.

- **Is every event is supported?** No. Only a few update types are
  supported with classes at the moment. *But.* You don't have to only use
  classes. You can use `"vk:raw"` for receiving any update types that are
  not supported with classes.

- **Does this library work with user accounts?** No, but actually yes. Only
  groups are supported by `Vkpore` class, but if you pass a user token in
  `VkClient` - it will possibly work fine.

- **Does this library support telegram?** No. It's a library for Vkontakte.
