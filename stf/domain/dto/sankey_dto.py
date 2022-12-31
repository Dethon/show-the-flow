from pydantic import BaseModel


class LinkDTO(BaseModel):
    source: str
    amount: float
    target: str


class SankeyDTO(BaseModel):
    links: list[LinkDTO]
    colorscale: str = "IceFire"
    unit: str | None = None
    full_label: bool = False
    width: int = 500
    height: int = 500
