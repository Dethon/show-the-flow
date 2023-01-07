from dash import dcc, html
from stf.dash_components import UnitableInput


def test_component_structure_general():
    aio_id, className, unit, value, field_type, placeholder = "test_id", "test", "px", 27, "number", "test"
    component = UnitableInput(
        unit=unit,
        value=value,
        placeholder=placeholder,
        type=field_type,
        aio_id=aio_id,
        className=className,
    )
    input_component = component.children[0]
    unit_component = component.children[1]

    assert f"input-with-unit {className}" == component.className
    assert len(component.children) == 2
    assert isinstance(unit_component, html.P)
    assert isinstance(input_component, dcc.Input)
    assert isinstance(unit_component.children, str)
    assert unit_component.children == unit
    assert unit_component.className == "input-unit"
    assert unit_component.id == UnitableInput.ids.unit(aio_id) == component.unit_id

    assert input_component.placeholder == placeholder
    assert input_component.value == value
    assert input_component.type == field_type
    assert input_component.id == UnitableInput.ids.input(aio_id) == component.input_id


def test_component_structure_alt_without_unit():
    component = UnitableInput()
    assert "input-with-unit" == component.className
    assert len(component.children) == 1
    assert isinstance(component.children[0], dcc.Input)
