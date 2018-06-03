# Austin Antoniou in collaboration with Dan McGregor and Matt Osborne
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

url_def = 'https://pbs.twimg.com/profile_images/479315519729070081/ty2LLr9m.jpeg'
url_ban = 'https://pbs.twimg.com/media/CKZ8n7xUcAAEeUR.png'
#url_del = 'http://www.clker.com/cliparts/1/d/0/3/11954298581253392365Andy_-_Trash_Can.svg.hi.png'
url_del = 'https://st.depositphotos.com/1742172/2155/v/950/depositphotos_21551301-stock-illustration-cartoon-dancing-trash-can.jpg'


menu = tk.Tk()
#myfont = ('Helvetica','24')
myfont = ('GothamNarrowSSm','24')

def search_user():
    searcher = tk.Toplevel(menu)
    searcher.title('User Search')
    searcher.config(bg = '#00aced')
    #searcher.geometry('408x200')
    error_lbl = tk.Label(searcher, text = 60*' ',font=myfont,bg = '#00aced')
    error_lbl.grid(row=3, column=0)
    def search():
        error_lbl.config(text = '')
        try:
            viewer(v.get())
        except ValueError as e:
            error_lbl.config(text = e)
            #error_lbl.grid(row=3, column=0)
    search_lbl = tk.Label(searcher, text = 'Search users:', font=myfont, bg = '#00aced')
    v = tk.StringVar()
    search_entry = tk.Entry(searcher, textvariable = v, font=myfont, highlightthickness = 0)
    search_bttn = tk.Button(searcher, text = ' search ', command = search, font=myfont, bg = '#00aced', highlightthickness = 0)
    search_lbl.grid(row=0, column=0)
    search_entry.grid(row=1, column=0)
    search_bttn.grid(row=2, column=0)
    search_bttn.grid_columnconfigure(0, pad=50)
    searcher.mainloop()

def viewer(username):
    user = User(username)
    url = user.get('image')
    if url == 'N/A':
        if user.get('status') == 'Banned':
            url = url_ban
        elif user.get('status') == 'Deleted':
            url = url_del
        else:
            url = url_def
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
    view.configure(bg = '#00aced')
    #view.geometry('600x300')
    user_lbl = tk.Label(view, text = username, font=myfont, bg='#00aced')
    img = Image.open(BytesIO(raw_data))
    img = img.resize((100,100))
    img = ImageTk.PhotoImage(img)
    img_lbl = tk.Label(view, image = img)
    status_lbl = tk.Label(view, text = 'Status: '+user.get('status'), font=myfont, bg='#00aced')
    descr_lbl = tk.Message(view, text = 'Description: '+desc, width = 200, font=myfont, bg='#00aced')
    followers_lbl = tk.Label(view, text = 'Followers: '+user.get('followers'), font=myfont, bg='#00aced')
    following_lbl = tk.Label(view, text = 'Following: '+user.get('friends'), font=myfont, bg='#00aced')
    tweets_lbl = tk.Label(view, text = 'Tweets: '+user.get('tweets'), font=myfont, bg='#00aced')
    user_lbl.grid(row=0)
    img_lbl.grid(row=1)
    status_lbl.grid(row=2)
    descr_lbl.grid(row=3)
    followers_lbl.grid(row=4)
    following_lbl.grid(row=5)
    tweets_lbl.grid(row=6)
    view.grid_columnconfigure(0, pad=50)
    view.mainloop()

