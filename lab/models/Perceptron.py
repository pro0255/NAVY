import numpy as np
from lab.cv1.visualizer import LineVisualizer


def signum(X, weights, bias):
    res = np.dot(X, weights) + bias
    if res > 0:
        return 1
    elif res < 0:
        return -1
    else:
        return 0


def error(y, y_guess):
    return y - y_guess


lv = LineVisualizer()


class Perceptron:
    def __init__(self, learning_rate, X_l):
        self.learning_rate = learning_rate
        self.weights = np.random.uniform(0, 1, X_l + 1)

    def recalculate_weights(self, error, x):
        new_weights = (
            self.weights[0 : len(self.weights) - 1] + error * self.learning_rate * x
        )
        bias = self.weights[-1] + error * self.learning_rate
        concatanated = list(new_weights) + [bias]
        return np.array(concatanated)

    def fit(self, X, y, epoch=1):
        for _ in range(epoch):
            y_guesses = []
            for index, x in enumerate(X):
                y_guess = signum(
                    x, self.weights[0 : len(self.weights) - 1], self.weights[-1]
                )
                y_guesses.append(y_guess)
                current_error = error(y[index], y_guess)
                self.weights = self.recalculate_weights(current_error, x)

            lv.draw_train(X, y_guesses)

    def predict(self, X):
        y_prediction = [
            signum(x, self.weights[0 : len(self.weights) - 1], self.weights[-1])
            for x in X
        ]

        res =  np.array(y_prediction)
        lv.draw_test(X, res)
        return res
        
