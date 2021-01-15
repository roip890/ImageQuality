import pandas as pd
import numpy as np
from hypothesis import strategies as st

data_2 = pd.read_csv('data/imgQuality_2.csv', index_col=0).iloc[:, 2:].replace(True, 1).replace(False, 0)
data_6 = pd.read_csv('data/imgQuality_6.csv', index_col=0).iloc[:, 2:].replace(True, 1).replace(False, 0)
data_12 = pd.read_csv('data/imgQuality_12.csv', index_col=0).iloc[:, 2:].replace(True, 1).replace(False, 0)

data_2_avg = data_2.mean(axis=1)
data_6_avg = data_6.mean(axis=1)
data_12_avg = data_12.mean(axis=1)
# print(st.booleans().)

data_means = pd.DataFrame(columns=['2', '6', '12'])
data_means['2'] = data_2_avg
data_means['6'] = data_6_avg
data_means['12'] = data_12_avg
print(data_means)
