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

## Example

```py
app = Vkpore(["token"])

@app.on("vk:message_new")
async def _(event: MessageNew):  # Echo callback
    await event.response(event.text)

app.run()
```

## FAQ

- **Is there plugins?** No. `Vkpore` is a library for aiding in developing
  your solutions with organizing and using vkontakte API.

- **Is every event is supported?** No. Only few update types are supported
  with classes at the moment. *But.* You don't have to only use classes.
  You can user `"vk:raw"` for receiving any update types that is not
  supported with classes.

- **Does this library work with user accounts?** No, but actually yes. Only
  groups are supported by `Vkpore` class, but if you pass a user token in
  `VkClient` - it will possibly work fine.

- **Does this library support telegram?** No. It's library for vkontakte.

## Roadmap

- [x] Documentation
- [x] Continuous integration
- [x] Publish module
- [x] Improve `NewMessage`:
  - [x] Attachments
  - [x] Actions
  - [x] Forwarded messages
- [_] Improve `Attachment`:
  - [_] Video
  - [_] Audio
  - [_] Doc
  - [_] Link
  - [_] MarketAlbum
  - [_] Wall
  - [_] WallReply
  - [_] Sticker
  - [_] Gift
- [_] Benchmarks
