from lab.cv6.LSystem import LSystem
from lab.cv6.CONSTANTS import first, second, third, fourth


def run(tup, num):
    s = LSystem(*tup, num)
    s.draw()


def cv6():
    # run(first,2)
    # run(second,2)
    run(third, 1)
    # run(fourth,2)


    # print('cv6')