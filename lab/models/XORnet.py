from lab.cv2 import CONSTANTS 

class XORnet:
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate

    def fit(self, X, y):
        for i in range(CONSTANTS.NUMBER_OF_EPOCHS):
            print(f'Epoch {i}')
            self.forward_propagation()
            self.back_propagation()

    def predict(self, X):
        print('prediction')

    def forward_propagation(self):
        print('forward_propagation')

    def back_propagation(self):
        print('back_propagation')




