###############################################################################
##      MakeDozeNetworksFriendo
##      Matthew Osborne
##      In Conjunction with: Austin Antoniou, Dan McGregor, Luke Andrejek
##      For the Erdos Institute May 2018 Code program
###############################################################################
##      Last Updated: June 3, 2018
###############################################################################
## This file contains all the functions we will use to make the various networks
###############################################################################

# We Need to import these packages for various functions
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import holoviews as hv
import DataPath as DP

# Get the DataPaths
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

def GetMax(Type):
    if Type == 'RT':
        EdgeList = pd.read_csv(DFPath + r"2Tweet2Furious\\ShortRTEdgeList.csv")

        # Find the maximum weight of all the Edges
        maxWeight = float(max(EdgeList['Weight']))
        return maxWeight
    elif Type == 'HT':
        EdgeList = pd.read_csv(DFPath + r"2Tweet2Furious\\HashtagEdgeList.csv")

        # Find the maximum weight of all the Edges
        maxWeight = float(max(EdgeList['Weight']))
        return maxWeight
    elif Type == 'Ment':
        EdgeList = pd.read_csv(DFPath + r"2Tweet2Furious\\HashtagEdgeList.csv")

        # Find the maximum weight of all the Edges
        maxWeight = float(max(EdgeList['Weight']))
        return maxWeight
    else:
        return maxWeight
        print "No dice!"



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

# This function takes in a networkx graph object, the desired position of the
# nodes of the graph, the desired weights of the edges and the desired node Size
# note that default node size is 5
def DrawNetworkxGraph(G,pos,Weights,Size=5):

    # open the matplotlib.plot figure and set it to be 20 by 20
    plt.figure(figsize = (20,20))

    # turn of the axis labels
    plt.axis('off')

    # Draw the graph nodes
    nx.draw_networkx_nodes(G,pos,node_size=Size)

    # Draw the graph edges
    nx.draw_networkx_edges(G,pos,width=Weights)

    # This opens the plot on your machine
    plt.show()

# This function will draw a networkx graph and save it, in addition to the
# inputs required of DrawNetworkxGraph you need to enter the type and Tolerance
# Type must be "RT", "HT", or "Ment"
def SaveNetworkxGraph(G,pos,Weights,Folder,Type,Tol,Size=5):

    # set up the plot
    plt.figure(figsize = (20,20))
    plt.axis('off')

    # Draw the nodes
    nx.draw_networkx_nodes(G,pos,node_size=Size)

    # Draw the edges
    nx.draw_networkx_edges(G,pos,width=Weights)

    # This part of the code will set the x and y axes so that the entire Graph
    # is shown in the plot and is as large as possible
    xpositions = []
    ypositions = []
    for node in G.nodes():
        xpositions.extend([list(pos[node])[0]])
        ypositions.extend([list(pos[node])[1]])
    xmin = min(xpositions)
    xmax = max(xpositions)
    ymin = min(ypositions)
    ymax = max(ypositions)
    plt.ylim((ymin-.01,ymax+.01))
    plt.xlim((xmin-.01,xmax+.01))

    # Save the figure, you may need to change the filename based on your machine
    plt.savefig(fname = DFPath + Folder + r'\\' + Type + 'MinWeight' + str(Tol) + '.png',bbox_inches='tight')

    # Close the plot
    plt.close()

# This function takes in a networkx graph object and opens an html file with
# an interactive holoviews graph consisting of the nodes and edges from the
# networkx graph
def MakeHVGraph(G):
    # Set plot options
    print "Setting plot options"
    options = {'Graph': dict(node_size = 5, edge_line_width = .2,height=1000,width=1000,xaxis=None,yaxis=None,inspection_policy='nodes')}
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

    # Open the plot
    show(plot)




def SaveAllGraphs(Type):
    Stop = False
    max = GetMax(Type)

    if Type == 'RT':
        Folder = r'RTImages'
    elif Type == 'HT':
        Folder = r'HTImages'
    elif Type == 'Ment':
        Folder = r'MentImages'
    else:
        print 'Nope!'
        Stop = True

    if Stop == False:
        print "Building First Graph"
        G,pos0,Weights = BuildGraph(Type,1)
        SaveNetworkxGraph(G,pos0,Weights,Folder,Type,1)
        del G
        del Weights

        print "Building other Graphs"
        for i in range(2,int(max)):
            G,pos,Weights = BuildGraph(Type,i)
            del pos
            SaveNetworkxGraph(G,pos0,Weights,Folder,Type,i)
            del G
            del Weights
            print i
