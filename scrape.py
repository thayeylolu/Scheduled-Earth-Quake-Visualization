#!/usr/bin/env python
# Author: Taiwo Owoseni
# date: 2022-08-19

"""Scrape data from the earhquakebot and store as csv file.
Usage: scrape_tweet.py 
"""

from docopt import docopt
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as dt
import requests
from bs4 import BeautifulSoup

def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/ (KHTML, like Gecko)\
                Chrome/ Safari/'}

    response = requests.get(url, headers=headers)
    #print(response.content)
    soup = BeautifulSoup(response.content.decode('cp1252'), 'html.parser')
    return soup

def get_title(soup):
    if soup.findAll("title"):
        return soup.find("title").string
    else:
        return ""
   
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

