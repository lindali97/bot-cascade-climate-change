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
from flatten_json import flatten

def json_to_df(file):
    file = json.loads(file)
    json_list = list(file.values())
    list_flattened = [flatten(d) for d in json_list]
    flat_tweet = pd.DataFrame(list_flattened)
    return flat_tweet

def column_unifier(col_list, df):
    col_not_available = [i for i in col_list if i not in list(df)]
    df[col_not_available] = len(col_not_available) * [None]
    df = df[col_list]
    df = df.replace({np.nan: None})
    return df

col_list_tweet = ['text', 'conversation_id', 'author_id', 'id', 'created_at',
       'public_metrics_retweet_count', 'public_metrics_reply_count',
       'public_metrics_like_count', 'public_metrics_quote_count',
       'possibly_sensitive', 'author_id_hydrate_id',
       'referenced_tweets_0_type',
       'referenced_tweets_0_id', 
       'referenced_tweets_0_id_hydrate_author_id',
       'in_reply_to_user_id', 'in_reply_to_user_id_hydrate_username',
       'id_hydrate_text',
       'id_hydrate_possibly_sensitive', 'id_hydrate_created_at',
       'id_hydrate_id', 'id_hydrate_conversation_id',
       'id_hydrate_public_metrics_retweet_count',
       'id_hydrate_public_metrics_reply_count',
       'id_hydrate_public_metrics_like_count',
       'id_hydrate_public_metrics_quote_count',
       'id_hydrate_referenced_tweets_0_type',
       'id_hydrate_referenced_tweets_0_id', 'id_hydrate_author_id',
       'id_hydrate_in_reply_to_user_id', 'conversation_id_hydrate_text',
       'conversation_id_hydrate_possibly_sensitive',
       'conversation_id_hydrate_created_at', 'conversation_id_hydrate_id',
       'conversation_id_hydrate_conversation_id',
       'conversation_id_hydrate_public_metrics_retweet_count',
       'conversation_id_hydrate_public_metrics_reply_count',
       'conversation_id_hydrate_public_metrics_like_count',
       'conversation_id_hydrate_public_metrics_quote_count',
       'conversation_id_hydrate_author_id',
       'in_reply_to_user_id_hydrate_location',
       'referenced_tweets_0_id_hydrate_geo_place_id',
       'conversation_id_hydrate_referenced_tweets_0_type',
       'conversation_id_hydrate_referenced_tweets_0_id', 'geo_place_id',
       'conversation_id_hydrate_geo_place_id', 'id_hydrate_geo_place_id',
       'referenced_tweets_1_type', 'referenced_tweets_1_id',
       'referenced_tweets_1_id_hydrate_author_id']

if __name__ == "__main__":
   

    QUERY = argv[1]
    filename = argv[2]
    
    EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id'
    TWEET_FIELDS = 'created_at,author_id,public_metrics,conversation_id,geo,in_reply_to_user_id,possibly_sensitive'
    USER_FIELDS = 'created_at,description,location,protected,public_metrics,verified,withheld'
    
    logging.basicConfig(level = logging.INFO, datefmt = '%a, %d %b %Y %H:%M:%S',
                    format ='%(asctime)s %(levelname)s %(message)s',
                    filename = filename + ".log")
    
    auth = load_token("sql_auth.txt")
    db_user = auth[0]
    db_pass = auth[1]
    db_endpoint='127.0.0.1'
    port=5432
    dbname='twitter_bots'

    engine_string = "postgresql+psycopg2://%s:%s@%s:%d/%s" % (db_user, db_pass, db_endpoint, port, dbname)
    engine = sqlalchemy.create_engine(engine_string)

    while True:
        try:
            consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token = load_token('twitter_auth')
            api = TwitterAPI(consumer_key, consumer_secret, auth_type='oAuth2', api_version='2')
            
            r = api.request('tweets/search/stream/rules', {'add': [{'value':QUERY}]})
            print(r.status_code)
            logging.info("RULE ADDED....")
            if r.status_code != 201: exit()
                
            r = api.request('tweets/search/stream/rules', method_override='GET')
            logging.info("RULE ADDED AND CONFIRMED....")
            if r.status_code != 200: exit()
                
            r = api.request('tweets/search/stream', {'expansions': EXPANSIONS,
                                                     'tweet.fields': TWEET_FIELDS,
                                                     'user.fields': USER_FIELDS,},
                            hydrate_type=HydrateType.APPEND)
            
            logging.info(f'START...')
            
            if r.status_code != 200: 
                logging.exception("Error in streaming tweets!")
                raise ValueError('error in streaming tweets!')
            else:
                for item in r:
                    json_string = json.dumps(item, indent=2)
                    flat_tweet = json_to_df(json_string)
                    tweet_item = column_unifier(col_list_tweet, flat_tweet)
                    
                    tweet_item.to_sql('tweet_table_cop26', engine, if_exists='append', index = False)

        except Exception as e:
            logging.warning("Error:" + str(e))
            time.sleep(60)
            
            #end_time = item['created_at']
            #filename = filename + "_res"
            continue

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    