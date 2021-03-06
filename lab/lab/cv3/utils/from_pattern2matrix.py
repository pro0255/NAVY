from lab.cv3.utils.replace0_to_1 import replace0_to_1
from lab.cv3.utils.create_column_vector import create_column_vector
from lab.cv3.utils.create_weighted_matrix import create_weighted_matrix
from lab.cv3.utils.sub_I import sub_I

def from_pattern2matrix(pattern):
    replace0_to_1(pattern)
    vec = create_column_vector(pattern)
    W = create_weighted_matrix(vec)
    sub_I(W)
    return W