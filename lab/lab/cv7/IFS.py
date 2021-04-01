import numpy as np
import pandas as pd
from lab.cv7.CONSTANTS import VERBOSE, START_VECTOR


r_max = 10


class IFS:
    def __init__(self, csv_model, p):
        self.csv_model = csv_model
        self.p = p

    def calculate_cords(self, input_v):
        res = []
        r = np.random.randint(0, 4)
        multiplication = self.csv_model.iloc[r, 1:r_max].values
        addition = self.csv_model.iloc[r, r_max:].values

        n_input = np.array(input_v)
        n_m = np.array(multiplication).reshape(-1, 3)
        n_a = np.array(addition)

        c_r = n_m @ n_input + n_a

        if VERBOSE:
            print(pd.DataFrame(n_input))
            print(pd.DataFrame(n_m))
            print(pd.DataFrame(n_a))
            print(pd.DataFrame(c_r))

        res = c_r.flatten()
        return res

    def process(self, m_g):
        res = [START_VECTOR]
        for _ in range(m_g):
            input_v = res[-1]
            res.append(self.calculate_cords(input_v))
        res = np.array(res)
        x = res[:, 0]
        y = res[:, 1]
        z = res[:, 2]
        return x, y, z
