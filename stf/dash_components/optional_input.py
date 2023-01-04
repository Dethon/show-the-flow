from __future__ import annotations
from typing import Any
from dash import dcc, Output, Input, callback
from stf.dash_components.base_component import BaseComponent
from stf.dash_components.unitable_input import UnitableInput


class OptionalInput(BaseComponent):
    class ids:
        checklist = lambda aio_id: {"component": "OptionalInput", "subcomponent": "checklist", "aio_id": aio_id}
        input = lambda aio_id: {"component": "OptionalInput", "subcomponent": "input", "aio_id": aio_id}

    def __init__(
        self,
        unit: str | None = None,
        value: Any | None = None,
        placeholder: str | None = None,
        type: str | None = None,
        aio_id: str | None = None,
        className: str | None = None,
        check_props: dict | None = None,
        input_props: dict | None = None,
        p_unit_props: dict | None = None,
    ) -> None:
        self.aio_id = aio_id or self.generate_uuid()
        self.unitable_input_id = self.ids.input(self.aio_id)
        self.check_id = self.ids.checklist(self.aio_id)
        self.input = UnitableInput(
            unit=unit,
            value=value,
            placeholder=placeholder,
            type=type,
            p_unit_props=p_unit_props,
            input_props=input_props,
        )
        self.input_id = self.input.input_id

        super().__init__(
            [dcc.Checklist(id=self.check_id, className="check", options=[{"": 1}], **(check_props or {})), self.input],
            className=self.class_name_concat(["optional-input", className]),
        )

        @callback(Output(self.input_id, "value"), Output(self.input_id, "disabled"), Input(self.check_id, "value"))
        def mutate_input(check) -> tuple[str, bool]:
            return "", not check
