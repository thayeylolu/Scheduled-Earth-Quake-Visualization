#!/usr/bin/env python
# Author: Taiwo Owoseni
# date: 2022-08-19

"""Scrape data from the earhquakebot and store as csv file.
Usage: scrape_tweet.py 
"""

import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as dt

limit = 50
today_date = dt.date.today().strftime("%Y-%m-%d")

query_list = [
    (f"(@earthquakeBot) lang:en since:2022-08-18 until:{today_date})"),
]
def main():
    tweets = []
    for query in query_list:
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) > limit:
                break
            else:
                   
                tweets.append([tweet.date, tweet.user.username, tweet.content])

    df = pd.DataFrame(tweets, columns=["Date", "User", "Tweet"])

    # to save to csv
    df.to_csv('earthquake_bot_with_location.csv')

if __name__ == "__main__":
    main()

