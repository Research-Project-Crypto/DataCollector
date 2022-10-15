import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

min = 0
min_csv = ""
max = 0
max_csv = ""

for path, dirs, files in os.walk("Data/Crypto/"):
    correlationdf = pd.DataFrame(columns=[name[:-8] for name in files], index=[name[:-8] for name in files])

    for csv1 in tqdm(files):
        df1 = pd.read_csv(f"Data/Crypto/{csv1}").head(43200)
        for csv in tqdm(files): 
            if not pd.isnull(correlationdf.at[csv1[:-8],csv[:-8]]):
                continue
            
            df2 = pd.read_csv(f"Data/Crypto/{csv}").head(43200)

            corr = df1.corrwith(df2, axis = 0)

            correlationdf[csv[:-8]][csv1[:-8]] = corr["close"]
            correlationdf[csv1[:-8]][csv[:-8]] = corr["close"]

    print(correlationdf)

correlationdf.to_csv("correlations_1month.csv")