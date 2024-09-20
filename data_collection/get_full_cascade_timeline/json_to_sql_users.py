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
    list_flattened = [flatten(d) for d in file]
    flat_tweet = pd.DataFrame(list_flattened)
    return flat_tweet


flat_user = json_to_df(json_file)


col_list_users = ['id', 'created_at', 'protected', 'verified', 'name', 'screen_name',
                     'followers_count', 'friends_count', 'statuses_count','listed_count','favourites_count',
                      'geo_enabled','location','description','lang','default_profile','default_profile_image',
                      "profile_use_background_image"]


user_item = flat_user[col_list_users]

user_item['id'] = [str(i) for i in user_item['id']]


user_item.to_sql('user_table_blm', engine, if_exists='append', index = False)
engine.dispose()
