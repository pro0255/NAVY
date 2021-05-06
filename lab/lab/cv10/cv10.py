from lab.cv10.CONSTANTS import x_0, N, DIS_R, percentil, DECIMALS, R_TRAIN_SIZE, STEP, START_R, N_START_R, N_DIS_R, START_TRAIN_R, END_TRAIN_R, TRAIN_SPACE_TIMES
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
from itertools import product


def logistic_map(x, r):
    x_1 = r*x*(1-x)
    return x_1



def get_non_net_points():
    res = {}
    p_x = []
    p_y = []

    PICK_SIZE = int(N * percentil)
    r = START_R
    step = STEP
    while r < DIS_R:
        xs = calc_logistic_map_for_r(r)
        casted = list(np.array(xs).round(decimals=DECIMALS))[-PICK_SIZE:]


        picked = casted
        res[r] = picked
        x = [r] * len(picked) 
        y = picked
       

        p_x += list(x)
        p_y += list(y)

        r += step
    return (p_x, p_y), res


def get_linspace():
    LINSPACE_SIZE = 10000
    return np.linspace(x_0, 1, LINSPACE_SIZE)

def get_training_points(result):
    train_x = []
    train_y = []
 

    for r in np.linspace(START_TRAIN_R, END_TRAIN_R, 25):
        for times in range(TRAIN_SPACE_TIMES):
            for x in np.linspace(x_0, 1, 100):
                train_x.append([r, x])
                x_1 = logistic_map(x, r)
                train_y.append(x_1)

    # for r in result.keys():
    #     sequence = list(result[r])

    #     for i in range(len(sequence)-1):
    #         x_0 = sequence[i]
    #         x_1 = sequence[i+1]

    #         train_x.append([r, x_0])
    #         train_y.append(x_1)
    

    train_x = np.array(train_x)
    train_y = np.array(train_y)
    print(f'Generated training points')
    return np.array(train_x), np.array(train_y)


def get_net_points(result):
    p_x = []
    p_y = []


    #Train model
    train_x, train_y = get_training_points(result)

    print(f'Size of train X {train_x.shape}')
    print(f'Size of train Y {train_y.shape}')



    #Model construction
    model = Sequential()
    model.add(Input(shape=(2)))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])


    #Learn model
    EPOCHS = 100

    model.fit(
        train_x, 
        train_y,     
        epochs=EPOCHS,
        shuffle=True,
        #batch_size=BATCH_SIZE
    )

    #Predict points
    from_r = N_START_R
    to_r = N_DIS_R

    for r in np.arange(from_r, to_r, STEP):
        x = x_0
        # print('Start test')
        for test_i in range(200):
            inp = np.array([[r, x]])
            x = model.predict(inp).flatten()[0]

        # print('End test')
        # PICK_SIZE = int(N * percentil)
        PICK_SIZE = 50
        for real_i in range(PICK_SIZE):
            inp = np.array([[r, x]])
            x = model.predict(inp).flatten()[0]
            p_x.append(r)
            p_y.append(x)
    
    print('Generated')
    #Return points
    return p_x, p_y


def calc_logistic_map_for_r(r):
    xs = []
    x = x_0
    for _ in range(N):
        x = logistic_map(x, r)
        xs.append(x)
    return xs


def cv10():
   
    ##No net##
    no_net_points, res = get_non_net_points()
    n_x, n_y = no_net_points


    ##NET!##
    net_x, net_y = get_net_points(res)

    fig, axs = plt.subplots(2)
    fig.suptitle('Logistic map')
    fig.set_size_inches(15, 10)


    for ax in axs.flat:
        ax.set(xlabel='r', ylabel='x')

    axs[0].set_title('No net :-(')
    axs[0].grid()
    axs[0].set_xlim(0, 4)
    axs[0].scatter(n_x, n_y, c='gray', s=1)



    axs[1].set_title('Future net :-)')
    axs[1].grid()
    axs[1].set_xlim(0, 4)
    axs[1].scatter(net_x, net_y, c='red', s=1)



    #PLOT


    plt.show()