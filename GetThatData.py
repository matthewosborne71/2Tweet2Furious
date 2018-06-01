## GrabUserData is a python file that contains the functions that will
## allow you to grab data from our users and their tweets
############################################################
## Matthew Osborne
## Austin Antoniou, Dan McGregor, Luke Andrejek
##
## Last Updated: May 31, 2018
###########################################################
## Note: DataPath is a python file containing the file paths to the
## data on my machine. In order to make the code work you will need to
## change those lines to your data paths
###########################################################


import pandas as pd
import tweetextract as te

# A function that will grab all of the usernames of the 2247 accounts
def GrabAccounts():
    import DataPath
    DFPath, TweetPath = DataPath.getPaths()

    print "Grabbing The Accounts"
    TweetDF = pd.read_csv(DFPath + 'TweetDF.csv')
    SET = set(TweetDF['User'].unique())

    return SET

# This function will write all of the RTs from every users tweets into a csv
# file
def GrabRTs():
    import DataPath
    DFPath, TweetPath = DataPath.getPaths()
    # create the csv file
    f = open(DFPath + 'RTList.csv','w+')
    f.write('User,RTtext\n')
    f.close()

    f = open(DFPath + 'RTList.csv','a+')


    Users = GrabAccounts()
    for name in Users:

        print "Reading in " + name + "\'s file."
        File = pd.read_csv(TweetPath + name + r'_tweets.csv')

        print "Extracting the retweets of " + name
        for tweet in File['text']:
            if tweet[:4] == 'RT @':
                f.write(name + ',' + tweet.replace(',', '') + '\n')
    f.close()



# This function will write the Hashtags from the every users tweet
# into a csv file
def WriteHashtags():
    f = open('HashTagList.csv','w+')
    f.write('User,HashTag,isRT\n')
    f.close()

# This function grabs each hashtag and stores it in the csv created by
# WriteHashtags()
def GrabHashtags():
    import DataPath
    DFPath, TweetPath = DataPath.getPaths()
    # create the csv file
    f = open('HashTagList.csv','a')

    Users = GrabAccounts()
    i = 0
    for User in Users:
        print i
        import DataPath
        DFPath, TweetPath = DataPath.getPaths()

        # For each user go through all of their tweets and mine the
        # hashtags

        print 'Fetching the Hashtags from ' + User
        UserData = pd.read_csv(TweetPath + User + r'_tweets.csv' )
        for tweet in UserData['text']:
            isRT = te.isRT(tweet)
            hashtags = te.hashtags(tweet)

            for hashtag in hashtags:
                if hashtag != '':
                    f.write(User + ',' + hashtag + ',' + isRT + '\n')

        i = i+1

# Create a csv that keeps track of how many times each person uses a hashtag
# condensed must be True or False
def WhatHashtags(condensed):
    import DataPath
    DFPath, TweetPath = DataPath.getPaths()

    # Open the csv where data will be written
    if condensed == False:
        f = open('WhatHashtags.csv','w+')
        f.write('User,isRT,Hashtag,TimesUsed\n')
        f.close()

        # Get the Users
        HashtagList = pd.read_csv(DFPath + r'2Tweet2Furious\\HashtagList.csv')
        Users = list(HashtagList['User'].value_counts().index)

        # For each User we will find the unique hashtags they have used along with
        # the number of times they used that hashtag
        f = open('WhatHashtags.csv','a')
        j = 0
        for User in Users:
            print j
            UserFile = HashtagList[HashtagList['User'] == User]
            UserFileRT = UserFile[UserFile['isRT'] == 'Y']['HashTag'].value_counts()
            UserFileNRT = UserFile[UserFile['isRT'] == 'N']['HashTag'].value_counts()

            for i in range(len(UserFileRT)):
                f.write(User + ',' + 'Y' + ',' + str(UserFileRT.index[i]) + ',' + str(UserFileRT[i]) + '\n')
            for i in range(len(UserFileNRT)):
                f.write(User + ',' + 'N' + ',' + str(UserFileNRT.index[i]) + ',' + str(UserFileNRT[i]) + '\n')
            j = j +1

        f.close()
    elif condensed == True:
        f = open('WhatHashtagsCondensed.csv','w+')
        f.write('User,Hashtag,TimesUsed\n')
        f.close()

        # Get the Users
        HashtagList = pd.read_csv(DFPath + r'2Tweet2Furious\\HashtagList.csv')
        Users = list(HashtagList['User'].value_counts().index)

        # For each User we will find the unique hashtags they have used along with
        # the number of times they used that hashtag
        f = open('WhatHashtagsCondensed.csv','a')
        j = 0
        for User in Users:
            print j
            UserFile = HashtagList[HashtagList['User'] == User]
            UserHashtags = UserFile['HashTag'].value_counts()

            for i in range(len(UserHashtags)):
                f.write(User + ',' + str(UserHashtags.index[i]) + ',' + str(UserHashtags[i]) + '\n')

            j = j +1

        f.close()


