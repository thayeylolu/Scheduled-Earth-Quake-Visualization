#!/usr/bin/env python
# Author: Taiwo Owoseni
# date: 2022-08-20

"""Create location table for earthquakes and store as csv file.
Usage: location_data.py 
"""
# import module
from geopy.geocoders import Nominatim
import pandas as pd
import  os
import datetime as dt

CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR.replace("/notebooks", "")
RAW_DATA_DIR = PARENT_DIR + "/data/raw"
CLEAN_DATA_DIR = PARENT_DIR + "/data/preprocessed/clean"
LOCATION_DATA_DIR = PARENT_DIR + "/data/preprocessed/location"

today_date = dt.date.today().strftime("%Y-%m-%d")
str_today_date = str(today_date).replace('-', '_')

if not os.path.exists(LOCATION_DATA_DIR):
    os.mkdir(LOCATION_DATA_DIR)

data = pd.read_csv(f'{CLEAN_DATA_DIR}/clean_eq_2022_08_20.csv')
data = data.drop("Unnamed: 0",axis=1)
geolocator = Nominatim(user_agent="located_coord")

def _extract_loc_info(address):
    if address is not None:
        country = address.get('country', '')
    else:
        country = None
    return country

def _get_location_info(point):
        location = geolocator.reverse(point)
        if location is None:
            return None
        else:
            return location.raw['address']

def create_geolocation_data(df):
    df['lat'] = df['lat'].astype(str)
    df['long'] = df['long'].astype(str)

    location_df = df[['lat','long', 'filtered_location']]
    location_df['geom_data'] = location_df["lat"].map(str)  + ',' + location_df['long'].map(str)
    location_df['loc_info'] = location_df['geom_data'].apply(lambda x : _get_location_info(x))
    location_df['country'] = location_df['loc_info'].apply(lambda x : _extract_loc_info(x))
    location_df['country'].fillna(location_df['filtered_location'], inplace=True)

    return location_df.to_csv(f'{LOCATION_DATA_DIR}/location_eq_{str_today_date}.csv')

create_geolocation_data(data)