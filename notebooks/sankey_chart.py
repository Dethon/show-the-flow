# %%
import pandas as pd
from stf.domain.sankey import Sankey

# %%
links_df = pd.read_csv("../datasets/sample.csv")
sk = Sankey(links_df, unit="€")
sk.show()

# %%
