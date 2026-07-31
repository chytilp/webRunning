from typing import Any

from src.service.redis_client import RedisClient


data: dict[str, Any] = {
    "name": "Roman",
    "age": 25,
    "salary": 37.365,
    "is_alife": True,
}

key: str = "redis-set-object"

def remove_key_if_exists(redis: RedisClient, key: str):
    value = redis.get_object(key)
    if value is not None:
        redis.delete(key)


def test_redis_client_set_object() -> None:
    with RedisClient("localhost", 6379) as client:
        client.ping()
        remove_key_if_exists(client, key)
        client.set_object(key, data)

    # in new context try to read
    with RedisClient("localhost", 6379) as client:
        client.ping()
        new_data = client.get_object(key)
        remove_key_if_exists(client, key)

    assert new_data == data

def test_redis_client_delete() -> None:
    with RedisClient("localhost", 6379) as client:
        client.ping()
        remove_key_if_exists(client, key)
        client.set_object(key, data)

    # in new context try to read
    with RedisClient("localhost", 6379) as client:
        client.ping()
        client.delete(key)
        value: Any | None = client.get_object(key)
        assert value is None