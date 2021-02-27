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
        self.out_H = None
        self.out_O = None

    def fit(self, X, y):
        for i in range(CONSTANTS.NUMBER_OF_EPOCHS):
            self.forward_propagation(X)
            self.back_propagation(X, y)

    def predict(self, X):
        self.forward_propagation(X)
        return self.out_O

    def forward_propagation(self, X):
        self.out_H = sigmoid(X @ self.weights_H + self.bias_H)
        self.out_O = sigmoid(self.out_H @ self.weights_O + self.bias_O)


    #make comments
    def back_propagation(self, X, y):
        errors = error(y, self.out_O)
        delta_O = errors * sigmoid_(self.out_O)
        error_H = delta_O @ self.weights_O.T
        delta_H = error_H * sigmoid_(self.out_H)

        self.weights_H = self.weights_H + X.T @ delta_H * self.learning_rate
        self.weights_O = self.weights_O + X.T @ delta_O * self.learning_rate

        self.bias_O += np.sum(delta_O,axis=0,keepdims=True) * self.learning_rate
        self.bias_H += np.sum(delta_H, axis=0, keepdims=True) * self.learning_rate





        





