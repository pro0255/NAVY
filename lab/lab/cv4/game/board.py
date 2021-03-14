import pygame
from pygame.locals import *
import random
from lab.cv3.game.utils import Utils
import time
from lab.cv4.game.RectState import RectState
from lab.cv4.CONSTANTS import YELLOW_COLOR, BLACK_COLOR, PINK_COLOR, WHITE_COLOR
from lab.cv4.game.DEFAULT_MATRIX import DEFAULT_MATRIX


class Board():
    def __init__(self, screen, square_coords, square_length, n):
        self.screen = screen
        self.board_locations = square_coords
        self.square_length = int(square_length)
        self.n = n
        self.utils = Utils()
        self.mem = {(y, x): RectState.EMPTY for y in range(self.n) for x in range(self.n)}
        self.rect_state =  RectState.TRAP
        self.set_default()
        # self.reset()
   
    def set_default(self):
        size = len(DEFAULT_MATRIX)
        if self.n != size:
            raise ValueError('Not same size!')
        self.mem = {(y, x): DEFAULT_MATRIX[y][x] for y in range(size) for x in range(size)}


    def reset(self):
        self.mem = {(y, x): RectState.EMPTY for y in range(self.n) for x in range(self.n)}

    # method to draw pieces on the chess board
    def draw_board(self, allow_click=True):
        for rowI, row in enumerate(self.board_locations):
            for colI, col in enumerate(row):
                value = self.mem[(colI, rowI)]
                x, y = col
                box = pygame.Rect(x, y, self.square_length, self.square_length)
                color = WHITE_COLOR
                if value == RectState.CHEESE:
                    color = YELLOW_COLOR
                if value == RectState.TRAP:
                    color = PINK_COLOR
                if value == RectState.WALL:
                    color = BLACK_COLOR
                pygame.draw.rect(self.screen, color, box)

        if allow_click:
            util = Utils()
            # check if left mouse button was clicked
            if util.left_click_event():
                # call function to get mouse event
                mouse_coords = util.get_mouse_event()
                column = mouse_coords[0] // (self.square_length)
                row = mouse_coords[1] // (self.square_length)
                if (row, column) in self.mem:
                    self.mem[(row, column)] = self.rect_state


