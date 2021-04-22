from lab.cv10.CONSTANTS import x_0, N, DIS_R, percentil
import numpy as np
import matplotlib.pyplot as plt

def logistic_map(x, r):
    x_1 = r*x*(1-x)
    return x_1


def calc_logistic_map_for_r(r):
    xs = []
    x = x_0
    for _ in range(N):
        x = logistic_map(x, r)
        xs.append(x)
    return xs


def cv10():
    res = {}

    PICK_SIZE = int(N * percentil)

    r = 0
    step = 0.1
    while r < DIS_R:
        xs = calc_logistic_map_for_r(r)
        res[r] = xs

    
        casted = list(np.array(xs).round(decimals=6))[-PICK_SIZE:]

        picked = np.unique(casted)
        
        r += step


        x = [r] * len(picked) 
        y = picked

        plt.scatter(x, y, c='gray', s=1)


    #LEARN NET

    #PREDICT

    #PLOT

    plt.grid()
    plt.title('Logistic map')
    plt.xlabel('r')
    plt.ylabel('x')
    plt.show()