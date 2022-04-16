#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os.path
import os
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import time
import datetime
from io import StringIO
from twython import Twython
import random

global api
api = {
	'key'          : "uVAbgGZ9q5OS7EZ04zQjKNsEk",
	'secret'       : "uK3Zvxc5dtmzK4ezvX6g3FHfkRSZCHbAuO75UnNtLZAZ0ho2Jd",
	'token'        : "618974114-qkkFbpFoxq8SVd2wp961iVbLtiZ1CQJNK0NSfxkf",
	'token_secret' : "epTytbM7CFxq5J7mdBS26WhK8yIDdfeisi6wSG9eT6goc"
}

global twitter
twitter = Twython(
	api['key'],
	api['secret'],
	api['token'],
	api['token_secret']
)

# let's make things fun by using randomly selected messages.
messages = {
	'lost' : [
		"You unfollowed me. My @Raspberry_Pi noticed.",
		"You unfollowed me. I don't appreciate that.",
		"Why did you unfollow me? Please fill in this survey: https://onedrive.live.com/redir?page=survey&resid=643D972B6E5A6AE7!8438&authkey=!ACGh2UHjtuL-xvk&ithint=file%2cxlsx"
	],
	'new' : [
		"Thanks for following me. - This is an automated message sent from my @Raspberry_Pi.",
		"Thanks for following me. Yes, I did write a program to send this tweet.",
		"Thanks for following me. Check out the program that sent this tweet at: https://gist.github.com/MaxCampman/0a6e92911c206bb72232"
	]
}

global message
message = {
	'lost' : "You unfollowed me. My @Raspberry_Pi noticed.",
	'new'  : "Thanks for following me. - This is an automated message sent from my @Raspberry_Pi."
}


# select the random message for 'lost' and 'new'.
random.seed()
message['lost'] = messages['lost'][random.randint(0, len(messages['lost']) - 1)]
message['new'] = messages['new'][random.randint(0, len(messages['new']) - 1)]

global theFile
theFile = "followers.txt"

def log(text):
	# log text to a file. used to save the result of the program
	logFile = open("followerLog.txt", "a")
	logFile.write(text + "\n")
	logFile.close()

def get_followers(SCREEN_NAME, COUNT):
	next_cursor = -1
	
	# get the list of twitter followers
	twitter_followers = twitter.get_followers_list(
		screen_name=SCREEN_NAME,
		count=COUNT,
		cursor=next_cursor
	)
	
	# create local variable followers and assign it to an empty array
	followers = []
	
	# get the list of followers and put them into the followers array
	for follower in twitter_followers["users"]:
		followers.append(
			follower["screen_name"]
		)
		next_cursor = twitter_followers["next_cursor"]
	
	# return the array of followers
	return followers


# create the follower lists that are to be compared
global follower_list
follower_list = {
	'old' : [],
	'new' : []
}

# set current_followers to the list of current followers
follower_list['new'] = get_followers("@0xpibbles", 2000) # change MaxCampman to your screen name

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
follower_list['old'] = follower_file.readlines()

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

# def image_write(image, string, colour):
# 	# open the image
# 	img = Image.open(image)
	
# 	# select the font
# 	font = ImageFont.truetype("/home/pi/twitter/fonts/SourceCodePro-Semibold.ttf", 20)
	
# 	# prepare to draw on to the image
# 	draw = ImageDraw.Draw(img)
	
# 	# draw the text 10 pixels across and 10 pixels down
# 	draw.text(
# 		(10, 10),
# 		string,
# 		colour,
# 		font=font
# 	)
# 	draw = ImageDraw.Draw(img)
	
# 	image_io = StringIO.StringIO()

# 	img.save(image_io, format='PNG')
# 	image_io.seek(0)
	
# 	return image_io

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
		# write to the image
		# raspi_img = image_write(
		# 	"raspberry-pi.jpg",
		# 	"@" + unfollower + " unfollowed @---.",
		# 	(255, 255, 255)
		# )
		# raspi_img.seek(0)
		
		# send the unfollower a message to let them know that you are on to them
		# twitter.update_status_with_media(
		# 	status="@" + unfollower + " " + message['lost'],
		# 	media=raspi_img
		# )
		
		# log the loss of a follower
		log("Lost follower: " + unfollower)
		
		# close the image
		# raspi_img.close()
		
	for follower in change[1]:
		# write to the image
		# raspi_img = image_write(
		# 	"raspberry-pi.jpg",
		# 	"@" + follower + " followed @---.",
		# 	(255, 255, 255)
		# )
		# raspi_img.seek(0)
		
		
		# send the follower a friendly welcome message
		# twitter.update_status_with_media(
		# 	status="@" + follower + " " + message['new'],
		# 	media=raspi_img
		# )
		
		# log the gain of a follower
		log("New follower: " + follower)
		
		# close the image
		# raspi_img.close()
	
# finish off log
log("\n" + "========================" + "\n\n")