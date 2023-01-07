from __future__ import annotations
from typing import Type
from dash import html
from dash.development.base_component import Component
from stf.dash_components.base_component import BaseComponent


class LabeledInput(BaseComponent):
    class ids:
        label = lambda aio_id: {"component": "LabeledInput", "subcomponent": "label", "aio_id": aio_id}
        component = lambda aio_id: {"component": "LabeledInput", "subcomponent": "component", "aio_id": aio_id}

    def __init__(
        self,
        component: Type[Component],
        label: str,
        aio_id: str | None = None,
        className: str | None = "",
        p_label_props: dict | None = None,
        **kwargs,
    ) -> None:
        self.aio_id = aio_id or self.generate_uuid()
        self.label_id = self.ids.label(self.aio_id)
        self.component_id = self.ids.component(self.aio_id)
        try:
            self.component = component(aio_id=self.aio_id, **kwargs)
        except TypeError:
            self.component = component(id=self.aio_id, **kwargs)
        p_label_props = self.add_defaults(p_label_props or {}, {})
        p_label_props["children"] = label

        super().__init__(
            [html.P(id=self.label_id, className="input-label", **p_label_props), self.component],
            className=self.class_name_concat(["labeled-input", className]),
        )
