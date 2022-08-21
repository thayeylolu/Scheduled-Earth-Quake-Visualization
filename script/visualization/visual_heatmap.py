import time
import datetime as dt
import pandas as pd
import os
import glob
from folium import plugins
from folium.plugins import HeatMap
import folium
import numpy as np
from selenium import webdriver

driver = webdriver.Firefox()
today_date = dt.date.today().strftime("%Y-%m-%d")
str_today_date = str(today_date).replace('-', '_')

CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR.replace("/script/visualization", "")

RAW_DATA_DIR = os.path.join(PARENT_DIR ,"/data/raw")
CLEAN_DATA_DIR = os.path.join(PARENT_DIR, "data/preprocessed/clean")
LOCATION_DATA_DIR = os.path.join(PARENT_DIR , "data/preprocessed/location")
NUMERIC_DATA_DIR = os.path.join(PARENT_DIR , "data/preprocessed/numeric") 
RESULT_DIR = os.path.join(PARENT_DIR, "results")

if not os.path.exists(RESULT_DIR):
    os.mkdir(RESULT_DIR)

# join the two data on pid

def _append_files(directory, match_files):
    files = os.path.join(directory, match_files)
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df = df.drop("Unnamed: 0",axis=1)
    return df

num_df = _append_files(NUMERIC_DATA_DIR, "numeric_eq*.csv")
loc_df = _append_files(LOCATION_DATA_DIR, "location_eq*.csv")
merge_df = pd.merge(num_df, loc_df)

def make_heat_map(merge_df):

    merge_df['mag_norm'] = merge_df.magnitude/np.linalg.norm(merge_df.magnitude) # normalize data
    map = folium.Map(location = [15,30], tiles='Cartodb dark_matter', zoom_start = 1.5)
    heat_df = merge_df[['lat', 'long', 'mag_norm']]
    heat_data = [[row['lat'],row['long'], row['mag_norm']] for index, row in heat_df.iterrows()]
    HeatMap(heat_data).add_to(map)

    map.save(f"{RESULT_DIR}/heat_map_eq.html")
    url = f"file://{RESULT_DIR}/heat_map_eq.html"
    #print(url)
    driver.get(url)
    time.sleep(5)
    driver.save_screenshot(f"{RESULT_DIR}/heat_map_eq.png")
    driver.quit()

make_heat_map(merge_df)