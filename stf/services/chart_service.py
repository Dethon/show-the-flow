from stf.domain import Sankey, SankeyDTO
from stf.domain.ports import DataframeCache


class ChartService:
    def __init__(self, cache: DataframeCache) -> None:
        self.cache = cache

    def get_sankey_html_from_dto(self, dto: SankeyDTO) -> str:
        sankey = Sankey.from_dto(dto)
        return sankey.get_html()

    def get_sankey_from_cache(self, key: str, **kwargs) -> Sankey:
        links = self.cache.get_data(key)
        return Sankey(links, **kwargs)
