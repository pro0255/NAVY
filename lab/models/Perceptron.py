import numpy as np
from lab.cv1.visualizer import LineVisualizer


def signum(X, weights, bias):
    """Signum activation function which returns

    res > 0 <-> 1
    res = 0 <-> 0
    res < 0  <-> -1
    """
    res = np.dot(X, weights) + bias
    if res > 0:
        return 1
    elif res < 0:
        return -1
    else:
        return 0


def error(y, y_guess):
    return y - y_guess


class Perceptron:
    def __init__(self, learning_rate, X_l):
        self.lv = LineVisualizer()
        self.learning_rate = learning_rate
        self.weights = np.random.uniform(0, 1, X_l + 1)

    def recalculate_weights(self, error, x):
        """Relaculates weights
        Args:
            error (int): Represents error which was created due to bad prediction
            x (int[]): Points [x, y]
        Returns:
            [int[]]: Recalculated weights (net learns from error)
        """
        new_weights = (
            self.weights[0 : len(self.weights) - 1] + error * self.learning_rate * x
        )
        bias = self.weights[-1] + error * self.learning_rate
        concatanated = list(new_weights) + [bias]
        return np.array(concatanated)

    def fit(self, X, y, epoch=1):
        """Method represents learning process of net
        Args:
            X (int[][]): Array of Points [x, y]
            y (int[]): Array of labels which represents position of point [-1, 0, 1]
            epoch (int, optional): This number represents how many times will run learning process. Defaults to 1.
        """
        for _ in range(epoch):
            y_guesses = []
            for index, x in enumerate(X):
                y_guess = signum(
                    x, self.weights[0 : len(self.weights) - 1], self.weights[-1]
                )
                y_guesses.append(y_guess)
                current_error = error(y[index], y_guess)
                self.weights = self.recalculate_weights(current_error, x)

            self.lv.draw_train(X, y_guesses)

    def predict(self, X):
        """Method represents prediction process of unknown data
        Args:
            X (int[][]): Array of Points [x, y]
        Returns:
            [int[]]: Predicted positions connected to input Points
        """
        y_prediction = [
            signum(x, self.weights[0 : len(self.weights) - 1], self.weights[-1])
            for x in X
        ]

        res = np.array(y_prediction)
        self.lv.draw_test(X, res)
        return res
