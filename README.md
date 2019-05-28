# vkpore

Library for organizing interactions with [Vkontakte](https://vk.com/) api.

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

## Roadmap

- [_] Documentation
- [_] Continuous integration
- [_] Publish module
- [_] Improve `NewMessage`:
  - [_] Attachments
  - [_] Actions
  - [_] Forwarded messages
- [_] Benchmarks

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
