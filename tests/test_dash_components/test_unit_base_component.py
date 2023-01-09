from stf.entrypoints.dash_app.components.base_component import BaseComponent
from tests.utils.constants import UUID_LENGTH


def test_generate_uuid():
    base_component = BaseComponent()
    id1, id2 = base_component.generate_uuid(), base_component.generate_uuid()
    assert id1 != id2
    assert len(id1) == len(id2) == UUID_LENGTH


def test_add_defaults():
    base_component = BaseComponent()
    prop_dict = dict(prop1=1, prop2=2, prop3=3, prop4=4)
    defaults = dict(prop1=5, prop5=5)
    expected_result = dict(prop1=1, prop2=2, prop3=3, prop4=4, prop5=5)
    result = base_component.add_defaults(prop_dict, defaults)
    assert result == expected_result


def test_class_name_concat():
    base_component = BaseComponent()
    result = base_component.class_name_concat(["class1", "class2 class3", "class4"])
    assert result == "class1 class2 class3 class4"

    result = base_component.class_name_concat(["class1", "class2"], ",")
    assert result == "class1,class2"

    result = base_component.class_name_concat(["class1"])
    assert result == "class1"
