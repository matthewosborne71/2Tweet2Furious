# Austin Antoniou in collaboration with Dan MacGregor and Matt Osborne
# for the Erdos Institute 2018 Summer Code Bootcamp
# construction of a GUI for twitter data
# Goals: select a user, display all user information
# when viewing a user, be able to select individual tweets and view their data

import Tkinter as tk

from User_class import User

#import MakeDozeNetworksFriendo as mdnf


menu = tk.Tk()


# def network_menu():
#     window = tk.Tk()
#     window.title('Build a Network')
#     #def RT_graph():
#     #    (G,pos,weights) = BuildGraph('RT',int(d))
#     #    DrawNetworkxGraph(G,pos,5,weights)
#     #def HT_graph():
#     #    (G,pos,weights) = BuildGraph('HT',int(d))
#     #    DrawNetworkxGraph(G,pos,5,weights)
#     #def Ment_Graph():
#     #    (G,pos,weight) = BuildGraph('Ment',ind(d))
#     #    DrawNetworkxGraph(G,pos,5,weights)
#     type_lbl = tk.Label(window, text = 'Which type of network?')
#     RT_bttn = tk.Button(window, text = 'Retweet')#, command = RT_graph)
#     HT_bttn = tk.Button(window, text = 'Hashtag')#, command = HT_graph)
#     Ment_bttn = tk.Button(window, text = 'Mention')#, command = Ment_graph)
#     degree_lbl = tk.Label(window, text = 'Degree of connectivity required for an edge?')
#     d = tk.StringVar()
#     degree_enter = tk.Entry(window, textvariable = d)
#     type_lbl.pack()
#     RT_bttn.pack()
#     HT_bttn.pack()
#     Ment_bttn.pack()
#     degree_lbl.pack()
#     degree_enter.pack()
#     window.mainloop()


def search_user():
    searcher = tk.Toplevel(menu)
    searcher.title('User Search')
    searcher.geometry('600x300')
    def search():
        try:
            viewer(v.get())
        except ValueError as e:
            error_lbl = tk.Label(searcher, text = str(e))
            error_lbl.pack()
    search_lbl = tk.Label(searcher, text = 'Search users:')
    v = tk.StringVar()
    search_entry = tk.Entry(searcher, textvariable = v)
    search_bttn = tk.Button(searcher, text = 'search', command = search)
    search_lbl.pack()
    search_entry.pack()
    search_bttn.pack()
    searcher.mainloop()

def viewer(username):
    user = User(username)
    try:
        desc = str(user.get('description'))
    except UnicodeEncodeError as e:
        desc = 'Error - contains unicode'
    if desc == '':
        desc = 'None provided'
    view = tk.Toplevel(menu)
    view.title('User Data for '+username)
    view.geometry('600x300')
    user_lbl = tk.Label(view, text = username)
    #img_lbl = tk.Label(view, image = retrieve_image(user.get('image')))
    status_lbl = tk.Label(view, text = 'Status: '+user.get('status'))
    descr_lbl = tk.Message(view, text = 'Description: '+desc, width = 200)
    followers_lbl = tk.Label(view, text = 'Followers: '+user.get('followers'))
    following_lbl = tk.Label(view, text = 'Following: '+user.get('friends'))
    tweets_lbl = tk.Label(view, text = 'Tweets: '+user.get('tweets'))
    user_lbl.pack()
    descr_lbl.pack()
    followers_lbl.pack()
    following_lbl.pack()
    tweets_lbl.pack()
    view.mainloop()

def compare_search():
    csearcher = tk.Toplevel(menu)
    csearcher.title('User Comparison Search')
    csearcher.geometry('600x300')
    def compare():
        try:
            comparison(v1.get(),v2.get())
        except ValueError as e:
            error_lbl = tk.Label(csearcher, text = str(e))
            error_lbl.pack()
    search_lbl = tk.Label(csearcher, text = 'Search users:')
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    search_entry1 = tk.Entry(csearcher, textvariable = v1)
    search_entry2 = tk.Entry(csearcher, textvariable = v2)
    #txt = v.get()
    search_bttn = tk.Button(csearcher, text = 'search', command = compare)
    search_lbl.pack()
    search_entry1.pack()
    search_entry2.pack()
    search_bttn.pack()
    csearcher.mainloop()

def comparison(username1,username2):
    user1 = User(username1)
    user2 = User(username2)
    comp = user1.compare(user2)
    try:
        desc1 = str(user1.get('description'))
    except UnicodeEncodeError as e:
        desc1 = 'Error - contains unicode'
    try:
        desc2 = str(user2.get('description'))
    except UnicodeEncodeError as e:
        desc2 = 'Error - contains unicode'
    cview = tk.Toplevel(menu)
    cview.title('User Comparison')
    cview.geometry('600x300')
    f1 = tk.Frame(cview)
    f2 = tk.Frame(cview)
    f3 = tk.Frame(cview)
    user1_lbl = tk.Label(f1, text = username1)
    status1_lbl = tk.Label(f1, text = 'Status: '+user1.get('status'))
    desc1_lbl = tk.Message(f1, text = 'Description: '+desc1, width = 200)
    followers1_lbl = tk.Label(f1, text = 'Followers: '+user1.get('followers'))
    following1_lbl = tk.Label(f1, text = 'Following: '+user1.get('friends'))
    tweets1_lbl = tk.Label(f1, text = 'Tweets: '+user1.get('tweets'))
    #
    user2_lbl = tk.Label(f2, text = username2)
    status2_lbl = tk.Label(f2, text = 'Status: '+user2.get('status'))
    desc2_lbl = tk.Message(f2, text = 'Description: '+desc2, width = 200)
    followers2_lbl = tk.Label(f2, text = 'Followers: '+user2.get('followers'))
    following2_lbl = tk.Label(f2, text = 'Following: '+user2.get('friends'))
    tweets2_lbl = tk.Label(f2, text = 'Tweets: '+user2.get('tweets'))
    #
    #comp = user1.compare(user2)
    RT_lbl = tk.Label(f3, text = 'Retweeted users in common: '+comp['RTWeight'])
    Ment_lbl = tk.Label(f3, text = 'Mentioned users in common:+ '+comp['MentWeight'])
    HT_lbl = tk.Label(f3, text = 'Hashtags in common: '+comp['HTWeight'])
    user1_lbl.pack()
    user2_lbl.pack()
    desc1_lbl.pack()
    desc2_lbl.pack()
    status1_lbl.pack()
    status2_lbl.pack()
    followers1_lbl.pack()
    following2_lbl.pack()
    following1_lbl.pack()
    following2_lbl.pack()
    tweets1_lbl.pack()
    tweets2_lbl.pack()
    RT_lbl.pack()
    Ment_lbl.pack()
    HT_lbl.pack()
    f1.pack(side = tk.LEFT)
    f2.pack(side = tk.RIGHT)
    f2.pack(side = tk.BOTTOM)
    cview.mainloop()


menu.title('Twitter Data Retrieval')
menu.geometry('300x300')
#network_bttn = tk.Button(window, text = 'Create network', command = network_menu)
search_bttn = tk.Button(menu, text = 'Search by username', command = search_user)
compare_bttn = tk.Button(menu, text = 'Compare users', command = compare_search)
#network_bttn.pack()
search_bttn.pack()
compare_bttn.pack()
menu.mainloop()
