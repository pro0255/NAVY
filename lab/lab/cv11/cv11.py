from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from lab.cv11.DoublePendulumSystem import get_derivative
from lab.cv11.DoublePendulumSystem import DoublePendulumSystem
from lab.cv11.CONSTANTS import init_theta1, init_theta2, init_angle_velocity1,init_angle_velocity2, dt


def cv11():

    sys = DoublePendulumSystem(init_theta1, init_angle_velocity1, init_theta2, init_angle_velocity2)
    sys.next_states()
    positions = sys.get_circle_positions() 

    fig = plt.figure()
    
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
    ax.set_title('Double Pendulum')
    ax.set_aspect('equal')

    line, = ax.plot([], [], 'o-', lw=3, c='green')

    def init():
        line.set_data([], [])
        return line


    def animate(i):
        state = positions[i]
        pen1, pen2 = state
        x1,y1 = pen1 
        x2,y2 = pen2 

        thisx = [0, x1, x2]
        thisy = [0, y1, y2]

        line.set_data(thisx, thisy)
        return line


    ani = animation.FuncAnimation(fig, animate, range(0, len(positions)), interval=20, init_func=init)
    plt.show()



