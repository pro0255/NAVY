
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from lab.cv8.CONSTANTS import x_from, x_to, y_from, y_to, x_num, y_num, M, z_0, MAX

def mandelbrot(c, m=M):
    z = z_0
    i = 0
    while abs(z) <= m and i <= MAX :
        z = (z ** 2) + c
        i += 1
    return i



def create_empty():
    return np.zeros((x_num, y_num)) 


def make_fractal(x_f, x_t, y_f, y_t):
    real = np.linspace(x_f, x_t, num=x_num)
    imag = np.linspace(y_f, y_t, num=y_num)
    s_r = len(real)
    s_i = len(imag)
    data = create_empty()

    for x in range(s_r):
        for y in range(s_i):
            data[x, y] = mandelbrot(complex(real[x], imag[y]))

    return data

ZOOM = 0.1

def cv8():
    fig, ax = plt.subplots()
    data_init = create_empty()
    window = plt.imshow(data_init.T, interpolation="nearest", vmin=0, vmax=MAX)


    def init():
        data = make_fractal(x_from, x_to, y_from, y_to)
        window.set_data(data.T)


    def onscroll(event):
        global ZOOM
        global x_to
        global x_from
        global y_to
        global y_from

        print(ZOOM)
        if event.button == 'down' and ZOOM > 0:
            ZOOM -= 0.1

        if event.button == 'up' and ZOOM < 1:
            ZOOM += 0.1

        x_space = abs(x_to - x_from)
        y_space = abs(y_to - y_from)

        max_x_space = x_space  
        max_y_space = y_space

        zoomed_x_space = x_space * ZOOM
        zoomed_y_space = y_space * ZOOM

        diff_x  = max_x_space - zoomed_x_space
        diff_y = max_y_space - zoomed_y_space

        sub_x = diff_x / 2 
        sub_y = diff_y / 2


        x_t = x_to - sub_x
        x_f = x_from + sub_x
        y_t = y_to - sub_y
        y_f = y_from + sub_y

        data = make_fractal(x_f, x_t, y_f, y_t)

        print(data)


        window.set_data(data.T)

        plt.show()

    init()
    
    # cid = fig.canvas.mpl_connect('scroll_event', onscroll)
    plt.show()
