###############################################################################
##      NewNetworkWhoDis
##      Matthew Osborne
##      In Conjunction with: Austin Antoniou, Dan McGregor, Luke Andrejek
##      For the Erdos Institute May 2018 Code program
###############################################################################
##      Last Updated: June 3, 2018
###############################################################################
## NewNetworkWhoDis contains functions for analyzing your network!
###############################################################################

# Import the packages we need
import networkx as nx
import DataPath as DP
DFPath,TweetPath = DP.getPaths()
import pandas as pd

# This function reads in a networkx graph object and returns a list containing
# lists that contain the nodes of the connected components of the Graph
def GetComponents(G):
    Components = sorted(nx.connected_components(G),key = len,reverse=True)

    return Components

# This function reads in a connected component from a retweet network, and
# returns a dataframe of who they have retweeted and how many times that account
# has been retweeted
def WhoseThere(C):

    # read in the dataframe
    print "Reading in RTs DF"
    RTs = pd.read_csv(DFPath + "RTs.csv")

    # Find the accounts that have been retweeted
    print "Extracting retweeted accounts"
    RTUser = []
    for node in C:
        RTUser.extend(list(RTs['RTUser'].loc[RTs['User']==node]))

    # Find how many times they were retweeted
    print "Grabbing times retweeted"
    Who = pd.DataFrame(RTUser,columns = ['RTUser'])
    del RTUser
    HowMany = Who['RTUser'].value_counts()
    del Who

    return HowMany
