
#!/usr/bin/env python
# Author: Taiwo Owoseni
# date: 2022-08-20

"""Clean from the earhquakebot and store as csv file.
Usage: clean_data.py 
"""

import pandas as pd
import re, os
import datetime as dt

today_date = dt.date.today().strftime("%Y-%m-%d")
str_today_date = str(today_date).replace('-', '_')

CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR.replace("/script/preparation", "")
RAW_DATA_DIR = os.path.join(PARENT_DIR ,"data/raw")
CLEAN_DATA_DIR = os.path.join(PARENT_DIR, "data/preprocessed/clean")


if not os.path.exists(CLEAN_DATA_DIR):
     os.makedirs(CLEAN_DATA_DIR)

# pick the most recent file
data = pd.read_csv(f'{RAW_DATA_DIR}/earthquake_bot_{str_today_date}.csv')
data = data.rename(columns={'Unnamed: 0':'id'})

def _find_last_word(x):
    last_word = re.search("(\w+)$", x).group()
    if last_word in ["Sea", "Ocean", "River", "Volcano"]:
        return x
    else:
        return last_word

def clean_data(df):
    if df.user.unique()[0] != 'earthquakeBot':
        # filter the dataset to have only data from 'earthquakebot'
        df = df.query('User == "earthquakeBot"')
    else:
        pass
    df['date_'] = pd.to_datetime(df['date'])
    df['date'] = df.date_.apply(lambda x: x.date())
    df['time'] = df.date_.apply(lambda x: x.time())
    df['id'] = df['date'].astype(str) + 'ID' +  df['id'].astype(str)
    df['region']= df.region.str.replace('occurred ', '').replace('in ', '').replace('.', '')
    df['filtered_location'] = df.location.apply(lambda x : _find_last_word(x))
    clean_df = df[['id','date', 'time', 'location','filtered_location', 'lat', 'long', 'magnitude']]

    return clean_df.to_csv(f'{CLEAN_DATA_DIR}/clean_eq_{str_today_date}.csv')

clean_data(data)


    


