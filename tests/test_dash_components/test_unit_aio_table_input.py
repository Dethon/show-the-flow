import pytest
import pandas as pd
from dash.exceptions import PreventUpdate
from dependency_injector import providers
from stf.domain.ports import DataframeCache
from stf.entrypoints.dash_app.components.input_table import InputTable, IDX_COL
from stf.adapters.fake_redis_chart_data_cache import FakeRedisDataframeCache
from stf.dependency_configurator import services


@pytest.fixture
def cache() -> DataframeCache:
    cache = FakeRedisDataframeCache()
    services.adapters.cache.override(providers.Object(cache))
    return cache


def test_callback_table_view_interaction_pagination(cache: DataframeCache):
    component = InputTable()
    page, page_size = 2, 1
    sort_by: list = []
    filter_query: dict = {}

    df = pd.DataFrame.from_dict([{"test": 1}, {"test": 2}, {"test": 3}, {"test": 4}])
    data = df.reset_index(names=IDX_COL).to_dict("records")
    key = cache.add_data(df)

    paged = lambda page, page_size: slice(page * page_size, (page * page_size) + page_size)

    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert result == data[paged(page, page_size)]

    page, page_size = 0, 1
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert result == data[paged(page, page_size)]

    page, page_size = 1, 3
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert result == data[paged(page, page_size)]

    page, page_size = 1, 2
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert result == data[paged(page, page_size)]


def test_callback_table_view_interaction_sort(cache: DataframeCache):
    component = InputTable()
    page, page_size = 0, 20
    sort_by = [{"column_id": "name", "direction": "asc"}]
    filter_query: dict = {}

    df = pd.DataFrame.from_dict(
        [{"test": 1, "name": "d"}, {"test": 2, "name": "c"}, {"test": 3, "name": "b"}, {"test": 4, "name": "a"}]
    )
    key = cache.add_data(df)

    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == [4, 3, 2, 1]

    sort_by = [{"column_id": "test", "direction": "desc"}]
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == [4, 3, 2, 1]


def test_callback_table_view_interaction_filter(cache: DataframeCache):
    component = InputTable()
    page, page_size = 0, 20
    sort_by: list = []
    filter_query = {"value": "scontains", "left": {"value": "name"}, "right": {"value": "ee"}}

    df = pd.DataFrame.from_dict(
        [
            {"test": 1, "name": "dooo"},
            {"test": 2, "name": "cooo"},
            {"test": 3, "name": "beee"},
            {"test": 4, "name": "aeee"},
        ]
    )
    key = cache.add_data(df)

    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == [3, 4]

    filter_query = {"value": "s>", "left": {"value": "test"}, "right": {"value": 1}}
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == [2, 3, 4]

    filter_query["value"] = "i<"
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == []

    filter_query["value"] = "s!="
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == [2, 3, 4]

    filter_query["value"] = "s="
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == [1]

    filter_query["value"] = "s>="
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == [1, 2, 3, 4]

    filter_query["value"] = "s<="
    result = component.table_view_interaction(page, page_size, sort_by, filter_query, key)
    assert [r["test"] for r in result] == [1]


def test_callback_update_store(cache: DataframeCache):
    pass


def test_callback_update_page_size_ok(cache: DataframeCache):
    component = InputTable()
    assert component.update_page_size(5) == 5


def test_callback_update_page_size_noupdate(cache: DataframeCache):
    component = InputTable()
    with pytest.raises(PreventUpdate):
        component.update_page_size(0)


def test_callback_update_page_count_ok(cache: DataframeCache):
    component = InputTable()
    data = pd.DataFrame.from_dict([{"a": 1}, {"a": 1}, {"a": 1}, {"a": 1}])
    cache = FakeRedisDataframeCache()
    services.adapters.cache.override(providers.Object(cache))
    key = cache.add_data(data)

    assert component.update_page_count(key, 7, {}) == 1
    assert component.update_page_count(key, 4, {}) == 1
    assert component.update_page_count(key, 3, {}) == 2
    assert component.update_page_count(key, 2, {}) == 2
    assert component.update_page_count(key, 1, {}) == 4


def test_callback_update_page_count_noupdate(cache: DataframeCache):
    component = InputTable()
    with pytest.raises(PreventUpdate):
        component.update_page_count("", 0, None)


def test_component_structure_general(cache: DataframeCache):
    pass
