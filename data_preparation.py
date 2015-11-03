'''
Created on Nov 2, 2015

@author: joeyqzhou
'''


import random
import numpy as np
import math


#Input:'ratings.dat'
#A example
#1::1193::5::978300760#
#UserId::Moive::Ratings::Timestamp
#Output:userMoiveData,dictionary,key:userId,value:[{moiveid:rating},...]
def readMoiveIdRatingFromRatings(filename='smallData_u.data',splitSymbol="\t"):
    fileRating = open(filename)
    userMoiveData = dict()
    for line in fileRating:
        piece = line.split(splitSymbol)
        id = piece[0]
        moiveId = piece[1]
        rating = piece[2]
        if id not in userMoiveData:
            userMoiveData[id] = {}
        userMoiveData[id][moiveId] = rating
    
    return userMoiveData


#Input:'ratings.dat'
#A example
#1::1193::5::978300760#
#UserId::Moive::Ratings::Timestamp
#Output:userMoiveData,dictionary,key:userId,value:[moiveid...]

def readMoiveIdFromRatings(filename='smallData_u.data',splitSymbol="\t"):
    fileRating = open(filename)
    userMoiveData = dict()
    for line in fileRating:
        piece = line.split(splitSymbol)
        id = piece[0]
        moiveId = piece[1]
        if id not in userMoiveData:
            userMoiveData[id] = []
        userMoiveData[id].append(moiveId)
    
    return userMoiveData

#To split data into (M-1) piece of training and 1 piece of testing data
#k is a random seclected number to between (1,M)
#seed is to generate the random number with certain mode (seed)
def splitData(data,M=8,k=3,seed=1):
    test = dict()
    train = dict()
    random.seed(seed)
    for user, items in data.items():
        for itemj in items:
            if random.randint(0,M) ==k:
                if user not in test:
                    test[user] = list()
                test[user].append(itemj)
            else:
                if user not in train:
                    train[user] = list()
                train[user].append(itemj)
    return train,test 


def splitRatingData(data,M=8,k=3,seed=1):
    test = dict()
    train = dict()
    random.seed(seed)
    for user, items_rating in data.items():
        for item_rating in items_rating.items():
            if random.randint(0,M) ==k:
                if user not in test:
                    test[user] = dict()
                test[user][item_rating[0]] = float( item_rating[1] ) #cast string to float
            else:
                if user not in train:
                    train[user] = dict()
                train[user][item_rating[0]] = float( item_rating[1] ) #cast string to float
    return train,test   