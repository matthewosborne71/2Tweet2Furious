import tweepy
import time
import os

sep = '\t'

f = open('AuthTokens.txt', 'r')
(consumer_token, consumer_secret, access_token, access_token_secret) = f.readlines()
f.close()

consumer_token = consumer_token[:-1]
consumer_secret = consumer_secret[:-1]
access_token = access_token[:-1]

f = open('DataPath.txt', 'r')
path = f.readline()
f.close()

path = path[:-1]

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def get_user_info(username):
	user = api.get_user(username)
	print "Accessing user: '" + username +"'"

	line = username
	line += sep + 'Active'
	if user.profile_background_image_url_https:
		line += sep + user.profile_background_image_url_https
	else:
		line += sep
	if user.profile_image_url_https:
		line += sep + user.profile_image_url_https
	else:
		line += sep
	if user.location:
		line += sep + user.location
	else:
		line += sep
	line += sep + str(user.followers_count)
	line += sep + str(user.friends_count)
	line += sep + str(user.statuses_count)
	if user.description:
		line += sep + user.description
	else:
		line += sep
	if user.name:
		line += sep + user.name
	else:
		line += sep
	if user.lang:
		line += sep + user.lang
	else:
		line += sep
	line += sep + str(user.created_at)
	return line

f = open('User_info.csv', 'w+')
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
f.write(line)
f.close()

f = open('User_info.csv', 'a+')

g = open('Error_log.txt', 'w+')


for file_name in os.listdir(path):
	username = file_name[:-11]
	try:
		line = get_user_info(username)
		f.write(line.encode('utf-8') + '\n')

	except tweepy.RateLimitError:
		print "Rate limit reached, waiting 15 minutes"
		time.sleep(60*15)

		line = get_user_info(username)
		f.write(line.encode('utf-8') + '\n')

	except tweepy.TweepError as e:
		if '63' in e.response.text:
			print "Warning: '" + username +"' is banned"
			line = username
			line += sep + 'Banned'
			line += sep*10
			f.write(line + '\n')

		elif '50' in e.response.text:
			print "Warning: '" + username +"' is deleted"
			line = username
			line += sep + 'Deleted'
			line += sep*10
			f.write(line + '\n')

		else:
			print 'Something went wrong:' + e.response.text
			g.write(username + ': ' + e.response.text)

f.close()
g.close()
