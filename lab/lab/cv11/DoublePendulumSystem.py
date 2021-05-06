
from lab.cv11.CONSTANTS import m1, m2, l1, l2, g, f, to, dt
from scipy.integrate import odeint
import numpy as np
import math



def get_derivative(y, t):
    theta1, z1, theta2, z2 = y

    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

    theta1dot = z1
    z1dot = (m2*g*np.sin(theta2)*c - m2*s*(l1*z1**2*c + l2*z2**2) -
             (m1+m2)*g*np.sin(theta1)) / (l1  * (m1 + m2*s**2))

    theta2dot = z2

    ##CHYBA?
    z2dot = ((m1+m2)*(l1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + 
             m2*l2*z2**2*s*c) / (l2 *(m1 + m2*s**2))

    return theta1dot, z1dot, theta2dot, z2dot


class DoublePendulumSystem:
    def __init__(self, theta1, angle_velocity1, theta2, angle_velocity2):
        self.state0 = (theta1, angle_velocity1, theta2, angle_velocity2)

    def next_states(self):
        t = np.arange(f, to, dt)
        self.states = odeint(get_derivative, self.state0, t)

    def get_circle_positions(self):
        positions = []
        for state in self.states:
            positions.append(self.get_position(state))
        return positions

    def get_position(self, state):
        theta1, _, theta2, _ = state
        x1 = l1 * math.sin(theta1)
        y1 = -l1 * math.cos(theta1)
        x2 =  l1*math.sin(theta1) + l2*math.sin(theta2)
        y2 = -l1*math.cos(theta1) - l2*math.cos(theta2)
        return ((x1,y1), (x2,y2))