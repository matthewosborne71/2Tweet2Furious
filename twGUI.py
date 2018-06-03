# Austin Antoniou in collaboration with Dan MacGregor and Matt Osborne
# for the Erdos Institute 2018 Summer Code Bootcamp
# construction of a GUI for twitter data
# Goals: select a user, display all user information
# when viewing a user, be able to select individual tweets and view their data

import Tkinter as tk

from io import BytesIO
import urllib
from PIL import Image, ImageTk

from User_class import User

#import MakeDozeNetworksFriendo as mdnf

menu = tk.Tk()
myfont = ('Helvetica','24')


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
    #searcher.geometry('400x300')
    def search():
        try:
            viewer(v.get())
        except ValueError as e:
            error_lbl = tk.Label(searcher, text = str(e),font=myfont)
            error_lbl.grid(row=3, column=0)
    search_lbl = tk.Label(searcher, text = 'Search users:', font=myfont)
    v = tk.StringVar()
    search_entry = tk.Entry(searcher, textvariable = v, font=myfont)
    search_bttn = tk.Button(searcher, text = 'search', command = search, font=myfont)
    search_lbl.grid(row=0, column=0)
    search_entry.grid(row=1, column=0)
    search_bttn.grid(row=2, column=0)
    searcher.mainloop()

def viewer(username):
    user = User(username)
    url = user.get('image')
    if url == 'N/A':
        url = 'https://pbs.twimg.com/profile_images/479315519729070081/ty2LLr9m.jpeg'
    u = urllib.urlopen(url)
    raw_data = u.read()
    u.close()
    try:
        desc = str(user.get('description'))
    except UnicodeEncodeError as e:
        desc = 'Error - contains unicode'
    if desc == '':
        desc = 'None provided'
    view = tk.Toplevel(menu)
    view.title('User Data for '+username)
    #view.geometry('600x300')
    user_lbl = tk.Label(view, text = username, font=myfont)
    img = Image.open(BytesIO(raw_data))
    img = img.resize((100,100))
    img = ImageTk.PhotoImage(img)
    img_lbl = tk.Label(view, image = img)
    status_lbl = tk.Label(view, text = 'Status: '+user.get('status'), font=myfont)
    descr_lbl = tk.Message(view, text = 'Description: '+desc, width = 200, font=myfont)
    followers_lbl = tk.Label(view, text = 'Followers: '+user.get('followers'), font=myfont)
    following_lbl = tk.Label(view, text = 'Following: '+user.get('friends'), font=myfont)
    tweets_lbl = tk.Label(view, text = 'Tweets: '+user.get('tweets'), font=myfont)
    user_lbl.grid(row=0)
    img_lbl.grid(row=1)
    status_lbl.grid(row=2)
    descr_lbl.grid(row=3)
    followers_lbl.grid(row=4)
    following_lbl.grid(row=5)
    tweets_lbl.grid(row=6)
    view.mainloop()

