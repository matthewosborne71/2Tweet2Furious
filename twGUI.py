# Austin Antoniou in collaboration with Dan MacGregor and Matt Osborne
# for the Erdos Institute 2018 Summer Code Bootcamp
# construction of a GUI for twitter data
# Goals: select a user, display all user information
# when viewing a user, be able to select individual tweets and view their data

import Tkinter as tk

from User_class import User

#import MakeDozeNetworksFriendo as mdnf

def test_input(txt):
    window = tk.Tk()
    window.geometry('300x300')
    test = tk.Label(window, text = txt)
    test.pack()
    window.mainloop()

def menu():
    window = tk.Tk()
    window.title('Twitter Data Retrieval')
    window.geometry('300x300')
    #network_bttn = tk.Button(window, text = 'Create network', command = network_menu)
    search_bttn = tk.Button(window, text = 'Search by username', command = search_user)
    compare_bttn = tk.Button(window, text = 'Compare users', command = compare_search)
    #network_bttn.pack()
    search_bttn.pack()
    compare_bttn.pack()
    window.mainloop()

def network_menu():
    window = tk.Tk()
    window.title('Build a Network')
    #def RT_graph():
    #    (G,pos,weights) = BuildGraph('RT',int(d))
    #    DrawNetworkxGraph(G,pos,5,weights)
    #def HT_graph():
    #    (G,pos,weights) = BuildGraph('HT',int(d))
    #    DrawNetworkxGraph(G,pos,5,weights)
    #def Ment_Graph():
    #    (G,pos,weight) = BuildGraph('Ment',ind(d))
    #    DrawNetworkxGraph(G,pos,5,weights)
    type_lbl = tk.Label(window, text = 'Which type of network?')
    RT_bttn = tk.Button(window, text = 'Retweet')#, command = RT_graph)
    HT_bttn = tk.Button(window, text = 'Hashtag')#, command = HT_graph)
    Ment_bttn = tk.Button(window, text = 'Mention')#, command = Ment_graph)
    degree_lbl = tk.Label(window, text = 'Degree of connectivity required for an edge?')
    d = tk.StringVar()
    degree_enter = tk.Entry(window, textvariable = d)
    type_lbl.pack()
    RT_bttn.pack()
    HT_bttn.pack()
    Ment_bttn.pack()
    degree_lbl.pack()
    degree_enter.pack()
    window.mainloop()


def search_user():
    window = tk.Tk()
    window.title('User Search')
    window.geometry('600x300')
    def test():
        test_input(str(v.get()))
    def search():
        try:
            viewer(v.get())
        except ValueError as e:
            error_lbl = tk.Label(window, text = 'User not found')
            error_lbl.pack()
    search_lbl = tk.Label(window, text = 'Search users:')
    v = tk.StringVar()
    search_entry = tk.Entry(window, textvariable = v)
    #txt = v.get()
    search_bttn = tk.Button(window, text = 'search', command = test)
    search_lbl.pack()
    search_entry.pack()
    search_bttn.pack()
    window.mainloop()

def viewer(username):
    user = User(username)
    window = tk.Tk()
    window.title('User Data for '+username)
    window.geometry('600x300')
    user_lbl = tk.Label(window, text = username)
    #img_lbl = tk.Label(window, image = retrieve_image(user.get('image')))
    status_lbl = tk.Label(window, text = 'Status: '+user.get('status'))
    descr_lbl = tk.Label(window, text = 'Description: '+user.get('description'))
    followers_lbl = tk.Label(window, text = 'Followers: '+user.get('followers'))
    following_lbl = tk.Label(window, text = 'Following: '+user.get('friends'))
    tweets_lbl = tk.Label(window, text = 'Tweets: '+user.get('tweets'))
    user_lbl.pack()
    descr_lbl.pack()
    followers_lbl.pack()
    following_lbl.pack()
    tweets_lbl.pack()
    window.mainloop()

def compare_search():
    window = tk.Tk()
    window.title('User Comparison Search')
    window.geometry('600x300')
    def compare():
        try:
            comparison(v1.get(),v2.get())
        except ValueError as e:
            error_lbl = tk.Label(window, text = str(e))
            error_lbl.pack()
    search_lbl = tk.Label(window, text = 'Search users:')
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    search_entry1 = tk.Entry(window, textvariable = v1)
    search_entry2 = tk.Entry(window, textvariable = v2)
    #txt = v.get()
    search_bttn = tk.Button(window, text = 'search', command = compare)
    search_lbl.pack()
    search_entry1.pack()
    search_entry2.pack()
    search_bttn.pack()
    window.mainloop()

def comparison(username1,username2):
    user1 = User(username1)
    user2 = User(username2)
    window = tk.Tk()
    window.title('User Comparison')
    window.geometry('600x300')
    user1_lbl = tk.Label(window, text = username1)
    status1_lbl = tk.Label(window, text = 'Status: '+user1.get('status'))
    descr1_lbl = tk.Label(window, text = 'Description: '+user1.get('description'))
    followers1_lbl = tk.Label(window, text = 'Followers: '+user1.get('followers'))
    following1_lbl = tk.Label(window, text = 'Following: '+user1.get('friends'))
    tweets1_lbl = tk.Label(window, text = 'Tweets: '+user1.get('tweets'))
    #
    user2_lbl = tk.Label(window, text = username2)
    status2_lbl = tk.Label(window, text = 'Status: '+user2.get('status'))
    descr2_lbl = tk.Label(window, text = 'Description: '+user2.get('description'))
    followers2_lbl = tk.Label(window, text = 'Followers: '+user2.get('followers'))
    following2_lbl = tk.Label(window, text = 'Following: '+user2.get('friends'))
    tweets2_lbl = tk.Label(window, text = 'Tweets: '+user2.get('tweets'))
    #
    user1_lbl.pack(side = tk.LEFT)
    user2_lbl.pack(side = tk.RIGHT)
    status1_lbl.pack(side = tk.LEFT)
    status2_lbl.pack(side = tk.RIGHT)
    followers1_lbl.pack(side = tk.LEFT)
    following2_lbl.pack(side = tk.RIGHT)
    tweets1_lbl.pack(side = tk.LEFT)
    tweets2_lbl.pack(side = tk.RIGHT)
    window.mainloop()
