import pandas as pd
import numpy as np

data = pd.read_feather("./testdata-RL18.feather")
data.station = pd.to_numeric(data.station, downcast = 'integer')

# drop soil moisture predictions due to missing values
# Note that self is a minor change compared to the paper, but does not have a significant effect
data = data.drop(['sm_mean', 'sm_var'], axis=1)
