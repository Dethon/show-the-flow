from dependency_injector import containers, providers
from stf.adapters import RedisDataframeCache
from stf.services import DatasetService, ChartService


class Config(containers.DeclarativeContainer):
    config = providers.Configuration()


class Adapters(containers.DeclarativeContainer):
    config = providers.DependenciesContainer()
    cache = providers.Singleton(RedisDataframeCache, config=config.config)


class Services(containers.DeclarativeContainer):
    adapters = providers.DependenciesContainer()
    dataset_service = providers.Factory(DatasetService, cache=adapters.cache)
    chart_service = providers.Factory(ChartService, cache=adapters.cache)


config = Config()
config.config.from_yaml("./config.yml")
services = Services(adapters=Adapters(config=config))
