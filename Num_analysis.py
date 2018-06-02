################################################################################
##      Num_analysis                                                          ##
##      Dan McGregor                                                          ##
################################################################################
##      Last Updated: June 2, 2018                                            ##
################################################################################
## This file computes the frequency of numbers in the twitter usernames       ##
## and compares against a uniform distribution using a chi square test        ##
################################################################################


import scipy.stats as stats
import os

# Reads in the path for the data files
import DataPath
DFPath, TweetPath = DataPath.getPaths()

# Initializes the num_dict to store number frequency data
num_dict = {}
for i in range(0, 10):
	num_dict[str(i)] = 0

# Loops through every file and extracts the numbers from the usernames
for file_name in sorted(os.listdir(TweetPath)):
	nums = file_name[-19:-11]
	for i in nums:
		num_dict[i] += 1

# Runs a chi square test to compare the frequency of the numbers to a uniform
# distribution
(chi_square, p) = stats.chisquare(num_dict.values())

# Prints out the frequency of each number and the results of the chi square test
for i in sorted(num_dict):
	print '{}: {}'.format(i, num_dict[i])
print 'Chi-squared: {}'.format(chi_square)
print 'p-value: {}'.format(p)

# This is the output of the program
"""
0: 1941
1: 1993
2: 1758
3: 1721
4: 1755
5: 1769
6: 1772
7: 1735
8: 1779
9: 1753
Chi-squared: 42.1241655541
p-value: 3.11916324124e-06
"""
