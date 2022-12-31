from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import pandas as pd
import numpy as np
from stf.domain.sankey.utils import concat_columns, get_rgba_colors


@dataclass
class SankeyComponents:
    links: SankeyLinkComponents
    nodes: SankeyNodeComponents

    @classmethod
    def create_from_df(
        cls,
        lnk_df: pd.DataFrame,
        colors: Iterable,
        source_col: str = "source",
        target_col: str = "target",
        size_col: str = "amount",
        unit: str | None = None,
        size_label: bool = True,
    ) -> SankeyComponents:
        nodes = SankeyNodeComponents.create_from_df(lnk_df, colors, source_col, target_col, size_col, unit, size_label)
        links = SankeyLinkComponents.create_from_df(lnk_df, nodes, source_col, target_col, size_col)
        return cls(links=links, nodes=nodes)


@dataclass
class SankeyNodeComponents:
    names: np.ndarray
    sizes: np.ndarray
    labels: np.ndarray
    colors: np.ndarray

    @classmethod
    def create_from_df(
        cls,
        lnk_df: pd.DataFrame,
        colors: Iterable,
        source_col: str = "source",
        target_col: str = "target",
        size_col: str = "amount",
        unit: str | None = None,
        size_in_label: bool = True,
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
            colors=get_rgba_colors(len(nodes_df), colors, opacity=0.5),
        )


@dataclass
class SankeyLinkComponents:
    sources: np.ndarray
    targets: np.ndarray
    sizes: np.ndarray
    colors: np.ndarray

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
        sources = np.array([translator[k] for k in lnk_df[source_col]])
        targets = np.array([translator[k] for k in lnk_df[target_col]])
        sizes = lnk_df[size_col].to_numpy()
        colors = np.array([node_components.colors[i] for i in sources])
        return cls(sources=sources, targets=targets, sizes=sizes, colors=colors)
