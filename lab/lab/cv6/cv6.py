from lab.cv6.LSystem import LSystem
from lab.cv6.CONSTANTS import first, second, third, fourth, fifth, sixth


def run(tup, num):
    s = LSystem(*tup, num)
    s.draw()




def cv6():
    # run(first, 1)
    # run(second, 2)
    # run(third, 4)
    # run(fourth, 4)
    # run(fifth, 4)
    run(sixth, 5)


    # print('cv6')