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

class User:
	def __init__(self, username):

		if type(username) is not str and type(username) is not unicode:
			raise TypeError('Username should be a string or unicode.')

		self.username = username

		with open(DFPath + 'User_info.csv') as csvfile:
			reader = DictReader(csvfile, delimiter = '\t')
			for row in reader:
				if row['Username'] == username:
					self.attributes = row
					break
			else:
				raise ValueError('This username is not in the database.')

	def get(self, attribute):
		if type(attribute) is not str and type(attribute) is not unicode:
			raise TypeError('Attribute should be a string or unicode.')

		attribute = attribute.capitalize()
		try:
			return self.attributes[attribute].replace('\\n', '\n').decode('utf-8')
		except KeyError:
			raise ValueError("Database does not contain the attribute: '" + attribute + "'.")

	def list_attributes(self):
		return self.attributes.keys()
