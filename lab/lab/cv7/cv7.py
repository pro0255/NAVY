import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from lab.cv7.IFS import IFS
from lab.cv7.CONSTANTS import GEN, COLOR, p, SIZE
import pandas as pd


def visualize(x, y, z):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(15, 6))
    surf = ax.scatter(x, y, z, linewidth=0, antialiased=False, c=COLOR, s=SIZE)
    plt.show()


def cv7():
    model1 = pd.read_csv(f'./lab/cv7/models/model1.csv',sep=';')
    model2 = pd.read_csv(f'./lab/cv7/models/model2.csv',sep=';')
    ifs = IFS(model2, p)
    res = ifs.process(GEN)
    visualize(*res)
