import matplotlib.pyplot as plt
import numpy as np
from utils.equation import equation
from lab.cv1 import CONSTANTS


FIGURE_NAME = 'LineVisualizer - 4 * x - 5' 
TRAIN_PLOT_NAME = 'TRAIN'
TEST_PLOT_NAME = 'TEST'


class LineVisualizer:
    def __init__(self):
        self.fig = plt.figure(
            num=FIGURE_NAME,
            figsize=(20, 10),
            dpi=80,
            facecolor="w",
            edgecolor="k",
        )
        self.ax = self.fig.add_subplot(121, title=TRAIN_PLOT_NAME)
        self.ax2 = self.fig.add_subplot(122, title=TEST_PLOT_NAME)

        self.legendTrain=False
        self.ax.grid(True)
        self.ax2.grid(True)

        

    def create_clusters(self, X, y_guess):
        """Segments data accroding to position [-1, 0, 1]
        Args:
            X (int[][]): Points [x, y]
            y_guess (int[]): Labels [-1, 0, 1]
        Returns:
            [((int[], int[]), (int[], int[]), (int[], int[]))]: [description]
        """
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

    def draw_clusters(self, clusters, ax):
        up, on, down = clusters
        ax.scatter(up[0], up[1], c=CONSTANTS.COLOR_UP, label="over")
        ax.scatter(on[0], on[1], c=CONSTANTS.COLOR_ON, label="on")
        ax.scatter(down[0], down[1], c=CONSTANTS.COLOR_DOWN, label="under")


    def draw_train(self, X, y_guess):
        """Draws points and line from train data
        Args:
            X (int[][]): Points [x, y]
            y_guess (int[]): Labels [-1, 0, 1]
        """
        self.draw(X, y_guess, self.ax)

        if not self.legendTrain:
            self.legendTrain = True
            self.ax.legend()
        
    def draw_test(self, X, y_guess):
        """Draws points and line from test data
        Args:
            X (int[][]): Points [x, y]
            y_guess (int[]): Labels [-1, 0, 1]
        """
        self.draw(X, y_guess, self.ax2)
        


    def draw(self, X, y_guess, ax):
        """Draw to plot

        Args:
            X (int[][]): Points [x, y]
            y_guess (int[]): Labels [-1, 0, 1]
            ax (Object): Plot to draw
        """
        point_left = [CONSTANTS.LEFT_PTS, equation(CONSTANTS.LEFT_PTS)]
        point_right = [CONSTANTS.RIGHT_PTS, equation(CONSTANTS.RIGHT_PTS)]

        x_values = [point_left[0], point_right[0]]
        y_values = [point_left[1], point_right[1]]

        self.draw_clusters(self.create_clusters(X, y_guess), ax)
        ax.plot(x_values, y_values, c="gray")



        plt.draw()
        plt.pause(CONSTANTS.PAUSE_PLOT_TIME)

