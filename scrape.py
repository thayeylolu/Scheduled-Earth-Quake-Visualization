#!/usr/bin/env python
# Author: Taiwo Owoseni
# date: 2022-08-19

"""Scrape data from the earhquakebot and store as csv file.
Usage: scrape_tweet.py 
"""

import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as dt
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


limit = 50
timeout = 20
today_date = dt.date.today().strftime("%Y-%m-%d")
query_list = [
    (f"(@earthquakeBot) lang:en since:2022-08-18 until:{today_date})"),
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

    def scrape_location_details(self):
        elements = self.driver.find_elements(By.XPATH, "//span[@class='DkEaL']")
        self.driver.implicitly_wait(2)
        return [i.get_attribute('textContent') for i in elements]


def main():
    google_maps = GoogleMaps()
    tweets = []
    for query in query_list:
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) > limit:
                break
            else:
                content = tweet.content
                map_index = content.find("Map")
                if content.find("Map:") != -1:
                    link_url = content[map_index + 5:]
                    map_url = google_maps.get_page(link_url)
                    coordinates = google_maps.scrape_coordinates()
                    location_1 = google_maps.scrape_location_details()[0]  
                    location_2 = google_maps.scrape_location_details()[1] 
                    tweets.append([tweet.date, tweet.user.username,
                                tweet.content, location_1, 
                                location_2, map_url, coordinates]) 
                else:
                    pass
                
    df = pd.DataFrame(tweets, columns=["Date", "User", 
                                        "Tweet","Location",
                                        "Location_2", "Map URL",
                                         "Coordinates"])

    # to save to csv
    df.to_csv('earthquake_bot_with_location.csv')

if __name__ == "__main__":
    main()

