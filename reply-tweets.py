#!/usr/bin/env python

import tweepy
from keys import api

CONSUMER_KEY = api['key']
CONSUMER_SECRET = api['secret']
ACCESS_TOKEN = api['token']
ACCESS_TOKEN_SECRET = api['token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

twts = api.search_tweets(q="asdfghjklhihellosez")

t = ['asdfghjklhihellosez']

for s in twts:
    for i in t:
        if i == s.text:
            print(s.user.screen_name)
            sn = s.user.screen_name
            m = "@%s Hello!" % (sn)
            print(m)
            print(s.id)
            s = api.update_status(m, s.id)