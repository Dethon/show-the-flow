import pytest
from dependency_injector import providers
from stf.adapters.fake_redis_chart_data_cache import FakeRedisDataframeCache
from stf.domain.ports import DataframeCache
from stf.dependency_configurator import services


@pytest.fixture
def cache() -> DataframeCache:
    cache = FakeRedisDataframeCache()
    services.adapters.cache.override(providers.Object(cache))
    return cache