# Create a Mention csv
def WriteMentions():
    f = open('MentionList.csv','w+')
    f.write('User,Mention,isRT\n')
    f.close()

# Write Mentions to the csv created by WriteMentions()
def GrabMentions():
    import DataPath
    DFPath, TweetPath = DataPath.getPaths()
    # create the csv file
    f = open('MentionList.csv','a')

    Users = GrabAccounts()
    i = 0
    for User in Users:
        print i
        import DataPath
        DFPath, TweetPath = DataPath.getPaths()

        # For each user go through all of their tweets and mine the
        # hashtags

        print 'Fetching the Mentions from ' + User
        UserData = pd.read_csv(TweetPath + User + r'_tweets.csv' )
        for tweet in UserData['text']:
            isRT = te.isRT(tweet)
            mentions = te.mentions(tweet)

            for mention in mentions:
                if mention != '':
                    f.write(User + ',' + mention + ',' + isRT + '\n')

        i = i+1

# Create a csv that keeps track of how many times each person uses a hashtag
# condensed must be either True or False
def WhatMentions(condensed):
    import DataPath
    DFPath, TweetPath = DataPath.getPaths()

    if condensed == False:
        # Open the csv where data will be written
        f = open('WhatMentions.csv','w+')
        f.write('User,isRT,Mention,TimesUsed\n')
        f.close()

        # Get the Users
        MentionList = pd.read_csv(DFPath + r'2Tweet2Furious\\MentionList.csv')
        Users = list(MentionList['User'].value_counts().index)

        # For each User we will find the unique hashtags they have used along with
        # the number of times they used that hashtag
        f = open('WhatMentions.csv','a')
        j = 0
        for User in Users:
            print j
            UserFile = MentionList[MentionList['User'] == User]
            UserFileRT = UserFile[UserFile['isRT'] == 'Y']['Mention'].value_counts()
            UserFileNRT = UserFile[UserFile['isRT'] == 'N']['Mention'].value_counts()

            for i in range(len(UserFileRT)):
                f.write(User + ',' + 'Y' + ',' + str(UserFileRT.index[i]) + ',' + str(UserFileRT[i]) + '\n')
            for i in range(len(UserFileNRT)):
                f.write(User + ',' + 'N' + ',' + str(UserFileNRT.index[i]) + ',' + str(UserFileNRT[i]) + '\n')
            j = j +1

        f.close()
    elif condensed == True:
        f = open('WhatMentionsCondensed.csv','w+')
        f.write('User,Mention,TimesUsed\n')
        f.close()

        # Get the Users
        MentionList = pd.read_csv(DFPath + r'2Tweet2Furious\\MentionList.csv')
        Users = list(MentionList['User'].value_counts().index)

        # For each User we will find the unique hashtags they have used along with
        # the number of times they used that hashtag
        f = open('WhatMentionsCondensed.csv','a')
        j = 0
        for User in Users:
            print j
            UserFile = MentionList[MentionList['User'] == User]
            UserMentions = UserFile['Mention'].value_counts()

            for i in range(len(UserMentions)):
                f.write(User + ',' + str(UserMentions.index[i]) + ',' + str(UserMentions[i]) + '\n')
            j = j +1

        f.close()
