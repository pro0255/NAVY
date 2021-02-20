import itertools
import numpy as np


def generatePointsInBounds(left, right, pts_size):
    X = []
    Y = []

    for _ in range(pts_size):
        X.append(np.random.uniform(left, right))
        Y.append(np.random.uniform(left, right))

    return np.array(list(zip(X, Y)))
