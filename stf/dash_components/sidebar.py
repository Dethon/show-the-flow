import pandas as pd
from dash import html, no_update, ctx, callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from stf.dash_components.components import input_table, add_row_button, upload_box, file_alert
from stf.dash_components.constants import TITLE, FILE_FORMAT_ERROR_MSG
from stf.sankey import df_from_csv_base64

sidebar = html.Div(
    className="left-panel", children=[html.H1(TITLE), file_alert, upload_box, input_table, add_row_button]
)


@callback(
    [Output(input_table, "data"), Output(file_alert, "displayed"), Output(file_alert, "message")],
    Input(upload_box, "contents"),
    Input(upload_box, "filename"),
    Input(add_row_button, "n_clicks"),
    State(input_table, "data"),
    State(input_table, "columns"),
)
def update_table(
    file_contents: str,
    file_name: str,
    add_row_clicks: int,
    current_data: list[dict[str, str | float]],
    current_columns: list[dict[str, str]],
) -> tuple[list[dict[str, str | float]], bool, str]:
    trigger_id = ctx.triggered_id
    if add_row_clicks > 0 and trigger_id == add_row_button.id:  # pylint: disable=no-member
        return add_row(current_data, current_columns), no_update, no_update
    elif file_contents is not None and trigger_id == upload_box.id:  # pylint: disable=no-member
        return load_file(file_contents, file_name)
    raise PreventUpdate


def add_row(rows: list[dict[str, str | float]], columns: list[dict[str, str]]) -> list[dict[str, str | float]]:
    rows.append({c["id"]: "" for c in columns})
    return rows


def load_file(contents: str, filename: str) -> tuple[list[dict[str, str | float]], bool, str]:
    if "csv" not in filename:
        return no_update, True, FILE_FORMAT_ERROR_MSG
    return validate_df(df_from_csv_base64(contents))


def validate_df(df: pd.DataFrame) -> tuple[pd.DataFrame, bool, str]:
    expected_headers = ["source", "amount", "target"]
    if set(expected_headers) == set(df.columns):
        return df.to_dict("records"), no_update, no_update

    return no_update, True, FILE_FORMAT_ERROR_MSG
