import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

filename = "correlations_1month"
wanted = "VET"
threshold = 0.8

correlationdf = pd.read_csv(f"{filename}.csv", index_col=0)

coins = correlationdf.columns.values[1:]
correlations = correlationdf[wanted]

high_corr = []
low_corr = []

for i in tqdm(range(len(correlations))):
    if correlations.index[i] == wanted:
        continue
    if correlations.values[i] > threshold:
        high_corr.append(correlations.index[i])
    else:
        low_corr.append(correlations.index[i])

print(high_corr)