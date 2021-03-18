import numpy as np


def create_column_vector(matrix):
    vector = matrix.flatten()
    column = np.array([vector]).T
    return column
