from typing import Any, List, Optional, Tuple

from redis import Redis

from . import env


class RedisClient:
    """ """

    __client: Redis
    __instance: "RedisClient" = None

    def __new__(cls) -> "RedisClient":
        """
        Creates new instance of this class
        """

        if not cls.__instance:
            cls.__instance = super(RedisClient, cls).__new__(cls)
            cls.__instance.__client = Redis(
                db=env.REDIS_DB,
                host=env.REDIS_HOST,
                port=env.REDIS_PORT,
                decode_responses=True,
            )

        return cls.__instance

    def client(self) -> Redis:
        """
        Returns `Redis` client instance
        """

        return self.__instance.__client

    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """
        Set a key-value pair in Redis with optional expiration time.
        """

        return self.__client.set(key, value, ex=ex)

    def get(self, key: str) -> Optional[str]:
        """
        Retrieve a value by key from Redis.
        """

        return self.__client.get(key)

    def delete(self, key: str) -> int:
        """
        Delete a key from Redis.
        """

        return self.__client.delete(key)

    def zadd(self, key: str, score: int, member: str) -> bool:
        """
        Add a member to a sorted set with a score.
        """

        return self.__client.zadd(key, {member: score})

    def zincrby(self, key: str, increment: int, member: str) -> float:
        """
        Increment a member's score in the leaderboard.
        """

        return self.__client.zincrby(key, increment, member)

    def zrevrank(self, key: str, member: str) -> Optional[int]:
        """
        Get the rank of a member in descending order.
        """

        rank = self.__client.zrevrank(key, member)
        return rank if rank is not None else None

    def zrevrange(
        self, key: str, start: int, end: int, withscores: bool = True
    ) -> List[Tuple[str, Any]]:
        """
        Get the top members in descending order.
        """

        return self.__client.zrevrange(key, start, end, withscores=withscores)

    def push(self, key: str, value: str) -> int:
        """
        Push a value onto a Redis list (left push).
        """

        return self.__client.lpush(key, value)

    def pop(self, key: str, timeout: Optional[int] = 0) -> Optional[Tuple[str, str]]:
        """
        Blocking pop from the right of the list.
        """

        return self.__client.brpop([key], timeout)

    def close_connection(self) -> None:
        """
        Closes the Redis connection.
        """

        self.__client.close()
