from typing import cast, Any

from src.service.redis_client import RedisClient


class AppCache:
    def __init__(self, route: str) -> None:
        self.route: str = route
        self.keys: dict[str, str] = {
            "default_sections": f"{self.route}#default_sections",
            "default_aggregations": f"{self.route}#default_aggregations",
        }

    @staticmethod
    def _get_object(key: str) -> Any | None:
        with RedisClient() as client:
            result = client.get_object(key)
            if result is None:
                return None
            return result

    @staticmethod
    def _set_object(key: str, value: Any) -> None:
        with RedisClient() as client:
            client.set_object(key, value)

    def get_default_sections(self) -> list[str] | None:
        result = self._get_object(self.keys["default_sections"])
        if result is not None:
            return cast(list[str], result)
        return None

    def set_default_sections(self, sections: list[str]) -> None:
        self._set_object(self.keys["default_sections"], sections)

    def get_default_aggregations(self) -> list[str] | None:
        result = self._get_object(self.keys["default_aggregations"])
        if result is not None:
            return cast(list[str], result)
        return None

    def set_default_aggregations(self, aggregations: list[str]) -> None:
        self._set_object(self.keys["default_aggregations"], aggregations)
