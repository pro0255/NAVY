import numpy as np
from lab.cv3.CONSTANTS import pattern8, test_pattern

def replace0_to_1(matrix):
    #mutate input
    matrix[matrix == 0] = -1


def create_column_vector(matrix):
    vector = matrix.flatten()
    column = np.array([vector]).T
    return column

def create_weighted_matrix(vector):
    return vector @ vector.T 

def sub_I(matrix):
    np.fill_diagonal(matrix, 0)

def from_pattern2matrix(pattern):
    replace0_to_1(pattern)
    vec = create_column_vector(test_pattern)
    W = create_weighted_matrix(vec)
    sub_I(W)
    return W




def cv3():
    print(from_pattern2matrix(test_pattern))