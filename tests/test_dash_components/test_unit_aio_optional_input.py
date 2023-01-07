from dash import dcc
from stf.dash_components import OptionalInput, UnitableInput


def test_callback_input_enabling():
    component = OptionalInput()
    check_status = True
    result = component.input_enabling(check_status)
    assert check_status != result
    result = component.input_enabling(not check_status)
    assert check_status == result


def test_component_structure_general():
    aio_id, className, is_checked = "test_id", "test", False
    component = OptionalInput(aio_id=aio_id, className=className, is_checked=is_checked)
    checkbox_component = component.children[0]
    input_component = component.children[1]

    assert f"optional-input {className}" == component.className
    assert len(component.children) == 2
    assert isinstance(checkbox_component, dcc.Checklist)
    assert len(checkbox_component.options) == 1
    assert checkbox_component.options[0]["label"] == ""
    assert bool(checkbox_component.value) == is_checked
    assert checkbox_component.id == OptionalInput.ids.checklist(aio_id)
    assert isinstance(input_component, UnitableInput)
    assert (
        component.input_id
        == input_component.input_id
        == OptionalInput.ids.input(aio_id)
        == UnitableInput.ids.input(aio_id)
    )


def test_component_structure_alt_deactivated():
    is_checked = True
    component = OptionalInput(is_checked=is_checked)
    checkbox_component = component.children[0]
    assert bool(checkbox_component.value) == is_checked
    assert checkbox_component.options[0]["value"] == checkbox_component.value[0]
