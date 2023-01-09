import io
import hashlib
import pandas as pd
import redis
from stf.domain.ports import DataframeCache


class RedisDataframeCache(DataframeCache):
    def __init__(self, config) -> None:
        self._redis = redis.StrictRedis.from_url(config["REDIS_URL"])

    def _hash(cls, serialized_obj: bytes) -> str:
        return hashlib.sha512(serialized_obj).hexdigest()

    def add_data(self, data: pd.DataFrame) -> str:
        buffer = io.BytesIO()
        data.to_parquet(buffer, compression="gzip")
        buffer.seek(0)
        df_as_bytes = buffer.read()
        hash_key = self._hash(df_as_bytes)

        self._redis.set(hash_key, df_as_bytes)
        return hash_key

    def get_data(self, key: str) -> pd.DataFrame | None:
        serialized_value = self._redis.get(key)
        if serialized_value is None:
            return None
        return pd.read_parquet(io.BytesIO(serialized_value))

    def remove_data(self, key: str) -> None:
        self._redis.expire(key, 10)
