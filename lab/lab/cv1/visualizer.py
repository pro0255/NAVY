import matplotlib.pyplot as plt
import numpy as np
from utils.equation import equation
from lab.cv1 import CONSTANTS


class LineVisualizer:
    def __init__(self):
        pass

    def create_clusters(self, X, y_guess):
        x_points = X[:, 0]
        y_points = X[:, 1]

        x_up = []
        y_up = []

        x_down = []
        y_down = []

        x_on = []
        y_on = []

        for index, y in enumerate(y_guess):
            if y == -1:
                x_down.append(x_points[index])
                y_down.append(y_points[index])
            elif y == 1:
                x_up.append(x_points[index])
                y_up.append(y_points[index])
            else:
                x_on.append(x_points[index])
                y_on.append(y_points[index])

        return ((x_up, y_up), (x_on, y_on), (x_down, y_down))

    def draw_clusters(self, clusters):
        up, on, down = clusters
        plt.scatter(up[0], up[1], c=CONSTANTS.COLOR_UP, label="nad")
        plt.scatter(on[0], on[1], c=CONSTANTS.COLOR_ON, label="na")
        plt.scatter(down[0], down[1], c=CONSTANTS.COLOR_DOWN, label="pod")

    def draw(self, X, y_guess):
        point_left = [CONSTANTS.LEFT_PTS, equation(CONSTANTS.LEFT_PTS)]
        point_right = [CONSTANTS.RIGHT_PTS, equation(CONSTANTS.RIGHT_PTS)]

        x_values = [point_left[0], point_right[0]]
        y_values = [point_left[1], point_right[1]]

        self.draw_clusters(self.create_clusters(X, y_guess))

        plt.plot(x_values, y_values, c="gray")
        plt.legend()
        plt.show()
