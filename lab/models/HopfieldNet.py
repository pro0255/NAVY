from lab.cv2 import CONSTANTS
import numpy as np
from utils.sigmoid import sigmoid, sigmoid_
from utils.error import error
from lab.cv3.utils.from_pattern2matrix import from_pattern2matrix
from lab.cv3.utils.replace0_to_1 import replace1_to_0, replace0_to_1
from utils.signum import signum

debug = False


class HopfieldNet:
    def __init__(self):
        self.W = None
        self.pattern_shape = None

    def save_pattern(self, pattern):
        print(pattern.shape)
        if self.pattern_shape == None:
            self.pattern_shape = pattern.shape
        if pattern.shape != self.pattern_shape:
            print("Pattern was not saved cause bad shape")
            return
        W = from_pattern2matrix(pattern)
        if self.W is None:
            self.W = W
        else:
            self.W += W
        print("Saved pattern in net")

    def recover_sync(self, destroyed_picture):
        vector = np.array(destroyed_picture.flatten())
        replace0_to_1(vector)
        vfunc = np.vectorize(signum)
        res = vfunc(np.dot(vector, self.W))
        if debug:
            print("vector", vector)
            print("res", res)
        replace1_to_0(res)

        return res.reshape(self.pattern_shape)

    def recover_async(self, destroyed_picture):
        vector = np.array(destroyed_picture.flatten())
        replace0_to_1(vector)
        gen = 0
        while True:
            print(f"Gen: {gen}")
            gen += 1
            old_gen_vector = np.copy(vector)
            for cI in range(self.W.shape[1]):
                column = self.W[:, cI]
                res = signum(np.dot(vector, column))
                vector[cI] = res
            if np.all(old_gen_vector == vector):
                break

        replace1_to_0(vector)
        return vector.reshape(self.pattern_shape)
