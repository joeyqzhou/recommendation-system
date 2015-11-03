# -*- coding: utf-8 -*-
'''
Created on 2015.05
update on 2015.08

@author: Joey 
'''
import random
import numpy as np
import math
import data_preparation as dp
#from cf_toPredict_watch import *

 

def userSimilarityRating(data,type='0'):
    #Build the inverse table: item_users(key:item,value:list)
    item_users = dict()
    for useri , items_rating in data.items():
        for itemj in items_rating.keys():
            if itemj not in item_users:
                item_users[itemj] = list()
            item_users[itemj].append(useri)
    
    #Calculate the absolute relative time
    #key:useri
    #value:dict,key:userj,value:the number of movie both useri and uerj have seen 
    C = dict()

    #key:userId
    #value:the total item number of userId
    N = dict()
    

    
    for itemi, users in item_users.items():
        for userj in users:
            if userj not in C:
                N[userj] = 0
                C[userj] = {}
            N[userj] += 1
            for userk in users:
                if userj != userk:
                    if userk not in C[userj]:
                        C[userj][userk] = 0
                    C[userj][userk] += 1
                
    #caluate similarity by normalize C
    W = dict()
    for u , related_users in C.items():
        if u not in W:
            W[u] = {}
        for v, cuv in related_users.items():
                W[u][v] = cuv / math.sqrt( N[u] * N[v] )
    
    return W 


#user collaborative filtering using ratings
#user: the user to recommend
#W: similarity between two users. key:user i,value:dict(key:user j,value Wij)
#R: users'rating for item 
def RatingUserCFRecommencd(user,trainData,W,K=6):

    normk = dict() #normalization coefficient
    already_used_item = trainData[user].keys()
    recomList = dict() #the sum of unnormalized rating
    
    for useri, similarity in sorted(W[user].items(), \
                                key = lambda x:x[1], reverse=True)[0:K]:
        for itemj in trainData[useri].keys():
            if itemj not in already_used_item:
                if itemj not in recomList:
                    recomList[itemj] = 0
                    normk[itemj] = 0
                recomList[itemj] += similarity*trainData[useri][itemj]
                #normk[itemj] += similarity
                
#The performance of predicting the average raing is so poor. Because the has to by the sum of the similarity
#the sum of similarity*rating is a better CF than only the similarity.
#     for itemi in recomList.keys():
#         recomList[itemi] /= normk[itemi]
                
    return  sorted(recomList.items(), key = lambda x:x[1], reverse=True)
    



def Evaluation_CF_rating(train, test, N):
    hit = 0
    totalTestItemNum = 0.0
    totalRecommendationNum = 0.0
    W = userSimilarityRating(train)    
    print "Evaluation"
    for user in train.keys():
        if user in test.keys():
            test_user_item = test[user]
            totalTestItemNum += len(test_user_item)
            recommendationList = RatingUserCFRecommencd(user,train,W)
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

if __name__ == "__main__":
    data = dp.readMoiveIdRatingFromRatings()
    trainData, testData = dp.splitRatingData(data)
    print Evaluation_CF_rating(trainData, testData, 7)  