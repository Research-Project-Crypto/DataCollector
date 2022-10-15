import asyncio
from os import path, walk, stat, makedirs
from binance import AsyncClient,ThreadedWebsocketManager
import csv
from datetime import date
import pandas as pd
from tqdm import tqdm
from random import shuffle

start_date = date.today()
path_exist = path.exists(f"./Data/Crypto/")
if path_exist == True:
    print('cleaning...')
    for root, dirs, files in walk(f"./Data/Crypto/"):
        for name in files:
            try:
                df = pd.read_csv(path.join(root, name), error_bad_lines=False)
                if len(df) >= 10:
                    df = df.set_index(df['event_time'])
                    df = df.drop_duplicates(subset=['kline_start_time'], keep='last')
                    df = df.sort_index()
                    df.pop('event_time')
                    df.to_csv(path.join(root, name))
            except Exception as e:
                print(str(e))
    print('done cleaning')
else:
    makedirs(f"./Data/Crypto/")

datapath = f"./Data/Crypto/"

retreived = []
for root, dirs, files in walk(f"./Data/Crypto/"):
    for name in files:
        try:
            print(name[:-4])
            retreived.append(name[:-4])
        except Exception as e:
            print(str(e))
    print('done cleaning')

API_KEY = ""
SECRET_KEY = ""

unwanted3 = [ "AUD", "BRL", "EUR", "GBP", "RUB", "TRY", "DAI", "UAH", "VAI", "NGN", "BNB", "BTC", "ETH", "XRP", "DOT", "DAI" ]
unwanted4 = [ "BUSD", "BIDR", "TUSD", "USDC", "IDRT", "USDP", "DOGE", "DOWN", "BULL", "BEAR", "USDSB", "TUSDT"]
wanted4 = ["USDT"]

open_connections = 0

async def main():
    global open_connections
    global client
    global streams
    client = await AsyncClient.create(API_KEY, SECRET_KEY)
    twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=SECRET_KEY)
    twm.start()
    tickers = []
    streams = []
    res = await client.get_exchange_info()
    symbols = res["symbols"]
    shuffle(symbols)
    for symbol in symbols:
        s = symbol["symbol"]
        if s not in retreived and s[-4:] == wanted4[0] and s[-6:-4] != "UP" and s[-8:-4] not in unwanted4:
            tickers.append(s)

    print(len(tickers))
    for s in tqdm(tickers):
        if path.isfile(f'./Data/Crypto/{s}.csv'):
            fileEmpty = stat(f'./Data/Crypto/{s}.csv').st_size == 0
            if fileEmpty:
                asyncio.create_task(get_coin(s))
                open_connections += 1
                await asyncio.sleep(10)
        else:
            asyncio.create_task(get_coin(s))
            open_connections += 1
            await asyncio.sleep(10)

        while open_connections >= 10:
            await asyncio.sleep(1)
    while open_connections > 1:
        await asyncio.sleep(1)

async def get_coin(s):
    global open_connections
    global client
    global streams
    # print(f'get {s}')
    # print(f'open connections: {open_connections}')
    try:
        candles = await client.get_historical_klines(s, interval = AsyncClient.KLINE_INTERVAL_1MINUTE, start_str = '480000 minutes ago CET', end_str = '1 minutes ago CET')
        # print(f'got {s}')
        open_connections -= 1
        # print(f'open connections: {open_connections}')
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, write_coin, s, candles)
    except Exception as e:
        print(str(e))

def write_coin(s, candles):
    global streams
    # print('start writing')
    with open(f'./Data/Crypto/{s}.csv', mode='a',newline='') as csv_file:
        writer = csv.writer(csv_file, dialect="unix")
        writer.writerow(["event_time","open", "close", "high", "low","volume"])
        for candle in candles:
            event_time = int(candle[0])
            # candle_start_time = float(candle[0])
            # candle_close_time = float(candle[6])
            candle_open = float(candle[1])
            candle_close = float(candle[4])
            candle_high = float(candle[2])
            candle_low = float(candle[3])
            candle_volume = float(candle[5])
            writer.writerow([event_time, candle_open, candle_close, candle_high, candle_low, candle_volume])
        print('done writing')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
