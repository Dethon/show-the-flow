from __future__ import annotations
from typing import Iterable
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from stf.domain.sankey.sankey_components import SankeyComponents, SankeyNodeComponents, SankeyLinkComponents
from stf.domain.dto import SankeyDTO
from stf.domain.utils import links_from_rows


class Sankey:
    def __init__(
        self,
        lnk_df: pd.DataFrame,
        source_col: str = "source",
        target_col: str = "target",
        size_col: str = "amount",
        colorscale: str = "IceFire",
        unit: str | None = None,
        full_label: bool = True,
        x_pos: list[float] | None = None,
        y_pos: list[float] | None = None,
    ) -> None:
        self.lnk_df = lnk_df
        self.data = SankeyComponents.create_from_df(
            lnk_df, colorscale, source_col, target_col, size_col, unit, full_label, x_pos, y_pos
        )
        self.figure = self._create_figure(self.data)

    def update_layout(self, **kwargs) -> None:
        if len(kwargs) == 0:
            return
        self.figure.update_layout(**kwargs)

    def update_traces(self, **kwargs) -> None:
        if len(kwargs) == 0:
            return
        self.figure.update_traces(**kwargs)

    def get_figure(self) -> go.Figure:
        return self.figure

    def show(self) -> None:
        self.figure.show()

    def get_html(self) -> str:
        return self.figure.to_html()

    def _create_nodes(self, node: SankeyNodeComponents) -> dict:
        return dict(
            pad=18,
            thickness=10,
            line=dict(color="black", width=0.5),
            label=node.labels,
            color=node.colors,
            x=node.x_pos,
            y=node.y_pos,
        )

    def _create_links(self, link: SankeyLinkComponents) -> dict:
        return dict(source=link.sources, target=link.targets, value=link.sizes, color=link.colors)

    def _create_figure(self, data: SankeyComponents) -> go.Figure:
        nodes = self._create_nodes(data.nodes)
        links = self._create_links(data.links)
        return go.Figure(data=[go.Sankey(node=nodes, link=links, arrangement="snap")])

    @classmethod
    def from_dto(cls, dto: SankeyDTO) -> Sankey:
        links_df = links_from_rows(dto.dict()["links"])
        snk = cls(links_df, colorscale=dto.colorscale, unit=dto.unit, full_label=dto.full_label)
        snk.update_layout(width=dto.width, height=dto.height)
        return snk
