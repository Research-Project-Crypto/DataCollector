from os import path, walk, stat, makedirs
import pandas as pd
import tqdm

for root, dirs, files in walk(f"./Data/Crypto/"):
        for name in (pbar:= tqdm.tqdm(files)):
            try:
                df = pd.read_csv(path.join(root, name))
                if len(df) >= 10:
                    df = df.set_index(df['event_time'])
                    df = df.sort_index()
                    df.pop('event_time')
                    df.to_csv(path.join(root, name))
            except Exception as e:
                print(str(e))

            pbar.set_description_str("Fixed: " + name)