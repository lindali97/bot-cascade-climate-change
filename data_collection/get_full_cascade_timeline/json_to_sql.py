#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 00:59:00 2021

@author: lindali

import some very large Twitter json dumps into SQL database.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import datetime as dt
import json
import ijson
import math


import sqlalchemy
import psycopg2

import os
from sys import argv
import logging

from load_token import load_token
from flatten_json import flatten


def json_to_df(json_file):
    with open(json_file) as f:
        file = json.load(f)
    json_list = list(file.values())
    flat_tweet = pd.json_normalize(json_list)
    return flat_tweet

auth = load_token("sql_auth.txt")
db_user = auth[0]
db_pass = auth[1]
db_endpoint='127.0.0.1'
port=5432
dbname='twitter_bots'

engine_string = "postgresql+psycopg2://%s:%s@%s:%d/%s" % (db_user, db_pass, db_endpoint, port, dbname)
engine = sqlalchemy.create_engine(engine_string)

json_file = argv[1]

def json_to_df(json_file):
    with open(json_file) as f:
        file = json.load(f)
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


flat_tweet = json_to_df(json_file)

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

col_list_user = ['author_id','author_id_hydrate_created_at', 'author_id_hydrate_protected',
       'author_id_hydrate_verified', 'author_id_hydrate_name',
       'author_id_hydrate_public_metrics_followers_count',
       'author_id_hydrate_public_metrics_following_count',
       'author_id_hydrate_public_metrics_tweet_count',
       'author_id_hydrate_public_metrics_listed_count',
       'conversation_id_hydrate_public_metrics_like_count',
       'author_id_hydrate_username', 'author_id_hydrate_location',
       'author_id_hydrate_description']

col_list_users_new = ['id', 'created_at', 'protected', 'verified', 'name', 
                     'followers_count', 'following_count', 'tweet_count','listed_count','favourite_count',
                     "username", 'location','description']

tweet_item = column_unifier(col_list_tweet, flat_tweet)
#user_item = flat_tweet[col_list_user]
#user_item.columns = col_list_users_new

tweet_item.to_sql('tweet_table_temp', engine, if_exists='replace', index = False)
query_to_final = '''
INSERT INTO tweet_table_blm
                      (text, conversation_id, author_id, id, created_at,public_metrics_retweet_count, public_metrics_reply_count,
       public_metrics_like_count, public_metrics_quote_count,possibly_sensitive, author_id_hydrate_id,referenced_tweets_0_type,
       referenced_tweets_0_id, referenced_tweets_0_id_hydrate_author_id,
       in_reply_to_user_id, in_reply_to_user_id_hydrate_username,id_hydrate_text,
       id_hydrate_possibly_sensitive, id_hydrate_created_at,
       id_hydrate_id, id_hydrate_conversation_id,
       id_hydrate_public_metrics_retweet_count,
       id_hydrate_public_metrics_reply_count,
       id_hydrate_public_metrics_like_count,
       id_hydrate_public_metrics_quote_count,
       id_hydrate_referenced_tweets_0_type,
       id_hydrate_referenced_tweets_0_id, id_hydrate_author_id,
       id_hydrate_in_reply_to_user_id, conversation_id_hydrate_text,
       conversation_id_hydrate_possibly_sensitive,
       conversation_id_hydrate_created_at, conversation_id_hydrate_id,
       conversation_id_hydrate_conversation_id,
       conversation_id_hydrate_public_metrics_retweet_count,
       conversation_id_hydrate_public_metrics_reply_count,
       conversation_id_hydrate_public_metrics_like_count,
       conversation_id_hydrate_public_metrics_quote_count,
       conversation_id_hydrate_author_id,
       in_reply_to_user_id_hydrate_location,
       referenced_tweets_0_id_hydrate_geo_place_id,
       conversation_id_hydrate_referenced_tweets_0_type,
       conversation_id_hydrate_referenced_tweets_0_id, geo_place_id,
       conversation_id_hydrate_geo_place_id, id_hydrate_geo_place_id,
       referenced_tweets_1_type, referenced_tweets_1_id,
       referenced_tweets_1_id_hydrate_author_id)
                     SELECT * FROM tweet_table_temp
                     '''
                     
conn = engine.connect()
conn.execute(query_to_final)
conn.close()
engine.dispose()

"""
user_item.to_sql('user_table_temp', engine, if_exists='replace', index = False)


query_to_final = '''INSERT INTO user_table_xr_impossible
                      (id, created_at, protected, verified, name, followers_count, following_count,
                      tweet_count, listed_count, username, location, description)
                     SELECT * FROM user_table_temp
                     ON CONFLICT (id) 
                     DO NOTHING;'''


conn = engine.connect()
conn.execute(query_to_final)

"""


