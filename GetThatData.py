## GrabUserData is a python file that contains the functions that will
## allow you to grab data from our users and their tweets
############################################################
## Matthew Osborne
## Last Updated: May 30, 2018
###########################################################
## Note: DataPath is a python file containing the file paths to the
## data on my machine. In order to make the code work you will need to
## change those lines to your data paths
###########################################################


import pandas as pd

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
    f.write('User,HashTag,RT\n')
    f.close()

def    GrabHashtags():

    f = open('HashTagList.csv','a')
    for User in Users:
        import DataPath
        DFPath, TweetPath = DataPath.getPaths()

        # For each user go through all of their tweets and mine the
        # hashtags
        print 'a'

        print 'Fetching the Hashtags from' + User
        UserData = pd.read_csv(TweetPath + User + r'_tweets.csv' )
        for tweet in UserData['text']:
            print 'a'
