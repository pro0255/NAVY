import pygame
from pygame.locals import *
import random
from lab.cv3.game.utils import Utils
import time


WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

class Board():
    def __init__(self, screen, square_coords, square_length, n):
        self.screen = screen
        self.board_locations = square_coords
        self.square_length = int(square_length)
        self.n = n
        self.utils = Utils()
        self.mem = {(y, x): False for y in range(self.n) for x in range(self.n)}
        # self.reset()
   
    def reset(self):
        self.mem = {(y, x): False for y in range(self.n) for x in range(self.n)}


    # method to draw pieces on the chess board
    def draw_board(self):
        for rowI, row in enumerate(self.board_locations):
            for colI, col in enumerate(row):
                value = self.mem[(colI, rowI)]
                x, y = col
                box = pygame.Rect(x, y, self.square_length, self.square_length)
                pygame.draw.rect(self.screen, WHITE if not value else BLACK, box)
                # pygame.Surface.blit(self.screen, , box)


        
        util = Utils()
        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()
            column = mouse_coords[0] // (self.square_length)
            row = mouse_coords[1] // (self.square_length)
            if (row, column) in self.mem:
                self.mem[(row, column)] = not self.mem[(row, column)] 


