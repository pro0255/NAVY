from lab.cv9.CONSTANTS import ITERATIONS, FROM, TO, INIT_HEIGHT, initial_displacement, roughness
import matplotlib.pyplot as plt
import numpy as np





def generate_new(left, right, displacement):
    middle_x = (left[0] + right[0]) / 2
    middle_y = (left[1] + right[1]) / 2
    change = np.random.uniform(-1, 1) * displacement
    middle_y += change

    return (middle_x, middle_y)


    

def merge(old, new):
    merged = []
    old_c = 0
    new_c = 0
    for i in range(len(old) + len(new)):
        if i % 2 == 0:
            merged.append(old[old_c])
            old_c += 1
        else:
            merged.append(new[new_c])
            new_c += 1
    return list(zip(*merged))

def iterate(x, y, displacement):
    new = [] 
    for i in range(len(x) - 1):
        left = (x[i], y[i])
        right = (x[i+1], y[i+1])
        new.append(generate_new(left, right, displacement))


    old = list(zip(x, y))
    return merge(old, new)


def cv9():
    init_x = [FROM, TO]
    init_y = [INIT_HEIGHT, INIT_HEIGHT]

    x = init_x
    y = init_y

    displacement = initial_displacement

    for i in range(ITERATIONS):
        print(f'Iteration {i}')
        x, y = iterate(x, y, displacement)
        displacement = displacement * roughness

    plt.plot(x, y, color='black', lw=0.2)
    plt.fill_between(x, y, facecolor='blue', alpha=1)
    plt.show()

