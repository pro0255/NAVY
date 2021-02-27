import numpy as np

def error(y, y_guess):
    return 1/2*np.power((y-y_guess), 2)