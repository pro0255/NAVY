
import numpy as np


def accuracy(y_pred, y_true):
    correct_prediction = np.sum(y_pred == y_true)
    size = len(y_pred)
    return correct_prediction/size 

