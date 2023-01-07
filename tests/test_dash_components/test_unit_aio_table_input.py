import pytest
from dash.exceptions import PreventUpdate
from stf.dash_components import InputTable


def test_callback_table_view_interaction_pagination():
    component = InputTable()
    page, page_size, sort_by, filter = 2, 1, [], {}
    data = [{"test": 1}, {"test": 2}, {"test": 3}, {"test": 4}]
    paged = lambda page, page_size: slice(page * page_size, (page * page_size) + page_size)

    result = component.table_view_interaction(page, page_size, sort_by, filter, data)
    assert result == data[paged(page, page_size)]

    page, page_size = 0, 1
    result = component.table_view_interaction(page, page_size, sort_by, filter, data)
    assert result == data[paged(page, page_size)]

    page, page_size = 1, 3
    result = component.table_view_interaction(page, page_size, sort_by, filter, data)
    assert result == data[paged(page, page_size)]

    page, page_size = 1, 2
    result = component.table_view_interaction(page, page_size, sort_by, filter, data)
    assert result == data[paged(page, page_size)]


def test_callback_table_view_interaction_sort():
    component = InputTable()
    page, page_size, filter = 0, 20, {}
    sort_by = [{"column_id": "name", "direction": "asc"}]
    data = [{"test": 1, "name": "d"}, {"test": 2, "name": "c"}, {"test": 3, "name": "b"}, {"test": 4, "name": "a"}]

    result = component.table_view_interaction(page, page_size, sort_by, filter, data)
    assert [r["test"] for r in result] == [4, 3, 2, 1]

    sort_by = [{"column_id": "test", "direction": "desc"}]
    result = component.table_view_interaction(page, page_size, sort_by, filter, data)
    assert [r["test"] for r in result] == [4, 3, 2, 1]


def test_callback_update_store():
    pass


def test_callback_update_page_size_ok():
    component = InputTable()
    assert component.update_page_size(5) == 5


def test_callback_update_page_size_noupdate():
    component = InputTable()
    with pytest.raises(PreventUpdate):
        component.update_page_size(0)


def test_callback_update_page_count_ok():
    component = InputTable()
    data = [{}, {}, {}, {}]
    assert component.update_page_count(data, 7) == 1
    assert component.update_page_count(data, 4) == 1
    assert component.update_page_count(data, 3) == 2
    assert component.update_page_count(data, 2) == 2
    assert component.update_page_count(data, 1) == 4


def test_callback_update_page_count_noupdate():
    component = InputTable()
    with pytest.raises(PreventUpdate):
        component.update_page_count([{}, {}, {}, {}], 0)


def test_component_structure_general():
    pass
