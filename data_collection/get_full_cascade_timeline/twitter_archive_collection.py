#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 00:12:37 2021

@author: lindali
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
import os

from TwitterAPI import TwitterAPI, TwitterOAuth, HydrateType, TwitterPager    

if __name__ == "__main__":
   

    QUERY = argv[1]
    start_time = argv[2]
    end_time = argv[3]
    filename = argv[4]
    
    EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id'
    TWEET_FIELDS = 'created_at,author_id,public_metrics,conversation_id,geo,in_reply_to_user_id,possibly_sensitive'
    USER_FIELDS = 'created_at,description,location,protected,public_metrics,verified,withheld'
    
    logging.basicConfig(level = logging.INFO, datefmt = '%a, %d %b %Y %H:%M:%S',
                    format ='%(asctime)s %(levelname)s %(message)s',
                    filename = filename + ".log")
    while True:
        try:
            consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token = load_token('twitter_auth')
            api = TwitterAPI(consumer_key, consumer_secret, auth_type='oAuth2', api_version='2')
            pager = TwitterPager(api, 'tweets/search/all', 
                {
                    'query': {QUERY}, 
                    'expansions': EXPANSIONS,
                    'start_time': start_time,
                    'end_time': end_time,
                    'tweet.fields': TWEET_FIELDS,
                    'user.fields': USER_FIELDS
                })
            all_item = {}
            for count, item in enumerate(pager.get_iterator(new_tweets=False, wait = 10)):  
                mod = (count + 1) % 1000
                if mod != 0:
                    all_item[count] = item
                else:
                    try:
                        with open(filename + str(count//1000) + '.json', 'w', encoding='utf-8') as f:
                            json.dump(all_item, f, indent=2)
                        all_item = {}
                        if item['created_at'].startswith("2020-05-25T00:00"):
                            break
                    except Exception as e:
                        logging.warning(f"Error in page {count//1000} for {filename}: {e}")

        except Exception as e:
            time.sleep(60)
            logging.warning("Macro error:" + str(e))
            end_time = item['created_at']
            filename = filename + "_res"
            continue

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    