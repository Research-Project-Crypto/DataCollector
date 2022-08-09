import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

# csv1 = "ALICEUSDT"
# df1 = pd.read_csv(f"Data/Crypto/{csv1}.csv")

min = 0
min_csv = ""
max = 0
max_csv = ""

# for path, dirs, files in os.walk("Data/Crypto/"):
#     correlationdf = pd.DataFrame(columns=[name[:-8] for name in files], index=[name[:-8] for name in files])
#     # print(correlationdf["1INCH"][csv1[:-4]])
#     for csv in files:
        
#         df2 = pd.read_csv(f"Data/Crypto/{csv}")
#         corr = df1.corrwith(df2, axis = 0)

#         #add correlation to correlationdf
#         correlationdf[csv[:-8]][csv1[:-4]] = corr["close"]
#         correlationdf[csv1[:-4]][csv[:-8]] = corr["close"]

#         if csv[:-4] == csv1:
#             continue
#         if corr["close"] < min:
#             min = corr["close"]
#             min_csv = csv.split('USDT')[0]
#         if corr["close"] > max:
#             max = corr["close"]
#             max_csv = csv.split('USDT')[0]
#     print(correlationdf)

for path, dirs, files in os.walk("Data/Crypto/"):
    correlationdf = pd.DataFrame(columns=[name[:-8] for name in files], index=[name[:-8] for name in files])
    # print(correlationdf["1INCH"][csv1[:-4]])
    for csv1 in tqdm(files):
        for csv in files: 
            if not pd.isnull(correlationdf.at[csv1[:-8],csv[:-8]]):
                continue

            df1 = pd.read_csv(f"Data/Crypto/{csv1}")
            df2 = pd.read_csv(f"Data/Crypto/{csv}")
            corr = df1.corrwith(df2, axis = 0)

            correlationdf[csv[:-8]][csv1[:-8]] = corr["close"]
            correlationdf[csv1[:-8]][csv[:-8]] = corr["close"]

    print(correlationdf)

correlationdf.to_csv("correlations.csv")