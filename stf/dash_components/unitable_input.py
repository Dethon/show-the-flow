from __future__ import annotations
from typing import Any
from dash import html, dcc
from stf.dash_components.base_component import BaseComponent


class UnitableInput(BaseComponent):
    class ids:
        input = lambda aio_id: {"component": "UnitableInput", "subcomponent": "input", "aio_id": aio_id}
        unit = lambda aio_id: {"component": "UnitableInput", "subcomponent": "unit", "aio_id": aio_id}

    def __init__(
        self,
        unit: str | None = None,
        value: Any | None = None,
        placeholder: str | None = None,
        type: str | None = None,
        aio_id: str | None = None,
        className: str | None = None,
        **input_props,
    ) -> None:
        self.aio_id = aio_id or self.generate_uuid()
        self.input_id = self.ids.input(self.aio_id)
        self.unit_id = self.ids.unit(self.aio_id)

        input_props = self.add_defaults(input_props or {}, {})
        input_props["placeholder"] = placeholder
        input_props["value"] = value
        input_props["type"] = type

        input_component = [dcc.Input(id=self.input_id, className="input", **input_props)]
        if unit:
            input_component.append(html.P(id=self.unit_id, className="input-unit", children=unit))

        super().__init__(input_component, className=self.class_name_concat(["input-with-unit", className]))
