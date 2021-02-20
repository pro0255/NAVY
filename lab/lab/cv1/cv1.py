import numpy as np
from lab.cv1 import CONSTANTS
from utils.generatePoints import generatePointsInBounds
from utils.resolveYForPts import resolveYForPts
from models.Perceptron import Perceptron
from utils.accuracy import accuracy


def cv1():
    perceptron = Perceptron(CONSTANTS.LEARNING_RATE, 2)

    X_train = generatePointsInBounds(
        CONSTANTS.LEFT_PTS, CONSTANTS.RIGHT_PTS, CONSTANTS.NUMBER_OF_PTS
    )
    y_train = resolveYForPts(X_train)

    X_test = generatePointsInBounds(
        CONSTANTS.LEFT_PTS, CONSTANTS.RIGHT_PTS, CONSTANTS.NUMBER_OF_PTS
    )
    y_test = resolveYForPts(X_test)

    perceptron.fit(X_train, y_train, CONSTANTS.NUMBER_OF_EPOCHS)
    y_prediction = perceptron.predict(X_test)

    acc = accuracy(y_prediction, y_test)
    print(f"Accuracy is {acc}")
