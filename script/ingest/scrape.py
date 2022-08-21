#!/usr/bin/env python
# Author: Taiwo Owoseni
# date: 2022-08-19

"""Scrape data from the earhquakebot and store as csv file.
Usage: scrape.py 
"""

import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import re, os

from selenium import webdriver
import snscrape.modules.twitter as sntwitter
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

limit = 50
timeout = 20

PARENT_DIR = os.getcwd()
RAW_DATA_DIR = os.path.join(PARENT_DIR ,"data/raw")

today_date = dt.date.today().strftime("%Y-%m-%d")
lastwk_date = dt.date.today() - timedelta(days=7)
lastwk_date = lastwk_date.strftime("%Y-%m-%d") 

str_today_date = str(today_date).replace('-', '_')
str_yesdy_date = str(lastwk_date).replace('-', '_')

if not os.path.exists(RAW_DATA_DIR):
    os.mkdir(RAW_DATA_DIR)

query_list = [
    (f"(@earthquakeBot) lang:en since:{lastwk_date} until:{today_date})"),
]
class WebDriverImplementation:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(options = self.options)
class GoogleMaps(WebDriverImplementation):
    def get_page(self, url):
        try:
            self.driver.get(url)
            map_present = EC.url_contains("https://www.google.com/maps/place/")
            WebDriverWait(self.driver, timeout).until(map_present) # visit the last redirect link
            return self.driver.current_url
        except TimeoutException:
            return "Timed out waiting for page to load"

    def scrape_coordinates(self):
        #(?<=X)(.*?)(?=Y) get cooridnates from string
        coordinates = re.search("(?<=maps/place/)(.*?)(?=/)", self.driver.current_url)
        return coordinates.group()
    
    def scrape_coordinates_search(self):
        #(?<=X)(.*?)(?=Y) get cooridnates from searchbox
        elements = self.driver.find_elements(By.XPATH, "//input[@class='tactile-searchbox-input searchboxinput xiQnY']")
        self.driver.implicitly_wait(2)
        return [element.get_attribute('value') for element in elements]
     

    def scrape_location_details(self):
        elements = self.driver.find_elements(By.XPATH, "//span[@class='DkEaL']")
        self.driver.implicitly_wait(2)
        return [i.get_attribute('textContent') for i in elements]

class USGSEarthQuake(WebDriverImplementation):
    def get_page(self, url):
        try:
            self.driver.get(url)
            quake_home = EC.url_contains("https:/earthquake.usgs.gov/")
            WebDriverWait(self.driver, timeout).until(quake_home) # visit the last redirect link
            return self.driver.current_url
        except TimeoutException:
            return "Timed out waiting for page to load"

def main():
    google_maps = GoogleMaps()
    tweets_dictionary = {}
    tweet_key = 0
    for query in query_list:
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets_dictionary) > limit:
                break
            else:
                # print(tweet.content)
                tweet_key += 1
                find_link_url = re.search("(?<=Map: )(.*?)(?=$)", tweet.content)
                # print(find_link_url)
                if find_link_url is not None:
                    link_url = find_link_url.group()
                    map_url = google_maps.get_page(link_url)
                    #coordinates = google_maps.scrape_coordinates()
                    se_cord = google_maps.scrape_coordinates_search()[0]
                    lat = se_cord.split(",")[0]
                    long = se_cord.split(",")[1]
                    location_1 = google_maps.scrape_location_details()[0]
                    location_2 = google_maps.scrape_location_details()[1]
                    magnitude = re.search("(?<=A )(.*?)(?= magnitude)", tweet.content).group()
                    region =  re.search("(?<=occured )|(?<=earthquake)(.*?)(?=Details)", tweet.content).group()
                    tweets_dictionary[tweet_key]= [tweet.date, tweet.user.username,
                                                region, tweet.content, location_1,    
                                                location_2, map_url,lat,long, magnitude]
                    #print(tweets_dictionary)
                else:
                    pass
                
    df = pd.DataFrame.from_dict(tweets_dictionary,orient='index',
                                 columns=[
                                        "date", "user", 
                                        "region",
                                        "tweet","location",
                                        "location_2", "map_url",
                                        "lat","long", "magnitude"])

    # to save to csv
    df.to_csv(f'{RAW_DATA_DIR}/earthquake_bot_{str_today_date}.csv')
if __name__ == "__main__":
    main()

