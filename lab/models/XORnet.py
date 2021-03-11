from lab.cv2 import CONSTANTS 
import numpy as np
from utils.sigmoid import sigmoid, sigmoid_
from utils.error import error

class XORnet:
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate
        self.weights_H = np.random.uniform(size=(2, 2))
        self.bias_H = np.random.uniform(size=(1, 2))
        self.weights_O = np.random.uniform(size=(2, 1))
        self.bias_O = np.random.uniform(size=(1, 1))

        self.net1 = None
        self.net2 = None
        self.net3 = None




    def fit(self, X, y):
        for i in range(CONSTANTS.NUMBER_OF_EPOCHS):
            for i in range(len(X)):
                current_x = np.array(X[i])
                current_y = np.array(y[i])
                self.forward_propagation(current_x)
                self.back_propagation(current_x, current_y)

    def predict(self, X):
        res = []
        for x in X:
            self.forward_propagation(x)
            res.append(self.net3)
        return res

    def forward_propagation(self, current_x):
        #0 -> w1,w3
        self.net1 = sigmoid(np.dot(current_x, self.weights_H[0]) + self.bias_H[0][0])
        #1 -> w2,w4
        self.net2 = sigmoid(np.dot(current_x, self.weights_H[1]) + self.bias_H[0][1])
        #output
        self.net3 = sigmoid(self.net1 * self.weights_O[0][0] + self.net2 * self.weights_O[1][0] + self.bias_O[0][0])
        

    def back_propagation(self, current_x, current_y, debug_print=False):
        error_ = error(current_y, self.net3) #missing '-' #error / out3

        delta_O = error_ * sigmoid_(self.net3) #out3 / net3
        #net3 = w5*net1 + w6*net2 + b_o
        #w5
        update_w5 = delta_O[0] * self.net1 * self.learning_rate #net3 / w5
        #w6
        update_w6 = delta_O[0] * self.net2 * self.learning_rate #net3 / w6
        #bias O
        update_bias_O = delta_O[0] * self.learning_rate

        #error H
        error_h_w5 = update_w5 * self.weights_O[0][0] #w5
        error_h_w6 = update_w6 * self.weights_O[1][0] #w6

        #delta H
        delta_h_w5 = error_h_w5 * sigmoid_(self.net1) #w5 path
        delta_h_w6 = error_h_w6 * sigmoid_(self.net2) #w6 path


        # print(self.bias_O)
        # print(self.bias_H)
        #w1, w2 -> x1
        update_w12 = delta_h_w5 * current_x[0] * self.learning_rate
        #w3, w4 -> x2
        update_w34 = delta_h_w6 * current_x[1] * self.learning_rate
        #bias H
        update_bias_H_1 = delta_h_w5 * self.learning_rate
        update_bias_H_2 = delta_h_w6 * self.learning_rate
        
        #update
        self.weights_O[0][0] += update_w5 
        self.weights_O[1][0] += update_w6
        self.weights_H[0][0] += update_w12
        self.weights_H[1][0] += update_w12
        self.weights_H[0][1] += update_w34
        self.weights_H[1][1] += update_w34
        self.bias_O += update_bias_O
        self.bias_H[0][0] += update_bias_H_1
        self.bias_H[0][1] += update_bias_H_2