def compare_search():
    csearcher = tk.Toplevel(menu)
    csearcher.title('User Comparison Search')
    #csearcher.geometry('600x300')
    def compare():
        try:
            comparison(v1.get(),v2.get())
        except ValueError as e:
            error_lbl = tk.Label(csearcher, text = str(e), font=myfont)
            error_lbl.pack()
    search_lbl = tk.Label(csearcher, text = 'Search users:', font=myfont)
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    search_entry1 = tk.Entry(csearcher, textvariable = v1, font=myfont)
    search_entry2 = tk.Entry(csearcher, textvariable = v2, font=myfont)
    #txt = v.get()
    search_bttn = tk.Button(csearcher, text = 'search', command = compare, font=myfont)
    search_lbl.grid(row=0)
    search_entry1.grid(row=1)
    search_entry2.grid(row=2)
    search_bttn.grid(row=3)
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
    url1 = user1.get('image')
    if url1 == 'N/A':
        url1 = 'https://pbs.twimg.com/profile_images/479315519729070081/ty2LLr9m.jpeg'
    url2 = user2.get('image')
    if url2 == 'N/A':
        url2 = 'https://pbs.twimg.com/profile_images/479315519729070081/ty2LLr9m.jpeg'
    u1 = urllib.urlopen(url1)
    u2 = urllib.urlopen(url2)
    raw_data1 = u1.read()
    raw_data2 = u2.read()
    u1.close()
    u2.close()
    img1 = Image.open(BytesIO(raw_data1))
    img2 = Image.open(BytesIO(raw_data2))
    img1 = img1.resize((100,100))
    img2 = img2.resize((100,100))
    img1 = ImageTk.PhotoImage(img1)
    img2 = ImageTk.PhotoImage(img2)
    cview = tk.Toplevel(menu)
    cview.title('User Comparison')
    #cview.geometry('800x300')
    f1 = tk.Frame(cview)
    f2 = tk.Frame(cview)
    f3 = tk.Frame(cview)
    header = tk.Message(f1, text = 'Comparison of:\n'+username1+'\n'+username2, font=myfont, width=400)
    user1_lbl = tk.Label(f1, text = username1, font=myfont)
    img1_lbl = tk.Label(f1, image = img1)
    status1_lbl = tk.Label(f1, text = 'Status: '+user1.get('status'), font=myfont)
    desc1_lbl = tk.Message(f1, text = 'Description: '+desc1, width = 200, font=myfont)
    followers1_lbl = tk.Label(f1, text = 'Followers: '+user1.get('followers'), font=myfont)
    following1_lbl = tk.Label(f1, text = 'Following: '+user1.get('friends'), font=myfont)
    tweets1_lbl = tk.Label(f1, text = 'Tweets: '+user1.get('tweets'), font=myfont)
    #
    user2_lbl = tk.Label(f1, text = username2, font=myfont)
    img2_lbl = tk.Label(f1, image = img2)
    status2_lbl = tk.Label(f1, text = 'Status: '+user2.get('status'), font=myfont)
    desc2_lbl = tk.Message(f1, text = 'Description: '+desc2, width = 200, font=myfont)
    followers2_lbl = tk.Label(f1, text = 'Followers: '+user2.get('followers'), font=myfont)
    following2_lbl = tk.Label(f1, text = 'Following: '+user2.get('friends'), font=myfont)
    tweets2_lbl = tk.Label(f1, text = 'Tweets: '+user2.get('tweets'), font=myfont)
    #
    #comp = user1.compare(user2)
    RT_lbl = tk.Label(f3, text = 'Retweeted users in common: '+comp['RTWeight'], font=myfont)
    Ment_lbl = tk.Label(f3, text = 'Mentioned users in common: '+comp['MentWeight'], font=myfont)
    HT_lbl = tk.Label(f3, text = 'Hashtags in common: '+comp['HTWeight'], font=myfont)
    header.grid(row=0, column=1)
    user1_lbl.grid(row=1, column=0)
    user2_lbl.grid(row=1, column=2)
    img1_lbl.grid(row=2, column=0)
    img2_lbl.grid(row=2, column=2)
    desc1_lbl.grid(row=3, column=0)
    desc2_lbl.grid(row=3, column=2)
    status1_lbl.grid(row=4, column=0)
    status2_lbl.grid(row=4, column=2)
    followers1_lbl.grid(row=5, column=0)
    followers2_lbl.grid(row=5, column=2)
    following1_lbl.grid(row=6, column=0)
    following2_lbl.grid(row=6, column=2)
    tweets1_lbl.grid(row=7, column=0)
    tweets2_lbl.grid(row=7, column=2)
    RT_lbl.grid(row=0)
    Ment_lbl.grid(row=1)
    HT_lbl.grid(row=2)
    f1.grid(row=0, column=0)
    f3.grid(row=1, column=0)
    cview.grid_columnconfigure(0,pad='50')
    cview.mainloop()


menu.title('Twitter Data Retrieval')
#menu.geometry('300x200')
#network_bttn = tk.Button(window, text = 'Create network', command = network_menu)
search_bttn = tk.Button(menu, text = 'Search by username', command = search_user, font=myfont)
compare_bttn = tk.Button(menu, text = 'Compare users', command = compare_search, font=myfont)
#network_bttn.pack()
search_bttn.grid(row=0)
compare_bttn.grid(row=1)
menu.grid_columnconfigure(0,pad='50')
menu.mainloop()
