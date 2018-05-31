import scipy.stats as stats

num_dict = {}

for i in range(0, 10):
	num_dict[str(i)] = 0

f = open('TweetDF.csv')
f.readline()
for line in f:
	name = str.split(line, ',')[0]
	nums = name[-8:]
	for i in nums:
		num_dict[i] += 1
f.close()

for i in num_dict:
	print '{}: {}'.format(i, num_dict[i])

(chi_square, p) = stats.chisquare(num_dict.values())

print 'Chi-squared: {}'.format(chi_square)
print 'p-value: {}'.format(p)

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
