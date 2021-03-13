from enum import Enum
from lab.cv4.CONSTANTS import NOT_ALLOWED, TRAP, CHEESE

class RectState(Enum):
    WALL = NOT_ALLOWED
    CHEESE = CHEESE
    TRAP = TRAP
    EMPTY = 0
