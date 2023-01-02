import numpy as np
from plotly.express.colors import sample_colorscale
from stf.domain.colors.colors import rgb_to_rgba


class ColorScale:
    @classmethod
    def get_rgba(cls, name: str, n_colors: int, opacity: float = 0.5) -> list[str]:
        intervals = np.linspace(0, 1, n_colors).tolist()
        return [rgb_to_rgba(c, opacity=opacity) for c in sample_colorscale(name, intervals)]
