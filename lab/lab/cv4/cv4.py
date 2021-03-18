from lab.cv4.game.CheeseGame import CheeseGame
from lab.cv4.CONSTANTS import SIZE_OF_GAME


def cv4():
    g = CheeseGame(SIZE_OF_GAME)
    g.start_game()
