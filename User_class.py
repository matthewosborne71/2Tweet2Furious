################################################################################
##      User_class                                                            ##
##      Dan McGregor                                                          ##
################################################################################
##      Last Updated: June 2, 2018                                            ##
################################################################################
## This file defines a class for twitter users and methods for retreving data ##
## about them from the various csv files                                      ##
################################################################################


from csv import DictReader

# Reads in the path for the data files
import DataPath
DFPath, TweetPath = DataPath.getPaths()

# Defines the user class and its methods
class User:
	"""
	username (str or unicode): username of a user in the database

	Creates an instance of a user class for twitter user in the database.
	Raises an error if the user cannot be found.

	Contains the following methods:
	user.get(attribute),
	user.list_attributes(),
	user.get_top_RTs(count),
	user.get_top_HTs(count),
	user.get_top_Ments(count)
	and user.compare(other)
	"""
	def __init__(self, username):

		# Raises a TypeError if the username is not a string or unicode
		if (type(username) is not str) and (type(username) is not unicode):
			raise TypeError('Username should be a string or unicode.')

		# Sets username to the string entered
		self.username = username

		# Reads attributes of the user from User_info.csv
		with open(DFPath + 'User_info.csv') as csvfile:
			reader = DictReader(csvfile, delimiter = '\t')
			for row in reader:
				if row['Username'] == username:
					self.attributes = row
					break

			# Raises a ValueError if the username is not in the database
			else:
				raise ValueError('This username is not in the database.')

		# Reads statistics of the user from User_info.csv
		with open(DFPath + 'TweetDF.csv') as csvfile:
			reader = DictReader(csvfile, delimiter = ',')
			for row in reader:
				if row['User'] == username:
					self.attributes.update(row)
					break

			# Raises a ValueError if the username is not in the database
			else:
				raise ValueError('This username is not in the database.')


	# When the User instance is converted to a str, the username is returned
	def __str__(self):
		return self.username

	# Defines a getter method for the attributes of the user
	def get(self, attribute):
		"""
		attribute (str or unicode): name of an attribute of the user

		Returns the specified attribute of the user as a unicode string.
		Argument is not case sensitive.
		"""
		if (type(attribute) is not str) and (type(attribute) is not unicode):
			raise TypeError('Attribute should be a string or unicode.')

		attribute = attribute.capitalize()
		try:
			if self.attributes[attribute] == '':
				return 'N/A'
			return self.attributes[attribute].replace('\\n', '\n').decode('utf-8')
		except KeyError:
			raise ValueError("Database does not contain the attribute: '" + attribute + "'.")

	# Lists the possible attributes of the user
	def list_attributes(self):
		"""
		Returns a list of all possible attributes a user may have.
		"""
		return self.attributes.keys()

	# Gets the top RTs
	def get_top_RTs(self, count = 5):
		"""
		count (int): number of top RTs to return (default is 5, must be <= 10)

		Returns the top few twitter users retweeted by this user as a list of
		dicts. Each dict contains two strings, the user retweeted and the
		number of times they were retweeted.

		If the user does not have enough retweets, the list returned may be
		shorter than expected, and if no retweets can be found then the list
		is a single dict with a message that there were not enough retweets
		along with an empty string.

		Keys of the dictionaries are:
		RTUser
		TimesRTed
		"""
		if type(count) is not int:
			raise TypeError('Count should be an integer.')
		if count > 10:
			raise ValueError('Count cannot be greater than 10.')

		RT_list = []
		with open(DFPath + 'UserRTsShort.csv') as csvfile:
			reader = DictReader(csvfile, delimiter = ',')
			for row in reader:
				if (row['User'] == self.username) and (len(RT_list) < count):
					RT_list.append({'RTUser':row['RTUser'], 'TimesRTed':row['TimesRTed']})
				elif (row['User'] == self.username) and (len(RT_list) == count):
					break
				elif (row['User'] != self.username) and (len(RT_list) > 0):
					break
			else:
				if len(RT_list) == 0:
					RT_list = [{'RTUser':self.username + ' did not have enough retweets.', 'TimesRTed':''}]
		return RT_list

	# Gets the top HTs
	def get_top_HTs(self, count = 5):
		"""
		count (int): number of top HTs to return (default is 5, must be <= 10)

		Returns the top few hashtags used by this user as a list of
		dicts. Each dict contains two strings, the hashtag used and the
		number of times it was used.

		If the user did not use enough hashtags, the list returned may be
		shorter than expected, and if no hashtags can be found then the list
		is a single dict with a message that there were not enough hashtags
		along with an empty string.

		Keys of the dictionaries are:
		Hashtag
		TimesUsed
		"""
		if type(count) is not int:
			raise TypeError('Count should be an integer.')
		if count > 10:
			raise ValueError('Count cannot be greater than 10.')

		HT_list = []
		with open(DFPath + 'WhatHashtagsCondensed.csv') as csvfile:
			reader = DictReader(csvfile, delimiter = ',')
			for row in reader:
				if (row['User'] == self.username) and (len(HT_list) < count):
					HT_list.append({'Hashtag':row['Hashtag'], 'TimesUsed':row['TimesUsed']})
				elif (row['User'] == self.username) and (len(HT_list) == count):
					break
				elif (row['User'] != self.username) and (len(HT_list) > 0):
					break
			else:
				if len(HT_list) == 0:
					HT_list = [{'Hashtag':self.username + ' did not have enough hashtags.', 'TimesUsed':''}]
		return HT_list

	# Gets the top Ments
	def get_top_Ments(self, count = 5):
		"""
		count (int): number of top Ments to return (default is 5, must be <= 10)

		Returns the top few twitter users mentioned by this user as a list of
		dicts. Each dict contains two strings, the user mentioned and the
		number of times they were mentioned.

		If the user does not have enough mentions, the list returned may be
		shorter than expected, and if no mentions can be found then the list
		is a single dict with a message that there were not enough mentions
		along with an empty string.

		Keys of the dictionaries are:
		Mention
		TimesUsed
		"""
		if type(count) is not int:
			raise TypeError('Count should be an integer.')
		if count > 10:
			raise ValueError('Count cannot be greater than 10.')

		Ment_list = []
		with open(DFPath + 'WhatMentionsCondensed.csv', 'rU') as csvfile:
			reader = DictReader(csvfile, delimiter = ',')
			for row in reader:
				if (row['User'] == self.username) and (len(Ment_list) < count):
					Ment_list.append({'Mention':row['Mention'], 'TimesUsed':row['TimesUsed']})
				elif (row['User'] == self.username) and (len(Ment_list) == count):
					break
				elif (row['User'] != self.username) and (len(Ment_list) > 0):
					break
			else:
				if len(Ment_list) == 0:
					Ment_list = [{'Mention':self.username + ' did not have enough mentions.', 'TimesUsed':''}]
		return Ment_list

	# Finds RTs, HTs, and Ments in common between two users.
	def compare(self, other):
		"""
		other (User): other user to compare to

		Returns the number of retweets, hashtags, and mentions the two
		users have in common as a dictionary.

		Keys of the dictionary are:
		RTWeight
		HTWeight
		MentWeight
		"""
		if not isinstance(other, User):
			raise TypeError("'compare' must be called on another user.")

		if self.username == other.username:
			common_dict = {'RTWeight':'N/A', 'HTWeight':'N/A', 'MentWeight':'N/A'}
			return common_dict

		common_dict = {}
		with open(DFPath + 'ShortRTEdgeList.csv') as csvfile:
			reader = DictReader(csvfile, delimiter = ',')
			for row in reader:
				if (row['User1'] == self.username) and (row['User2'] == other.username):
					common_dict['RTWeight'] = row['Weight']
					break
				elif (row['User2'] == self.username) and (row['User1'] == other.username):
					common_dict['RTWeight'] = row['Weight']
					break
			else:
				common_dict['RTWeight'] = '0'

		with open(DFPath + 'HashtagEdgeList.csv') as csvfile:
			reader = DictReader(csvfile, delimiter = ',')
			for row in reader:
				if (row['User1'] == self.username) and (row['User2'] == other.username):
					common_dict['HTWeight'] = row['Weight']
					break
				elif (row['User2'] == self.username) and (row['User1'] == other.username):
					common_dict['HTWeight'] = row['Weight']
					break
			else:
				common_dict['HTWeight'] = '0'

		with open(DFPath + 'MentionsEdgeList.csv') as csvfile:
			reader = DictReader(csvfile, delimiter = ',')
			for row in reader:
				if (row['User1'] == self.username) and (row['User2'] == other.username):
					common_dict['MentWeight'] = row['Weight']
					break
				elif (row['User2'] == self.username) and (row['User1'] == other.username):
					common_dict['MentWeight'] = row['Weight']
					break
			else:
				common_dict['MentWeight'] = '0'

		return common_dict
