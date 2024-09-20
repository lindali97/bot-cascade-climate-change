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

from load_token import load_token

from sys import argv
import logging
import os

from TwitterAPI import TwitterAPI, TwitterOAuth, HydrateType, TwitterPager    

def sql_query_to_data_frame(query):
    connection = engine.connect()
    df = pd.read_sql_query(sqlalchemy.text(query), connection)
    connection.close()
    return df

if __name__ == "__main__":
    
    auth = load_token("sql_auth.txt")
    db_user = auth[0]
    db_pass = auth[1]
    db_endpoint='127.0.0.1'
    port=5432
    dbname='twitter_bots'

    engine_string = "postgresql+psycopg2://%s:%s@%s:%d/%s" % (db_user, db_pass, db_endpoint, port, dbname)
    engine = sqlalchemy.create_engine(engine_string)

    
    filename = argv[1]

    #USER_FIELDS = 'created_at,description,location,protected,public_metrics,verified,withheld'
    
    logging.basicConfig(level = logging.INFO, datefmt = '%a, %d %b %Y %H:%M:%S',
                    format ='%(asctime)s %(levelname)s %(message)s',
                    filename = filename + ".log")

    consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token = load_token('twitter_auth')
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, api_version='1.1')
    
    
    for i in range(2800000,4000000, 200000):
        query = f"SELECT DISTINCT author_id FROM (SELECT author_id FROM tweet_table_blm LIMIT 200000 OFFSET {i}) AS uids"
    
        users = sql_query_to_data_frame(query)
        users = list(users.author_id)
    
        users_new = []
        user_temp = []
        for count,item in enumerate(users):
            user_temp.append(item)
            if (count+1) % 100 != 0 and count != len(users)-1:
                continue
            else:
                uid_string = ','.join(user_temp)
                users_new.append(uid_string)
                user_temp = []

        error_item = {}

        for count, uids in enumerate(users_new):
            time.sleep(2)
            r = api.request('users/lookup',
                            {'user_id':uids})
            output = []
            for item in r:
                output.append(item)
            with open(filename + str(i) + str(count) + '.json', 'w', encoding='utf-8') as f:
                try:
                    json.dump(output, f, indent=2)
                except Exception as e:
                    error_item[count] = item
                    logging.warning(f"Error : {e}")
                    pass

        with open(filename + 'error_id.json', 'w', encoding='utf-8') as file:
            json.dump(error_item, file, indent=2)
                        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    