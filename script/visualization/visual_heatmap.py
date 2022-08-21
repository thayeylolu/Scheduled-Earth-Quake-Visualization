import time
import pandas as pd
import os
from folium import plugins
from folium.plugins import HeatMap
import folium
import numpy as np
from selenium import webdriver

driver = webdriver.Firefox()

CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR.replace("/notebooks/visualizations", "")
RAW_DATA_DIR = PARENT_DIR + "/data/raw"
CLEAN_DATA_DIR = PARENT_DIR + "/data/preprocessed/clean"
LOCATION_DATA_DIR = PARENT_DIR + "/data/preprocessed/location"
NUMERIC_DATA_DIR = PARENT_DIR + "/data/preprocessed/numeric"
RESULT_DIR = PARENT_DIR + "/results"

if not os.path.exists(RESULT_DIR):
    os.mkdir(RESULT_DIR)

# join the two data on pid
num_df = pd.read_csv(f'{NUMERIC_DATA_DIR}/numeric_eq_2022_08_20.csv')
loc_df = df = pd.read_csv(f'{LOCATION_DATA_DIR}/location_eq_2022_08_20.csv')

num_df = num_df.drop("Unnamed: 0",axis=1)
loc_df = loc_df.drop("Unnamed: 0",axis=1)

merge_df = pd.merge(num_df, loc_df)
merge_df['mag_norm'] = merge_df.magnitude/np.linalg.norm(merge_df.magnitude) # normalize data
print(RESULT_DIR)
def make_heat_map(merge_df):
    map = folium.Map(location = [15,30], tiles='Cartodb dark_matter', zoom_start = 1.5)
    heat_df = merge_df[['lat', 'long', 'mag_norm']]
    heat_data = [[row['lat'],row['long'], row['mag_norm']] for index, row in heat_df.iterrows()]
    HeatMap(heat_data).add_to(map)

    map.save(f"{RESULT_DIR}/heat_map_eq.html")
    url = f"file://{RESULT_DIR}/heat_map_eq.html"
    print(url)
    driver.get(url)
    time.sleep(5)
    driver.save_screenshot(f"{RESULT_DIR}/heat_map_eq.png")
    driver.quit()

make_heat_map(merge_df)