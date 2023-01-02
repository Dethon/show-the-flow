from plotly.colors import unlabel_rgb


def rgb_to_rgba(rgb_color: str, opacity: float = 1) -> str:
    return f"rgba{unlabel_rgb(rgb_color) + (opacity,)}"
