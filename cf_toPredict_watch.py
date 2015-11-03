# -*- coding: utf-8 -*-
'''
Created on 2015.05
Update 2015.09

@author: Joeyqzhou
'''

import random
import numpy as np
import math
import data_preparation as np


    
    

#To compute the user similarity of all data
#input
#data:dict(),key:user,value:[] list that contains items
#type: choose different similarity mode, type=0 is the default choice

# W[usr_i][usr_j] = C[i][j]/sqrt(N[i] * N[j]) 
def userSimilarity(data):
    #Build the inverse table: item_users(key:item,value:list)
    item_users = dict()
    for useri , items in data.items():
        for itemj in items:
            if itemj not in item_users:
                item_users[itemj] = list()
            item_users[itemj].append(useri)
    
    # C[i][j] is the absolute times that user_i and user_j have seen the same moive
    #key:useri
    #value:dict,key:userj,value:the number of movie both useri and uerj have seen 
    C = dict()
    
    
    # N[i] is the total number user_i have seen
    #key:userId
    #value:the total item number of userId
    N = dict()
    
    
    for itemi , users in item_users.items():
        for useri in users:
            if useri not in N:
                N[useri] = 0
            N[useri] += 1
            for userj in users:
                if useri != userj:
                    if useri not in C:
                        C[useri] = dict()
                    if userj not in C[useri]:
                        C[useri][userj] = 1
                    else:  
                        C[useri][userj] += 1
    
    #Normalizing C to get W
    #key:useri
    #value:dict,key:userj,value:simlarity(useri,userj)
    W = dict()

    for useri, related_user in C.items():
        W[useri] = dict()
        for userj in related_user:
            W[useri][userj] = C[useri][userj]*1.0/math.sqrt(N[useri]*N[userj])
        
    return W


#To recommend user a item list

# trainData: as the name
#data:dict(),key:user,value:[] list that contains items

#W is similarity dictionary
#key:useri
#value:dict,key:userj,value:simlarity(useri,userj)

#K: choose the nearest K neighbor of the user


#output:
#recommendationList:type(dict),key(item),val(how much you want to recommend)
def userCF_Recommend(user,trainData,W,K=6):
    recommendationList = dict()
    alreadyUsedItem = trainData[user]
    
    for useri , similar_useri in sorted(W[user].items(), \
                                        key = lambda x:x[1],\
                                        reverse=True)[0:K]:
        for itemj in trainData[useri]:
            if itemj not in alreadyUsedItem:
                if itemj not in recommendationList:
                    recommendationList[itemj] = 0
                recommendationList[itemj] += similar_useri
    
    return  sorted(recommendationList.items(), key = lambda x:x[1], reverse=True)     





def itemSimilarity(trainData):
    C = {}
    #key:item
    #value:key(itemj),value(absolute number seen by two users)
    N = {} 
    #key:item
    #value: len(item)  
    for user,items in trainData.items():
        for item in items:
            if item not in N:
                N[item] = 0
            N[item] += 1
            if item not in C:
                C[item] = {}
            for itemj in items:
                if itemj not in C[item]:
                    C[item][itemj] = 0
                C[item][itemj] += 1
                
    #key:item
    #value:key(itemj),value(simi(item,itemj))    
    W = {}
    for item, relatedItem_val in C.items():
        W[item] = {}
        for itemi in relatedItem_val:
            W[item][itemi] = C[item][itemi]*1.0/math.sqrt(N[item]*N[itemi])
        
    return W

def itemCF_Recommend(user,trainData,W,K=6):
    itemsAlreadyUsed = trainData[user]
    recomList = {}
    for itemi in itemsAlreadyUsed:
        for itemj, Wij in sorted(W[itemi].items(), key = lambda x:x[1], reverse = True)[0:K]:
            if itemj not in itemsAlreadyUsed:
                if itemj not in recomList:
                    recomList[itemj] = 0
                recomList[itemj] += Wij

    return sorted(recomList.items(), key = lambda x:x[1], reverse=True) 

#Calculate the recall of the CF
#train:training data
#test:testing data
#Recommend at most N items for each user
def Evaluation_userCF(train, test, N):
    hit = 0
    totalTestItemNum = 0.0
    totalRecommendationNum = 0.0
    W = userSimilarity(train)
    for user in train.keys():
        if user in test.keys():
            test_user_item = test[user]
            totalTestItemNum += len(test_user_item)
            recommendationList = userCF_Recommend(user,train,W) #Only get the movie ID
            recommendationList = [recomItem[0] for recomItem in recommendationList]
            if len(recommendationList)>N: #If the recommendation list's length is larger than N
                recommendationList = recommendationList[0:N]
                totalRecommendationNum += N
            else:
                totalRecommendationNum += len(recommendationList)
            for itemi in recommendationList:
                if itemi in test_user_item:
                    hit += 1
    return hit*1.0/totalTestItemNum,hit*1.0/totalRecommendationNum

def Evaluation_itemCF(train, test, N):
    hit = 0
    totalTestItemNum = 0.0
    totalRecommendationNum = 0.0
    W = itemSimilarity(train)
    for user in train.keys():
        if user in test.keys():
            test_user_item = test[user]
            totalTestItemNum += len(test_user_item)
            recommendationList = itemCF_Recommend(user,train,W) #Only get the movie ID
            recommendationList = [recomItem[0] for recomItem in recommendationList]
            if len(recommendationList)>N: #If the recommendation list's length is larger than N
                recommendationList = recommendationList[0:N]
                totalRecommendationNum += N
            else:
                totalRecommendationNum += len(recommendationList)
            for itemi in recommendationList:
                if itemi in test_user_item:
                    hit += 1
    return hit*1.0/totalTestItemNum,hit*1.0/totalRecommendationNum


#The begining of the main
if __name__ == "__main__":
    data = np.readMoiveIdFromRatings()
    trainData, testData = np.splitData(data)
    [recall,precision] = Evaluation_userCF(trainData, testData, 7)
    print "user CF, recall:", recall, " precision: ", precision
    [recall,precision] = Evaluation_itemCF(trainData, testData, 7)
    print "item CF, recall:", recall, " precision: ", precision

       
    