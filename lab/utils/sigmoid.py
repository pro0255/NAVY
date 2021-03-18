import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_(x):
    return x * (1 - x)
