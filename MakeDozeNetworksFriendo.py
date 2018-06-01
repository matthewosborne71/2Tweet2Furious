###############################################################################
##      MakeDozeNetworksFriendo
##      Matthew Osborne
###############################################################################
##      Last Updated: May 31, 2018
###############################################################################
## This file contains all the functions we will use to make the various networks
###############################################################################

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import holoviews as hv
import DataPath as DP

DFPath,TweetPath = DP.getPaths()

# This function will take in the name data you want to make the edgelist from,
# and what you want to name the csv that stores the edgelist as well as the
# Network type
#
# Note! Data must be a csv file, and name must end in .csv
# type must be one of:RT, HT, Ment
def MakeEdgeList(Data,EdgeListName,type):

    # Reading in this file gives you the user data needed to write the edgelist
    EdgeData = pd.read_csv(DFPath + Data)

    # Create the csv file where the edgelist is stored
    f = open(EdgeListName,'w+')
    f.write("User1,User2,Weight\n")
    f.close()

    # Re-Open the file so we can append to it
    f = open(EdgeListName,'a+')

    # Make a list of users for searching purposes
    UserList = list(set(EdgeData['User']))


    # Check the type to decide what kind of network we're building
    if type == 'RT':
        print 'We are building a retweet edgelist!'

        # For each user in the file check through all other users to see what
        # accounts they are retweeting in common. Meaning if userA retweets
        # Donald Trump and userB retweets Donald Trump this will be found

        i = 0
        for name1 in UserList:
            print i
            a = set(EdgeData['RTUser'][EdgeData['User']==name1])
            for name2 in UserList[i+1:]:
                b = set(EdgeData['RTUser'][EdgeData['User']==name2])
                c = a.intersection(b)
                if c:
                    f.write(name1 + "," + name2 + "," + str(len(c)) + "\n")

            i = i+1

        f.close()
    elif type == 'HT':
        print 'We are building a hashtag edgelist!'

    elif type == 'Ment':
        print 'We are building a mention edgelist!'

    else:
        print 'Sorry the type you have entered is not currently supported'
