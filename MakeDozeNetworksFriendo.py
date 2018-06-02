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
        # For each user in the file check through all other users to see what
        # hashtags the users have in commonself.
        i = 0
        for name1 in UserList:
            print i
            EData = EdgeData[EdgeData['TimesUsed']>2]
            a  = set(EData['Hashtag'][EData['User']==name1])
            for name2 in UserList[i+1:]:
                b = set(EData['Hashtag'][EData['User']==name2])
                c = a.intersection(b)
                if c:
                    f.write(name1 + ',' + name2 + ',' + str(len(c)) + '\n')
            i = i + 1

        f.close()


    elif type == 'Ment':
        print 'We are building a mention edgelist!'
        i = 0
        for name1 in UserList:
            print i
            EData = EdgeData[EdgeData['TimesUsed']>3]
            a = set(EData['Mention'][EData['User']==name1])
            for name2 in UserList[i+1:]:
                b = set(EData['Mention'][EData['User']==name2])
                c = a.intersection(b)
                if c:
                    f.write(name1 + ',' + name2 + ',' + str(len(c)) + '\n')

            i=i+1
        f.close()

    else:
        print 'Sorry the type you have entered is not currently supported'

# This function will take in a type and minimal edge weight, Tol, and spit out a
# networkx graph object
def BuildGraph(Type,Tol):
    print 'You are making a graph of type: ' + Type
    print 'Tolerance Level is: ' + str(Tol)

    # Make a Retweet Network
    if Type == 'RT':
        print 'Getting Edges'
        EdgeList = pd.read_csv(DFPath + r"2Tweet2Furious\\ShortRTEdgeList.csv")

        # Find the maximum weight of all the Edges
        maxWeight = float(max(EdgeList['Weight']))

        # Scale the weights
        Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

        # Get the users
        User1 = list(EdgeList['User1'][EdgeList['Weight']>=Tol].values.flatten())
        User2 = list(EdgeList['User2'][EdgeList['Weight']>=Tol].values.flatten())

        # Clear the large edgelist from memory
        del EdgeList

        EdgeList = zip(User1,User2,Weights)

        # Make the Graph
        print 'Making Graph'
        G = nx.Graph()

        print 'Adding Nodes to Graph'
        nodes = list(set(User1).union(set(User2)))
        G.add_nodes_from(nodes)

        # Add the appropriate edges
        print 'Adding Edges to the Graph'
        G.add_weighted_edges_from(EdgeList)

        # Use networkx to set an appealing position
        pos = nx.spring_layout(G)
        edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

        return G, pos, edgewidth

    # Make a Hashtag Network
    elif Type == 'HT':
        print 'Getting Edges'
        EdgeList = pd.read_csv(DFPath + r"2Tweet2Furious\\HashtagEdgeList.csv")

        # Find the maximum weight of all the Edges
        maxWeight = float(max(EdgeList['Weight']))

        # Scale the weights
        Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

        # Get the users
        User1 = list(EdgeList['User1'][EdgeList['Weight']>=Tol].values.flatten())
        User2 = list(EdgeList['User2'][EdgeList['Weight']>=Tol].values.flatten())

        # Clear the large edgelist from memory
        del EdgeList

        EdgeList = zip(User1,User2,Weights)

        # Make the Graph
        print 'Making Graph'
        G = nx.Graph()

        print 'Adding Nodes to Graph'
        nodes = list(set(User1).union(set(User2)))
        G.add_nodes_from(nodes)

        # Add the appropriate edges
        print 'Adding Edges to the Graph'
        G.add_weighted_edges_from(EdgeList)

        # Use networkx to set an appealing position
        pos = nx.spring_layout(G)
        edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

        return G, pos, edgewidth

    # Make a mention network
    elif Type == 'Ment':
        print 'Getting Edges'
        EdgeList = pd.read_csv(DFPath + r"2Tweet2Furious\\HashtagEdgeList.csv")

        # Find the maximum weight of all the Edges
        maxWeight = float(max(EdgeList['Weight']))

        # Scale the weights
        Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

        # Get the users
        User1 = list(EdgeList['User1'][EdgeList['Weight']>=Tol].values.flatten())
        User2 = list(EdgeList['User2'][EdgeList['Weight']>=Tol].values.flatten())

        # Clear the large edgelist from memory
        del EdgeList

        EdgeList = zip(User1,User2,Weights)

        # Make the Graph
        print 'Making Graph'
        G = nx.Graph()

        print 'Adding Nodes to Graph'
        nodes = list(set(User1).union(set(User2)))
        G.add_nodes_from(nodes)

        # Add the appropriate edges
        print 'Adding Edges to the Graph'
        G.add_weighted_edges_from(EdgeList)

        # Use networkx to set an appealing position
        pos = nx.spring_layout(G)
        edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

        return G, pos, edgewidth

    else:
        print "Sorry we don't support that type of network!"

def DrawNetworkxGraph(G,pos,Weights,Size=5):
    plt.figure(figsize = (20,20))
    plt.axis('off')
    nx.draw_networkx_nodes(G,pos,node_size=Size)
    nx.draw_networkx_edges(G,pos,width=Weights)
    plt.show()

def MakeHVGraph(G):
    # Set plot options
    print "Setting plot options"
    options = {'Graph': dict(node_size = 5, edge_line_width = .2,height=1000,width=1000,xaxis=None,yaxis=None)}
    padding = dict(x=(-1.2, 1.2), y=(-1.2, 1.2))
    # Make a holoviews graph
    print "Making the Interactive graph"
    Graph = hv.Graph.from_networkx(G,nx.spring_layout).redim.range(**padding)
    del G

    # This makes the html graph
    renderer = hv.renderer('bokeh')
    renderer.save(Graph,'hvplot.html')
    plot = renderer.get_plot(Graph.options(options)).state
    from bokeh.io import output_file, save, show
    save(plot, 'hvplot.html')
    show(plot)
