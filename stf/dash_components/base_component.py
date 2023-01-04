from __future__ import annotations
import uuid
from typing import Any, Iterable
from dash import html
from stf.domain.utils import as_list


class BaseComponent(html.Div):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def class_name_concat(self, classes: Iterable[str | None], sep: str = " ") -> str:
        mapped_classes = [c or "" for c in classes]
        return sep.join(mapped_classes)

    def generate_uuid(self) -> str:
        return str(uuid.uuid4())

    def add_defaults(self, prop_dict: dict, prop: str | Iterable[str], default: Any | Iterable) -> dict:
        result = prop_dict.copy()
        for prop, default in zip(as_list(prop), as_list(default)):
            if prop not in result:
                result[prop] = default
        return result