def compare_search():
    csearcher = tk.Toplevel(menu)
    csearcher.configure(bg = '#00aced')
    csearcher.title('User Comparison Search')
    def compare():
        try:
            comparison(v1.get(),v2.get())
        except ValueError as e:
            error_lbl = tk.Label(csearcher, text = str(e), font=myfont, bg = '#00aced')
            error_lbl.grid(row=4)
    search_lbl = tk.Label(csearcher, text = 'Search users:', font=myfont,bg = '#00aced')
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    search_entry1 = tk.Entry(csearcher, textvariable = v1, font=myfont, highlightthickness = 0)
    search_entry2 = tk.Entry(csearcher, textvariable = v2, font=myfont, highlightthickness = 0)
    #txt = v.get()
    search_bttn = tk.Button(csearcher, text = ' search ', command = compare, font=myfont, bg = '#00aced', highlightthickness = 0)
    search_lbl.grid(row=0)
    search_entry1.grid(row=1)
    search_entry2.grid(row=2)
    search_bttn.grid(row=3)
    csearcher.grid_columnconfigure(0,pad=50)
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
        if user1.get('status') == 'Banned':
            url1 = url_ban
        elif user1.get('status') == 'Deleted':
            url1 = url_del
        else:
            url1 = url_def
    url2 = user2.get('image')
    if url2 == 'N/A':
        if user2.get('status') == 'Banned':
            url2 = url_ban
        elif user2.get('status') == 'Deleted':
            url2 = url_del
        else:
            url2 = url_def
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
    cview.configure(bg = '#00aced')
    cview.title('User Comparison')

    #cview.geometry('800x300')
    f1 = tk.Frame(cview, bg = '#00aced')
    f2 = tk.Frame(cview, bg = '#00aced')
    f3 = tk.Frame(cview, bg = '#00aced')
    header = tk.Message(f1, text = 'Comparison of:\n'+username1+'\n'+username2, font=myfont, width=400,bg = '#00aced')
    user1_lbl = tk.Label(f1, text = username1, font=myfont, bg = '#00aced')
    img1_lbl = tk.Label(f1, image = img1, bg = '#00aced')
    status1_lbl = tk.Label(f1, text = 'Status: '+user1.get('status'), font=myfont, bg = '#00aced')
    desc1_lbl = tk.Message(f1, text = 'Description: '+desc1, width = 200, font=myfont, bg = '#00aced')
    followers1_lbl = tk.Label(f1, text = 'Followers: '+user1.get('followers'), font=myfont, bg = '#00aced')
    following1_lbl = tk.Label(f1, text = 'Following: '+user1.get('friends'), font=myfont, bg = '#00aced')
    tweets1_lbl = tk.Label(f1, text = 'Tweets: '+user1.get('tweets'), font=myfont, bg = '#00aced')
    #
    user2_lbl = tk.Label(f1, text = username2, font=myfont, bg = '#00aced')
    img2_lbl = tk.Label(f1, image = img2, bg = '#00aced')
    status2_lbl = tk.Label(f1, text = 'Status: '+user2.get('status'), font=myfont, bg = '#00aced')
    desc2_lbl = tk.Message(f1, text = 'Description: '+desc2, width = 200, font=myfont, bg = '#00aced')
    followers2_lbl = tk.Label(f1, text = 'Followers: '+user2.get('followers'), font=myfont, bg = '#00aced')
    following2_lbl = tk.Label(f1, text = 'Following: '+user2.get('friends'), font=myfont, bg = '#00aced')
    tweets2_lbl = tk.Label(f1, text = 'Tweets: '+user2.get('tweets'), font=myfont, bg = '#00aced')
    #
    #comp = user1.compare(user2)
    RT_lbl = tk.Label(f3, text = 'Retweeted users in common: '+comp['RTWeight'], font=myfont, bg = '#00aced')
    Ment_lbl = tk.Label(f3, text = 'Mentioned users in common: '+comp['MentWeight'], font=myfont, bg = '#00aced')
    HT_lbl = tk.Label(f3, text = 'Hashtags in common: '+comp['HTWeight'], font=myfont, bg = '#00aced')
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
menu.configure(bg = '#00aced')
#menu.configure(bg = '#1da1f2')
#menu.geometry('408x200')
#network_bttn = tk.Button(window, text = 'Create network', command = network_menu)
search_bttn = tk.Button(menu, text = 'Search by username', command = search_user, font=myfont, highlightthickness = 0, width = 20)
compare_bttn = tk.Button(menu, text = 'Compare users', command = compare_search, font=myfont, highlightthickness = 0, width = 20)
#network_bttn.pack()
search_bttn.grid(row=0)
compare_bttn.grid(row=1)
menu.grid_columnconfigure(0,pad='50')
menu.mainloop()
