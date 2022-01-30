import feedparser
import pandas as pd
import json

urls = ["https://cointelegraph.com/rss", "https://www.newsbtc.com/feed", "https://www.cryptoninjas.net/feed/", "https://www.fxopen.blog/","https://devcoins.org/","https://news.bitcoin.com/feed/", "https://blog.coinbase.com/feed", "https://www.financemagnates.com/cryptocurrency/feed/", "https://blog.kraken.com/feed", "https://coinstats.app/blog/feed/", "https://www.helenabitcoinmining.com/", "https://bitcoinmagazine.com/"]

# url = "https://www.cryptoninjas.net/feed/"
# f = feedparser.parse(url)
# print(f.keys())
# print(f.entries[1].keys())
# print(f.entries[1].content)
# print(f.entries[1].title)

f = open('data/coins2.json')
file = json.load(f)
cryptocurrencies = []
for item in file['data']['cryptoCurrencyList']:
    cryptocurrencies.append(item)

entries = []
for url in urls:
    f = feedparser.parse(url)
    for entry in f.entries:
        if type(entry) is not dict:
            entry = dict(entry)
        if 'content' in entry.keys() and 'value' in entry['content'][0].keys():
            entry['content'] = entry['content'][0]['value']
        entries.append(entry)

for entry in entries:
    related_cryptos = []
    relevant_items = ['title', 'tags', 'summary', 'content']
    for item in relevant_items:
        if item in entry.keys():
            for crypto in cryptocurrencies:
                if crypto['name'] in entry[item] and crypto['symbol'] not in related_cryptos:
                    related_cryptos.append(crypto['symbol'])
                    # print(crypto['name'])
                    # print(entry[item])
    entry['cryptos'] = related_cryptos

dataset = pd.DataFrame(entries)
print(dataset.head())
dataset.to_csv('data/feeds.csv')
