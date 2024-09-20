#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:25:30 2022

@author: lindali

Codes for infrastructure of second-stage analysis - data collection 
of user tweets before/after the penetration by bots.
"""

from load_token import load_token


import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import datetime as dt
import json
import time

import sqlalchemy
import psycopg2

from sys import argv
import logging

from TwitterAPI import TwitterAPI, TwitterOAuth, HydrateType, TwitterPager

user_table = argv[1]
filename = argv[2]

logging.basicConfig(level = logging.INFO, datefmt = '%a, %d %b %Y %H:%M:%S',
                format ='%(asctime)s %(levelname)s %(message)s',
                filename = filename + ".log")

users = pd.read_csv(user_table)
num = users.shape[0]

consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token = load_token('twitter_auth')
api = TwitterAPI(consumer_key, consumer_secret, auth_type='oAuth2', api_version='2')

for i in range(num):
    user_info = users.iloc[i]
    uid = int(user_info.matched_uid)
    start_time = user_info.time_start_str
    end_time = user_info.time_end_str
    
    file_usr = filename + "_" + str(uid) + ".json"
    
    QUERY = '(XRebellion OR xrebellion OR #ExtinctionRebellion OR "extinction rebellion" OR XR OR "climate change" OR protest) lang:en from:'+str(uid)
    
    EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id'
    TWEET_FIELDS = 'created_at,author_id,conversation_id,geo,in_reply_to_user_id'
    
    pager = TwitterPager(api, 'tweets/search/all', 
                {
                    'query': {QUERY}, 
                    'expansions': EXPANSIONS,
                    'start_time': start_time,
                    'end_time': end_time,
                    'tweet.fields': TWEET_FIELDS,
                    "max_results": 500
                    
                })
    
    
    try:
        with open(file_usr, 'a+', encoding='utf-8') as f:
            f.write("{\n")
            for count, item in enumerate(pager.get_iterator(new_tweets=False, wait = 12)): 
                f.write("\"" + str(count) + "\":")
                json.dump(item, f)
                f.write(",")
            f.write("\n}")
      
        time.sleep(5)        
        logging.info(f"User {uid} finished!")
        
    except Exception as e:
        logging.warning(f"Error in {uid} for {file_usr}: {e}")
        time.sleep(120)    
        
    
    
    

    
    



