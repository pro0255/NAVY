import numpy as np
from lab.cv3.CONSTANTS import pattern8, pattern8_destroyed
from lab.cv3.utils.from_pattern2matrix import from_pattern2matrix 
from models.HopfieldNet import HopfieldNet


def cv3():
    net = HopfieldNet()
    net.save_pattern(pattern8)
    result_sync = net.recover_sync(np.copy(pattern8_destroyed))
    result_async = net.recover_async(np.copy(pattern8_destroyed))
    print('Dest\n', pattern8_destroyed)
    print('Sync\n', result_sync)
    print('Async\n', result_async)