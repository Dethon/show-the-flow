import fakeredis
from stf.adapters import RedisDataframeCache


class FakeRedisDataframeCache(RedisDataframeCache):
    def __init__(self) -> None:
        self._redis = fakeredis.FakeStrictRedis()
