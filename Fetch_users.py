################################################################################
##      Fetch_Users                                                           ##
##      Dan McGregor                                                          ##
################################################################################
##      Last Updated: June 2, 2018                                            ##
################################################################################
## This file looks up each user on twitter using twitter's API and records    ##
## the information in a csv file                                              ##
################################################################################


import tweepy
import time
import os

# Reads in the path for the data files
import DataPath
DFPath, TweetPath = DataPath.getPaths()

# Sets the separation for the csv file, using tabs because some fields in the
# user information may contain commas
sep = '\t'

# Reads in the tokens that will be needed to connect to the twitter API
import AuthTokens
consumer_token, consumer_secret, access_token, access_token_secret = AuthTokens.getTokens()

# Sets up the authentication and connects to the API
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# This function will record all the required information about a user and return
# it in a tab separated line. Some fields may be missing, other need to be
# converted to strings, and a few might contain newline characters that need
# to be replaced by \\n to keep the csv file formatted correctly. Note: some
# fields may contain unicode
def get_user_info(username):
	"""
	username (str) = username of a twitter account

	Looks up a user on twitter and records:
	the url of their background image,
	the url of their profile image,
	their location,
	their followers count,
	their following count,
	their number of tweets,
	their description,
	and their name.

	This is returned as a tab separated line.
	"""
	# Request user object from the twitter API corresponding to the username
	user = api.get_user(username)

	# Debug print statement to make sure program is running correctly.
	# 'usercount' is a 4 character string counting the number of users that
	# have been read in.
	print usercount + " Accessing user: '" + username +"'"

	# Begins assembling the line to return
	line = username
	line += sep + 'Active'

	# user.profile_background_image_url_https may be None
	if user.profile_background_image_url_https:
		line += sep + user.profile_background_image_url_https
	else:
		line += sep

	# user.profile_image_url_https may be None
	if user.profile_image_url_https:
		line += sep + user.profile_image_url_https
	else:
		line += sep
	# user.location may be None, and may contain newline characters
	if user.location:
		line += sep + user.location.replace('\n','\\n')
	else:
		line += sep
	# The following 3 fields are ints which must be converted to strings
	line += sep + str(user.followers_count)
	line += sep + str(user.friends_count)
	line += sep + str(user.statuses_count)

	# user.description may be None, and may contain newline characters
	if user.description:
		line += sep + user.description.replace('\n','\\n')
	else:
		line += sep

	# user.name may be None, and may contain newline characters
	if user.name:
		line += sep + user.name.replace('\n','\\n')
	else:
		line += sep

	# user.location may be None
	if user.lang:
		line += sep + user.lang
	else:
		line += sep

	# user.created_at is a datetime object which must be converted to a string
	line += sep + str(user.created_at)
	return line

# Creates the csv file and initializes the first line as a header
f = open(DFPath + 'User_info.csv', 'w+')
line = 'Username'
line += sep + 'Status'
line += sep + 'Background'
line += sep + 'Image'
line += sep + 'Location'
line += sep + 'Followers'
line += sep + 'Friends'
line += sep + 'Tweets'
line += sep + 'Description'
line += sep + 'Name'
line += sep + 'Language'
line += sep + 'Created'
f.write(line + '\n')
f.close()

# Open the csv file to be appended to, and open an error log to record any
# unexpected errors that occur along with the associated username
f = open('User_info.csv', 'a+')
g = open('Error_log.txt', 'w+')

# 'i' is a counter that increases with each user requested, used in the debug
# print statements. 'k' is a counter that decreases with each user requested,
# used to keep track of the rate limit to prevent API requests from being
# rejected. Here, 'k' is initialized to the number of requests remaining before
# the rate limit is reached
i = 1
k = api.rate_limit_status()['resources']['users']['/users/show/:id']['remaining']

# Loops through every user, attempts to 'get_user_info' and record to the csv
# file, has some logic for handling the rate limit as well as various errors
for file_name in sorted(os.listdir(TweetPath)):

	# 'usercount' is used in the debug print statements
	usercount = format(i, '04d')

	# Checks to see if rate limit has been reached. If it has, the program waits
	# 15 minutes, resets the value of 'k', and then continues
	if k == 0:
		print "Rate limit reached, waiting 15 minutes"
		time.sleep(15*60)
		k = api.rate_limit_status()['resources']['users']['/users/show/:id']['remaining']

	# Increases 'i' and decrease 'k' for each attempts to call the API
	i += 1
	k -= 1

	# Gets the 'username' from the 'file_name', try to 'get_user_info', and
	# append the line containing that info to the csv file (in unicode)
	username = file_name[:-11]
	try:
		line = get_user_info(username)
		f.write(line.encode('utf-8') + '\n')

	# If tweepy returns an error, there are two possibilities to
	# check for explicitly, and a catch block for any unexpected error
	except tweepy.TweepError as e:

		# '63' is the code for a suspended user. No other information can be
		# retreived from twitter in this case
		if '63' in e.response.text:
			print usercount + " Warning: '" + username +"' is banned"
			line = username
			line += sep + 'Banned'
			line += sep*10
			f.write(line + '\n')

		# '50' is the code for a missing user. No other information can be
		# retreived from twitter in this case
		elif '50' in e.response.text:
			print usercount + " Warning: '" + username +"' is deleted"
			line = username
			line += sep + 'Deleted'
			line += sep*10
			f.write(line + '\n')

		# If an unexpected error occurs, prints the error message and write it
		# to the Error_log file
		else:
			print 'Something went wrong:' + e.response.text
			g.write(username + ': ' + e.response.text + '\n')

# Closes the files when finished
f.close()
g.close()
