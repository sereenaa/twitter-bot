#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os.path
import os
import time
import datetime
from twython import Twython
import argparse
from keys import api

parser = argparse.ArgumentParser(description = "Parse the arguments", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--twitter_username", required=True, help = "Twitter Username")
args = parser.parse_args()
twitter_username = args.twitter_username

global twitter
twitter = Twython(
	api['key'],
	api['secret'],
	api['token'],
	api['token_secret']
)



global theFile
theFile = "following/%s_following.txt" % twitter_username

def log(text):
	# log text to a file. used to save the result of the program
    logFile1 = open("following/%s_followingLog.txt" % twitter_username, "a")
    logFile1.write(text + "\n")
    logFile1.close()

    logFile2 = open("following/followingLog.txt", "a")
    logFile2.write(text + "\n")
    logFile2.close()

def get_following(SCREEN_NAME):
	
	# get the list of twitter following
	twitter_following = twitter.get_friends_ids(
		screen_name=SCREEN_NAME
	)
	
	# create local variable following and assign it to an empty array
	following = []
	
	# get the list of followings and put them into the followings array
	for x in twitter_following["ids"]:
		data = twitter.show_user(user_id=x)
		following.append(
			data["screen_name"]
		)
	
	# return the array of followings
	return following


# create the following lists that are to be compared
global following_list
following_list = {
	'old' : [],
	'new' : []
}

#global twitter_username
#twitter_username = "0xpibbles"
# set current_followings to the list of current followings
following_list['new'] = get_following(twitter_username) 

# open/create the followings.txt file
following_file = open(theFile, "a+")

# if the followings.txt file does not exist or is empty, write the array of followings into the file
if os.path.isfile(theFile) == False or os.stat(theFile)[6] == 0:
	# loop through the list of following and write them to the text file
	for following in following_list['new']:
		following_file.write(following + "\n")
		
	print("Wrote to file")

	# save the updates that were made to the following file
	following_file.close()
	
	# reopen the file so that it can be used again
	following_file = open(theFile, "r+")

# take the information from the following.txt file and put it into the list following_list['old']
#follfollowing_listower_list['old'] = following_file.readlines()
following_file.seek(0)
following_list["old"] = following_file.readlines()

x = len(following_list['old'])

# remove the new line markers from the items in the following_list['old'] array
for i in range(0, x):
	following_list['old'][i] = following_list['old'][i].rstrip()

following_file.seek(0)
following_file.truncate()

# write the updated list of followings back into the followings.txt file
for following in following_list['new']:
	following_file.write(following + "\n")

print("Updated file")

# save the now updated file
following_file.close()

def inOther(name, list):
	# check the name against all followings in the other list
	
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
	
	# go through list of old followings
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
	
	# lists that are left are the unfollowing and following respectively
	return [old_list, new_list]


# checks to see if the list of following has actually changed at all
if following_list['new'] == following_list['old']:
	print("No change.")
else:
	# start log, showing the date and time of the program running
	log(
		time.strftime("%Y/%m/%d %H:%M:%S") +
		"\n" + "========================" + "\n"
	)

	# set change to returned lists of following
	change = checkBoth(following_list['old'], following_list['new'])
	print(str(change))
	
	for unfollowing in change[0]:
		
		# log the loss of a following
		log(twitter_username + " unfollowed: " + unfollowing)
		
		
	for following in change[1]:
		
		
		# log the gain of a following
		log(twitter_username + " followed: " + following)
		
	
# finish off log
log("\n" + "========================" + "\n\n")