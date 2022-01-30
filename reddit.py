import praw
import pandas as pd

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)

reddit.read_only = True

subreddits = ["CryptoCurrency", "CryptoCurrencies", "bitcoin", "altcoin"]


redditposts = []
for subreddit in subreddits:
    for submission in reddit.subreddit(subreddit).new(limit=25):
        # print(submission.title)
        # print(submission.num_comments)
        # print(submission.upvote_ratio)
        # print(submission.score)
        redditposts.append({'title': submission.title, 'num_comments': submission.num_comments, 'upvote_ratio': submission.upvote_ratio, 'score': submission.score, 'created_utc': submission.created_utc})

df = pd.DataFrame(redditposts)
df.to_csv('data/redditposts.csv', index=False)
