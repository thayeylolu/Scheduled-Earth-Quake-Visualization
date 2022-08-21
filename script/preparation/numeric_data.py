#!/usr/bin/env python
# Author: Taiwo Owoseni
# date: 2022-08-20

"""Create numeric table from cleaned earthquakes data
   and store as csv file.
Usage: location_data.py 
"""
# import module
import pandas as pd
import  os
import datetime as dt

CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR.replace("/script/preparation", "")
RAW_DATA_DIR = PARENT_DIR + "/data/raw"
CLEAN_DATA_DIR = PARENT_DIR + "/data/preprocessed/clean"
NUMERIC_DATA_DIR = PARENT_DIR + "/data/preprocessed/numeric"

today_date = dt.date.today().strftime("%Y-%m-%d")
str_today_date = str(today_date).replace('-', '_')

if not os.path.exists(NUMERIC_DATA_DIR):
    os.mkdir(NUMERIC_DATA_DIR)
# pick the most recent file
data = pd.read_csv(f'{CLEAN_DATA_DIR}/clean_eq_2022_08_20.csv')
data = data.drop("Unnamed: 0",axis=1)

numeric_data = data[["p_id", "date", "time", "magnitude"]]
numeric_data.to_csv(f'{NUMERIC_DATA_DIR}/numeric_eq_{str_today_date}.csv')