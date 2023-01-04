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
        p_unit_props: dict | None = None,
        input_props: dict | None = None,
    ) -> None:
        self.aio_id = aio_id or self.generate_uuid()
        self.input_id = self.ids.input(self.aio_id)
        self.unit_id = self.ids.unit(self.aio_id)

        p_unit_props = self.add_defaults(p_unit_props or {}, "children", unit)
        input_props = self.add_defaults(input_props or {}, ["placeholder", "value", "type"], [placeholder, value, type])

        input = [dcc.Input(id=self.input_id, className="input", **input_props)]
        if unit:
            input.append(html.P(id=self.unit_id, className="input-unit", **p_unit_props))

        super().__init__(input, className=self.class_name_concat(["input-with-unit", className]))
