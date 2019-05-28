# pylint: disable=missing-docstring,protected-access,redefined-outer-name
from async_generator import asynccontextmanager


class Session:
    def __init__(self, exception=None, execute_fail=False, longpoll_failed=0):
        self.calls = []
        self.exception = exception
        self.execute_fail = execute_fail
        self.longpoll_failed = longpoll_failed

    async def close(self):
        pass

    @asynccontextmanager
    async def post(self, url, data):
        self.calls.append((url, data))

        class _response:  # pylint: disable=too-few-public-methods
            @staticmethod
            async def json(**_):
                if self.exception is not None:
                    raise self.exception()

                if url == "x.x":
                    if isinstance(self.longpoll_failed, Exception):
                        raise self.longpoll_failed

                    if self.longpoll_failed:
                        addition = {"failed": self.longpoll_failed}

                    else:
                        addition = {}

                    return {
                        "updates": [
                            {"type": "no", "object": 1},
                            {"type": "no", "object": 2},
                            {"type": "no", "object": 3},
                        ],
                        "ts": 2,
                        **addition,
                    }

                response = None

                if url.endswith("execute") and not self.execute_fail:
                    response = []

                    for part in data["code"].split("API")[1:]:
                        if ".groups.getLongPollServer" in part:
                            response.append({"server": "x.x", "key": "x", "ts": 1})
                        else:
                            response.append(7347)

                elif url.endswith("groups.getById"):
                    response = [{"id": 1, "name": "Group"}]

                elif url.endswith("messages.send"):
                    response = 7347

                elif url.endswith("groups.setLongPollSettings"):
                    response = ""

                return {"response": response}

        yield _response()
