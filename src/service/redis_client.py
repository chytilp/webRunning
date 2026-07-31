from __future__ import annotations

import json
from types import TracebackType
from typing import Any

from redis import Redis


class RedisClient:

    def __init__(self, host: str = "localhost", port: int = 6379) -> None:
        self.host: str = host
        self.port: int = port
        self.client: Redis | None = None

    def __enter__(self) -> RedisClient:
        self.client = Redis(
            host=self.host,
            port=self.port,
            db=0  # The default Redis database index
        )
        return self

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        if self.client is not None:
            self.client.close()
            self.client = None

    def ping(self) -> bool:
        return self.client.ping()

    def get(self, key: str) -> Any | None:
        return self.client.get(key)

    def set(self, key: str, value: Any, exp_seconds: int = 3600) -> None:
        self.client.set(key, value, ex=exp_seconds)

    def set_object(self, key: str, value: Any, exp_seconds: int = 3600) -> None:
        # value is json serializable
        serialized: str = json.dumps(value)
        self.client.set(key, serialized, ex=exp_seconds)

    def get_object(self, key: str) -> Any | None:
        data = self.client.get(key)
        if data is None:
            return None
        obj = json.loads(data.decode())
        return obj

    def delete(self, key: str) -> None:
        self.client.delete(key)