from lab.cv2 import CONSTANTS 
import numpy as np
from utils.sigmoid import sigmoid
class XORnet:
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate
        self.weights_H = np.random.uniform(size=(2, 2))
        self.bias_H = np.random.uniform(size=(1, 2))
        self.weights_O = np.random.uniform(size=(1, 2))
        self.bias_O = np.random.uniform(size=(1, 1))
        self.out_H = None
        self.out_O = None

    def fit(self, X, y):

        print(X.shape)
        print(self.weights_H.shape)
        input_to_activation = X @ self.weights_H
        self.out_H = sigmoid(input_to_activation + self.bias_H)
        print(self.out_H)
        # for i in range(CONSTANTS.NUMBER_OF_EPOCHS):
        #     print(f'Epoch {i}')
        #     self.forward_propagation()
        #     self.back_propagation()

    def predict(self, X):
        print('prediction')

    def forward_propagation(self):
        print('forward_propagation')

    def back_propagation(self):
        print('back_propagation')




