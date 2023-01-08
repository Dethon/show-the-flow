from __future__ import annotations
from dataclasses import dataclass
from typing import Collection
import pandas as pd
from stf.domain.utils import concat_columns
from stf.domain.colors import ColorScale


@dataclass
class SankeyNodeComponents:
    names: Collection[str]
    sizes: Collection[float]
    labels: Collection[str]
    colors: Collection[str]
    x_pos: Collection[float] | None = None
    y_pos: Collection[float] | None = None

    @classmethod
    def create_from_df(
        cls,
        lnk_df: pd.DataFrame,
        colorscale: str,
        source_col: str = "source",
        target_col: str = "target",
        size_col: str = "amount",
        unit: str | None = None,
        size_in_label: bool = True,
        x_pos: Collection[float] | None = None,
        y_pos: Collection[float] | None = None,
    ) -> SankeyNodeComponents:
        unit = "" if unit is None else unit
        nname_col = "name"
        cat_cols = [nname_col, size_col] if size_in_label else [nname_col]
        nodes_df = (
            pd.concat(
                [
                    lnk_df.groupby(source_col).sum(numeric_only=True).reset_index(names=nname_col),
                    lnk_df.groupby(target_col).sum(numeric_only=True).reset_index(names=nname_col),
                ]
            )
            .groupby(nname_col)
            .max()
            .reset_index()
        )

        return cls(
            names=nodes_df[nname_col].to_numpy(),
            sizes=nodes_df[size_col].to_numpy(),
            labels=concat_columns(nodes_df, *cat_cols, sep=": ") + unit,
            colors=ColorScale.get_rgba(colorscale, len(nodes_df), opacity=0.5),
            x_pos=x_pos,
            y_pos=y_pos,
        )


@dataclass
class SankeyLinkComponents:
    sources: Collection[int]
    targets: Collection[int]
    sizes: Collection[float]
    colors: Collection[str]

    @classmethod
    def create_from_df(
        cls,
        lnk_df: pd.DataFrame,
        node_components: SankeyNodeComponents,
        source_col: str = "source",
        target_col: str = "target",
        size_col: str = "amount",
    ) -> SankeyLinkComponents:
        translator = {name: idx for idx, name in enumerate(node_components.names)}
        sources = [translator[k] for k in lnk_df[source_col]]
        targets = [translator[k] for k in lnk_df[target_col]]
        sizes = lnk_df[size_col].to_numpy()
        colors = list(node_components.colors)
        colors = [colors[i] for i in sources]
        return cls(sources=sources, targets=targets, sizes=sizes, colors=colors)


@dataclass
class SankeyComponents:
    links: SankeyLinkComponents
    nodes: SankeyNodeComponents

    @classmethod
    def create_from_df(
        cls,
        lnk_df: pd.DataFrame,
        colorscale: str,
        source_col: str = "source",
        target_col: str = "target",
        size_col: str = "amount",
        unit: str | None = None,
        size_label: bool = True,
        x_pos: Collection[float] | None = None,
        y_pos: Collection[float] | None = None,
    ) -> SankeyComponents:
        nodes = SankeyNodeComponents.create_from_df(
            lnk_df, colorscale, source_col, target_col, size_col, unit, size_label, x_pos, y_pos
        )
        links = SankeyLinkComponents.create_from_df(lnk_df, nodes, source_col, target_col, size_col)
        return cls(links=links, nodes=nodes)
