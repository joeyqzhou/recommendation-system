'''
Created on Nov 1, 2015

@author: joey
'''
import random
import numpy as np
import math
import data_preparation as dp



def userSimilarityRating(data):
    #Build the inverse table: 
    #item_users(key:item,value:{user,rating_user_have give the item})
    item_users = dict()
    for useri , items_rating in data.items():
        for itemj in items_rating.keys():
            if itemj not in item_users:
                item_users[itemj] = list()
            item_users[itemj].append({useri:items_rating[itemj]})
    
    #cos(user_i,user_j) = cosine similarity between (x(i) and x(j))
    # x(i): is the vector represent the user that each column is a moive. if user i had
    # seen the moive, then the number in the vector is the rating, otherwise zero.
    #key:useri
    #value:dict,key:userj,value:the number of movie both useri and uerj have seen 
    C = dict()

    #key:userId
    #value:the total item number of userId
    N = dict()
    

    
    for itemi, users_rating in item_users.items():
        for userj_rating_i in users_rating:
            userj = userj_rating_i.keys()[0]
            if userj not in C:
                N[userj] = 0
                C[userj] = {}
            N[userj] += userj_rating_i[userj]#rating_{usrj_to_itemi}
            for userk_rating_i in users_rating:
                userk = userk_rating_i.keys()[0]
                if userj != userk:
                    if userk not in C[userj]:
                        C[userj][userk] = 0
                    C[userj][userk] += userj_rating_i[userj] * userk_rating_i[userk]
                
    #caluate similarity by normalize C
    W = dict()
    for u , related_users in C.items():
        if u not in W:
            W[u] = {}
        for v, cuv in related_users.items():
                W[u][v] = cuv / math.sqrt( N[u] * N[v] )
    
    return W 



#W: similarity between two users. key:user i,value:dict(key:user j,value Wij)
#R: users'rating for item 
def UserCF_to_predict_raring(user,item,trainData,W,K=6):

    predict_rating = 0.0
    unnormalized_predict_rating = 0.0
    
    count = 0
    norm_similarity = 0.0
    for useri, similarity in sorted(W[user].items(), \
                                key = lambda x:x[1], reverse=True):
        if item in trainData[useri].keys():
            count += 1
            if count >=K:
                break
            unnormalized_predict_rating += similarity * trainData[useri][item]
            norm_similarity += similarity
            

    if count < K/2:
        return -1 #cant predict, here can be replaced by the average value of the item get
    else:   
        predict_rating = unnormalized_predict_rating/norm_similarity
        return predict_rating



def Evaluation_CF_to_predict_rating(train, test, K):
    sum_squared_error = 0.0
    rmse = 0.0
    W = userSimilarityRating(train)   
    count = 0 
    print "Evaluation"
    for user in train.keys():
        if user in test.keys():
            test_user_item = test[user] #key: item , value: rating user to item
            for itemi in test_user_item.keys():
                predict_rating = UserCF_to_predict_raring(user,itemi,train,W,K)
                if predict_rating != -1:
                    count += 1
                    real_rating = test[user][itemi]
                    rmse += (predict_rating - real_rating)**2
    print "predict number:", count
    rmse = np.sqrt(rmse/count)
    return rmse

if __name__ == "__main__":
    data = dp.readMoiveIdRatingFromRatings("ratings.dat","::")
    trainData, testData = dp.splitRatingData(data)
    print Evaluation_CF_to_predict_rating(trainData, testData, 20)  