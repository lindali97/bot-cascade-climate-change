#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 21:14:38 2022

@author: lindali
"""

import pandas as pd
import numpy as np
import os
import sys
import re
import json
from sys import argv
import glob

from flatten_json import flatten

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

file_path = argv[1] 
output_file = argv[2]

os.chdir(file_path)
jsons = glob.glob('*.json')

sid_obj = SentimentIntensityAnalyzer()

matching_data = pd.read_csv("/home/linda/data_collection_code/xr2019_user_matched_seconds.csv")
matching_data['matched_uid'] = [int(i) for i in matching_data.matched_uid]

def get_sentiment(text):
    sentiment_dict = sid_obj.polarity_scores(text)
    return sentiment_dict['compound']

def json_to_df(file_name):
    
    with open(file_name) as f:
        file = f.read()
        file = file.replace(",\n}", "}")
        if file != "{\n":
            json_file = json.loads(file)

            json_list = list(json_file.values())
            list_flattened = [flatten(d) for d in json_list]
            flat_tweet = pd.DataFrame(list_flattened)

            if flat_tweet.shape[0] != 0:
                flat_tweet['author_id'] = [int(i) for i in flat_tweet.author_id]

                all_tweet = flat_tweet.merge(matching_data[["matched_uid", "interaction_matched"]], how = "left", left_on = "author_id", right_on = "matched_uid", copy = False)

                all_tweet['created_at_dt'] =  pd.to_datetime(all_tweet.created_at, infer_datetime_format=True)
                all_tweet['interaction_at_dt'] =  pd.to_datetime(all_tweet.interaction_matched, infer_datetime_format=True)
                all_tweet['time_gap'] = all_tweet['created_at_dt'].sub(all_tweet['interaction_at_dt'], axis=0)

                all_text = list(all_tweet.text)
                sentiment_score = [get_sentiment(i) for i in all_text]
                all_tweet['senti'] = sentiment_score
                all_tweet['senti_category'] = [1 if i > 0.05 else -1 if i < -0.05 else 0 for i in sentiment_score]
            else:
                all_tweet = flat_tweet
        else:
            all_tweet = pd.DataFrame()
    
    return all_tweet
    
    
df = pd.DataFrame()
for file in jsons:
    print(file)
    df_temp = json_to_df(file)
    df = df.append(df_temp)
    

df.to_csv(output_file, header='column_names', index = False)

    