from typing import Any


TITLE = "Show the Flow (STF*)"
FILE_FORMAT_ERROR_MSG = "Wrong file format: Only CSV files with columns (source, amount, target) are supported."
DEFAULT_LAYOUT = dict(margin=dict(autoexpand=True, b=25, l=25, t=25, r=25))
COLORSCALES = ["IceFire", "Twilight", "HSV", "mrybm", "mygbm", "Edge"]
DEFAULT_TABLE_PROPS: dict[str, Any] = dict(aio_id="links-table", page_size=25)
