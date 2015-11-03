'''
Created on Nov 2, 2015

@author: joeyqzhou
'''
import random
import numpy as np
import math
import data_preparation as dp

#trainData,dictionary,key:userId,value:[{moiveid:rating},...]
#u: the average value
#k: vector length
def svd_training(trainData,u=3,k=100,learning_rate=0.01,regularization = 1e-4):
    bias_i = {}
    bias_u = {}
    vec_i = {}
    vec_u = {}
    #initialization
    for user in trainData.keys():
        if user not in bias_u:
            bias_u[user] = 0.0
            vec_u[user] = ( np.random.rand(k) - 0.5 ) * 0.1
        for item in trainData[user].keys():
            if item not in bias_i:
                bias_i[item] = 0.0
                vec_i[item] = ( np.random.rand(k) - 0.5 ) * 0.1  
        
    #training
    count = 0
    for user in trainData.keys():
        for item in trainData[user].keys():
            count += 1
            
            r_ui = trainData[user][item]
            r_ui_hat = u + bias_u[user] + bias_i[item] + np.dot(vec_u[user],vec_i[item])
            e_ui = r_ui - r_ui_hat
            
            #update
            bias_u[user] += learning_rate * ( e_ui - regularization*bias_u[user])
            bias_i[item] += learning_rate * ( e_ui - regularization*bias_i[item])
            vec_i[item] += learning_rate * ( e_ui * vec_u[user]- regularization*vec_i[item])
            vec_u[user] += learning_rate * ( e_ui * vec_i[item]  - regularization*vec_u[user])
            
    print "training count: ",count        
    return bias_u, bias_i, vec_u, vec_i

def svd_predict(user,item,bias_u, bias_i, vec_u, vec_i,u=3):
    return u+bias_u[user]+bias_i[item]+np.dot(vec_u[user],vec_i[item])

def Evaluation_svd_predict(train, test):
    [bias_u, bias_i, vec_u, vec_i] = svd_training(trainData)

    mse_squared_sum = 0.0
    count = 0.0
    for user in test.keys():
        if user in bias_u:
            for item in test[user].keys():
                if item in bias_i:
                    count += 1
                    mse_squared_sum += ( test[user][item] - svd_predict(user,item,bias_u, bias_i, vec_u, vec_i) )**2
    print mse_squared_sum                
    print count
    return np.sqrt(mse_squared_sum/count) #RMSE
       
if __name__ == "__main__":
    data = dp.readMoiveIdRatingFromRatings("ratings.dat","::")
    trainData, testData = dp.splitRatingData(data)
    RMSE = Evaluation_svd_predict(trainData, testData)
    print "RMSE:",RMSE
    
    