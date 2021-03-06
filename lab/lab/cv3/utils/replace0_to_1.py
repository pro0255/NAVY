def replace0_to_1(matrix):
    #mutate input
    matrix[matrix == 0] = -1


def replace1_to_0(matrix):
    matrix[matrix == -1] = 0