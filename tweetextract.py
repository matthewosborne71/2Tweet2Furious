# By Austin Antoniou, in Collaboration with Dan MacGregor and Matt Osborne
# as part of the Erdos Institute Summer 2018 Code Bootcamp
# 31 May 2018

# tweetextract.py contains functions for extracting particular features
# of tweets; e.g., mentions, hashtags, and the user being retweeted
# (if applicable)

import re

def isRT(tweetstring):
    if tweetstring[:4] == 'RT @':
        isRT = 'Y'
    else:
        isRT = 'N'

    return isRT

def hashtags(tweetstring):
    #given the text of a tweet as a string, this function returns a list of
    #all hashtags which were used in the tweet
    hashtag = [re.sub(r"(\W+)$", "", j) for j in set([i for i in tweetstring.split() if i.startswith("#")])]

    for i in range(len(hashtag)):
        if ',' in hashtag[i]:
            hashtag[i] = hashtag[i].split(',')[0]
        if 'http' in hashtag[i]:
            hashtag[i] = hashtag[i].split('http')[0]


    return hashtag


def mentions(tweetstring):
    #given the text of a tweet as a string, this function returns a string of
    #all twitter usernames mentioned in the tweet, separated by spaces
    if tweetstring[:4] == 'RT @':
        tweetstring = tweetstring[4:]

    mentions = [re.sub(r"(\W+)$", "", j) for j in set([i for i in tweetstring.split() if i.startswith("@")])]

    for i in range(len(mentions)):
        if ',' in mentions[i]:
            mentions[i] = mentions[i].split(',')[0]
        if '.' in mentions[i]:
            mentions[i] = mentions[i].split('.')[0]
        if 'http' in mentions[i]:
            mentions[i] = mentions[i].split('http')[0]
        if ':' in mentions[i]:
            mentions[i] = mentions[i].split(':')[0]
        if "'" in mentions[i]:
            mentions[i] = mentions[i].split("'")[0]


    return mentions

def RTing(tweetstring):
    #given the text of a tweet as a string, this function returns the
    #username being retweeted, if applicable, or 'NONE; if the tweet is original
    #THIS DEPENDS ON THE FORMAT OF A RETWEET BEING:
    #"RT @retweeteduser content of the original tweet"
    if tweetstring[:4] == 'RT @':
        RTuser = ''
        for char in tweetstring[4:]:
            if char != ' ':
                RTuser += char
            else:
                return RTuser
    else:
        return 'NONE'

def extract(tweetstring):
    #in: the text of a tweet as a string
    #out: a tuple whose entries are
    #(1) a list of mentions made
    #(2) a list of hashtags used
    tweetstring += ' '
    mentions, hashtags = ('','')
    mrecord,hrecord = False,False
    for char in tweetstring:
        if char == '@':
            mrecord = True
        elif char == '#':
            hrecord = True
        if mrecord: # if '@' found, record characters until a space is found
            mentions += char
            if char == ' ':
                mrecord = False
        if hrecord: # if '#' found, record characters until a space is found
            hashtags += char
            if char == ' ':
                hrecord = False
    return (mentions,hashtags)

import pandas as pd

def modify_tweetcsv(filepath):
    df = pd.read_csv(filepath)
    (df['RTing'],df['mentions'],df['hashtags'])=('','','')
    for i in range(len(df)):
        df.loc[i,'RTing'] = RTing(df['text'][i])
        ext = extract(df['text'][i])
        df.loc[i,'mentions'] = ext[0]
        df.loc[i,'hashtags'] = ext[1]
    return df
