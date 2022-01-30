# Data Collector

This is a collection of all the data collectors we've written and used throughout our Research Project

## Crypto

Our crypto data is collected from the Binance Exchange as they allow us to fetch ticker data from the beginning of the existance of the symbol pair.
This is perfect for training our AI on large amounts of data, for context we're able to collect 15.3GB of raw minute candles from Binance.

After adding all our indicators, normalizing the data and labelling it we end up with about double of what we collected.

To use the collector you need to go to the [Binance API management](https://www.binance.com/en/my/settings/api-management) page, create an API-key and put it inside the crypto.py file.

```py
...

API_KEY = ""
SECRET_KEY = ""

...
```

Aside from that nothing will need to be changed and you can just run the file, it will start collecting all data from symbols trading with USDT.

## RSS Feeds

RSS Feeds don't require any API keys, they can be fetched by anyone at any point. We were unable to utilise this collector very well since there's no way to collect historical data, one needs to continously collect data to get any proper dataset.

We've selected quite a few crypto related RSS feeds which we found on the following blog: https://blog.feedspot.com/cryptocurrency_rss_feeds/

## Reddit

For Reddit we've collected data from a crypto subreddits, the ones we've chosen seem to contain the most general data about crypto as collecting data from specific crypto tokens/coins might skew the sentiment of the data collected.

So we've gone with the following subreddits:
 - CryptoCurrency
 - CryptoCurrencies
 - bitcoin
 - altcoin

With Reddit we were unable to collect old data as we can only fetch data from subreddits through tags "hot", "new" or "random". We were able however to get the 25 newest posts but then again for us to collect archival data we'd need to collect this of a really long period and the data collected could be of very low quality since anyone is able to post at any time.

There exist archives of Reddit online but there's no information on the structure available and these are fairly large for just textual content.
