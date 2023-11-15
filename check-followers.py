#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os.path
import argparse
from dotenv import load_dotenv
import os
import requests
from requests_oauthlib import OAuth1
import time
import tweepy
from TwitterAPI import TwitterAPI
from twython import Twython

load_dotenv()
API_KEY=os.environ['TWITTER_API_KEY']
API_SECRET=os.environ['TWITTER_API_SECRET']
API_TOKEN=os.environ['TWITTER_API_TOKEN']
API_TOKEN_SECRET=os.environ['TWITTER_API_TOKEN_SECRET']

oauth = OAuth1(API_KEY,
               client_secret=API_SECRET,
               resource_owner_key=API_TOKEN,
               resource_owner_secret=API_TOKEN_SECRET)

parser = argparse.ArgumentParser(description = "Parse the arguments", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--twitter_username", required=True, help = "Twitter Username")
args = parser.parse_args()
twitter_username = args.twitter_username


def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    response = requests.get(url, auth=oauth)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    data = response.json()
    return data['data']['id']

def get_following(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}/following"
    response = requests.get(url, auth=oauth)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")
    data = response.json()
    following = [user['username'] for user in data['data']]
    return following

# Define the username you're interested in
username = '0xpibs'

# Get the user ID for the specified username
user_id = get_user_id(username)

# Get the list of users the specified user is following
following = get_following(user_id)
print(following)





global twitter
twitter = Twython(API_KEY, API_SECRET, API_TOKEN, API_TOKEN_SECRET, api_version='2')


global theFile
theFile = "followers/%s_followers.txt" % twitter_username

def log(text):
	# log text to a file. used to save the result of the program
	logFile1 = open("followers/%s_followerLog.txt" % twitter_username, "a")
	logFile1.write(text + "\n")
	logFile1.close()
	
	logFile2 = open("followers/followerLog.txt", "a")
	logFile2.write(text + "\n")
	logFile2.close()



# def get_followers(SCREEN_NAME):
	
# 	# get the list of twitter followers
# 	# twitter_followers = twitter.get_followers_ids(screen_name=SCREEN_NAME)
# 	twitter_followers = twitter.get_friends_ids(screen_name=SCREEN_NAME)
	
# 	# create local variable followers and assign it to an empty array
# 	followers = []
	
# 	# get the list of followers and put them into the followers array
# 	for x in twitter_followers["ids"]:
# 		try: 
# 			data = twitter.show_user(user_id=x)
# 		except (TwythonError, e):
# 			if e.error_code == 403:
# 				pass 
# 		followers.append(
# 			data["screen_name"]
# 		)
	
# 	# return the array of followers
# 	return followers




# create the follower lists that are to be compared
global follower_list
follower_list = {
	'old' : [],
	'new' : []
}

#global twitter_username
#twitter_username = "0xpibbles"
# set current_followers to the list of current followers
follower_list['new'] = get_followers(twitter_username) 

# open/create the followers.txt file
follower_file = open(theFile, "a+")

# if the followers.txt file does not exist or is empty, write the array of followers into the file
if os.path.isfile(theFile) == False or os.stat(theFile)[6] == 0:
	# loop through the list of followers and write them to the text file
	for follower in follower_list['new']:
		follower_file.write(follower + "\n")
		
	print("Wrote to file")

	# save the updates that were made to the follower file
	follower_file.close()
	
	# reopen the file so that it can be used again
	follower_file = open(theFile, "r+")

# take the information from the followers.txt file and put it into the list follower_list['old']
#follower_list['old'] = follower_file.readlines()
follower_file.seek(0)
follower_list["old"] = follower_file.readlines()

x = len(follower_list['old'])

# remove the new line markers from the items in the follower_list['old'] array
for i in range(0, x):
	follower_list['old'][i] = follower_list['old'][i].rstrip()

follower_file.seek(0)
follower_file.truncate()

# write the updated list of followers back into the followers.txt file
for follower in follower_list['new']:
	follower_file.write(follower + "\n")

print("Updated file")

# save the now updated file
follower_file.close()

def inOther(name, list):
	# check the name against all followers in the other list
	
	x = len(list)
	
	for i in range(0, x):
		# if found return True and position that it was found in
		if name == list[i]:
			return [True, i]
		
	# otherwise, return False
	return [False, -1]

def checkBoth(old_list, new_list):
	i = 0
	
	x = len(old_list)
	
	# go through list of old followers
	while i < x:
		isInOther = inOther(old_list[i], new_list)
		# if the name is in the other list ...
		if isInOther[0] == True:
			# ... delete it from both lists
			del old_list[i]
			del new_list[isInOther[1]]
			# set x to the new length of the old list
			x = len(old_list)
		else:
			i += 1
	
	# lists that are left are the unfollowers and followers respectively
	return [old_list, new_list]


# checks to see if the list of followers has actually changed at all
if follower_list['new'] == follower_list['old']:
	print("No change.")
else:
	# start log, showing the date and time of the program running
	log(
		time.strftime("%Y/%m/%d %H:%M:%S") +
		"\n" + "========================" + "\n"
	)

	# set change to returned lists of followers
	change = checkBoth(follower_list['old'], follower_list['new'])
	print(str(change))
	
	for unfollower in change[0]:
		
		# log the loss of a follower
		log(twitter_username + " lost follower: " + unfollower)
		
		
	for follower in change[1]:
		
		
		# log the gain of a follower
		log(twitter_username + " new follower: " + follower)
		
	
# finish off log
log("\n" + "========================" + "\n\n")