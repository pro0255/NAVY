import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from lab.cv7.IFS import IFS
from lab.cv7.CONSTANTS import GEN, COLOR


def visualize(x, y, z):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.scatter(x, y, z, linewidth=0, antialiased=False, c=COLOR)
    plt.show()


def cv7():
    ifs = IFS()
    res = ifs.process(GEN)
    visualize(*res)
