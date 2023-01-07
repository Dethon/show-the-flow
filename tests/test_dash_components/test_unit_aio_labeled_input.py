from dash import dcc, html
from stf.dash_components import LabeledInput, UnitableInput
from tests.utils.constants import UUID_LENGTH


def test_component_structure_general():
    aio_id, className, unit, label, compo = "test_id", "test", "px", "test-label", UnitableInput
    component = LabeledInput(component=compo, label=label, aio_id=aio_id, className=className, unit=unit)

    label_component = component.children[0]
    input_component = component.children[1]

    assert f"labeled-input {className}" == component.className
    assert len(component.children) == 2
    assert isinstance(label_component, html.P)
    assert isinstance(input_component, compo)
    assert isinstance(label_component.children, str)
    assert label_component.children == label
    assert label_component.className == "input-label"
    assert label_component.id == LabeledInput.ids.label(aio_id) == component.label_id

    assert input_component.children[1].children == unit
    assert input_component.aio_id == aio_id
    assert input_component.children[0].id == compo.ids.input(aio_id) == input_component.input_id


def test_component_structure_alt_core_component():
    aio_id, className, label, compo = "test_id", "test", "test-label", dcc.Input
    component = LabeledInput(component=compo, label=label, aio_id=aio_id, className=className)

    label_component = component.children[0]
    input_component = component.children[1]

    assert f"labeled-input {className}" == component.className
    assert len(component.children) == 2
    assert isinstance(label_component, html.P)
    assert isinstance(input_component, compo)
    assert isinstance(label_component.children, str)
    assert label_component.children == label
    assert label_component.className == "input-label"
    assert label_component.id == LabeledInput.ids.label(aio_id) == component.label_id
    assert input_component.id == aio_id


def test_component_structure_alt_no_aioid():
    className, label, compo = "test", "test-label", dcc.Input
    component = LabeledInput(component=compo, label=label, className=className)

    label_component = component.children[0]
    input_component = component.children[1]

    assert f"labeled-input {className}" == component.className
    assert len(component.children) == 2
    assert isinstance(label_component, html.P)
    assert isinstance(input_component, compo)
    assert isinstance(label_component.children, str)
    assert label_component.children == label
    assert label_component.className == "input-label"
    assert isinstance(component.aio_id, str)
    assert len(component.aio_id) == UUID_LENGTH
    assert label_component.id == LabeledInput.ids.label(component.aio_id) == component.label_id
    assert input_component.id == component.aio_id
