from typing import Union

from core.config.enum import RedisKey
from core.config.redis import RedisClient

Configurations = Union[RedisClient, RedisKey]
