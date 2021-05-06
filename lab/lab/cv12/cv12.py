import numpy as np
from lab.cv12.CONSTANTS import f, p, size, frames, interval, EMPTY, TREE, FIRE
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import animation




def init_map():
    """Generates init map
    """
    m = np.zeros(shape=(size, size))
    return m

def populate_map(m):
    """Populates map with random init state
    """
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            states = list(range(EMPTY, FIRE))
            tree_state = random.choice(states)
            m[y, x] = tree_state
    return m

def return_cell_state(y,x,m):
    """Return new state of cell according to old map and config of probs
    """
    #y, x
    movement = [
        [1, 0], #nahoru
        [1, 1], #nohoru diagonala
        [0, 1], #doprava
        [-1, 1], #doprava diagonala
        [-1, 0], #dolu
        [-1, -1], #doleva diagonala
        [0, -1], #doleva
        [1, -1], #diagonala
    ]

    current_cell_state = m[y, x]
    """
        A burning cell turns into an empty cell
        A cell occupied by a tree becomes a burning cell if any of its eight neighbouring cells are burning
        A cell occupied by a tree becomes burning with a probabilty f (even if none of its neighbouring cells are burning), as though struck by lightning
        An empty cell becomes occupied by a tree with probability p.
    """

    if current_cell_state == FIRE:
        # print('Turning empty')
        #A burning cell turns into an empty cell
        return EMPTY

    if current_cell_state == EMPTY:
        #An empty cell becomes occupied by a tree with probability p.
        r = random.uniform(0, 1)
        if r < p:
            # print('Happy little tree')
            return TREE

    if current_cell_state == TREE:
        surr_fire = False
        for move in movement:
            _y, _x = move
            new_y = y + _y
            new_x = x + _x
            if new_y >= 0 and new_y < size and new_x >=0 and new_x < size:
                if m[new_y, new_x] == FIRE:
                    return FIRE

        r = random.uniform(0, 1)
        if r < f:
            return FIRE

    return current_cell_state


def new_map_state(old_map):
    """Generates new map according to state of old map and specified rules
    """
    new_map = np.zeros(shape=(size, size))
    # print(pd.DataFrame(old_map))
    for y in range(new_map.shape[0]):
        for x in range(new_map.shape[1]):
           new_map[y, x] = return_cell_state(y, x, old_map)
    return new_map


def cv12():
    colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange']
    cmap = colors.ListedColormap(colors_list)
    bounds = [EMPTY, TREE, FIRE,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)








    m = init_map()
    m = populate_map(m)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.set_title('The Forest-fire model')
    ax.set_axis_off()
    plt_m = ax.imshow(m, cmap=cmap, norm=norm)

    def animate(i):
        plt_m.set_data(animate.m)
        animate.m = new_map_state(animate.m)

    animate.m = m
    
    anim = animation.FuncAnimation(fig, animate, interval=interval, frames=frames)
    plt.show()
