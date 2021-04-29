from lab.cv10.CONSTANTS import x_0, N, DIS_R, percentil, DECIMALS, R_TRAIN_SIZE
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
from itertools import product


def logistic_map(x, r):
    x_1 = r*x*(1-x)
    return x_1



def generate_training_set(res):
    X = []
    Y = []
    for k in res.keys():
        values = res[k]
        product_res = list(product([k], values))
        # print(product_res)
        r, v = zip(*product_res)

        x_l = list(r)
        y_l = list(v)
        # X = X + list(x)
        # Y = Y + list(y)

        l = list(product_res)
        add = l if len(l) > R_TRAIN_SIZE else l + l * (len(l) - R_TRAIN_SIZE)

        negative = [] 
        while len(negative) < len(add):
            n = np.random.uniform(0, 1)
            if round(n, DECIMALS) not in y_l:
                negative.append(n)
                
        negative = list(zip([x_l[0]*len(negative)], negative))
        negative = [list(t) for t in negative]



        X += add
        X += negative
        Y += [1] * len(add)
        Y += [0] * len(negative)
    return X, Y

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
        casted = list(np.array(xs).round(decimals=DECIMALS))[-PICK_SIZE:]
        picked = np.unique(casted)
        res[r] = picked
       
        x = [r] * len(picked) 
        y = picked
        plt.scatter(x, y, c='gray', s=1)
        r += step

    #LEARN NET

    model = Sequential()
    model.add(Input(shape=(2)))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])


    X_train, Y_train = generate_training_set(res)

    EPOCHS = 1000

    model.fit(
        X_train, 
        Y_train,     
        epochs=EPOCHS,
        shuffle=True
    )

    #PREDICT

    r = 0
    step = 0.1
    while r < DIS_R:
        X = np.linspace(0, 1, 1000)
        vec_r = [r] * len(X)
        X = list(zip(vec_r, X))
        X = [list(x) for x in X]

        pred = model.predict(np.array(X))
        indicies = np.argwhere(pred >= 0.5).flatten()
        plot_values = np.array(X)[indicies]


        r += step
        if(len(plot_values) > 0):
            x, y = zip(*plot_values)
            plt.scatter(x, y, c='red', s=1)


    #PLOT

    plt.grid()
    plt.title('Logistic map')
    plt.xlabel('r')
    plt.ylabel('x')
    plt.show()