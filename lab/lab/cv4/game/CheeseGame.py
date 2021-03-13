import os
import pygame
from pygame.locals import *
from lab.cv4.game.utils import Utils
from lab.cv4.game.GameState import GameState
from lab.cv4.game.RectState import RectState
from lab.cv4.game.board import Board
from models.QLearning import QLearning
from lab.cv4.CONSTANTS import BLACK_COLOR, YELLOW_COLOR, PINK_COLOR, LEARNING_RATE
import numpy as np
import pandas as pd

W_W = 500
SELECT_BAR = 200
EXTRA = 100
W_H = W_W + EXTRA + SELECT_BAR
BUTTON_HEIGHT = 50
debug = False


def from_dic_matrix(dic, n):
    matrix = np.zeros(shape=(n, n))
    for k, v in dic.items():
        matrix[k[0]][k[1]] = v.value
    return matrix


class CheeseGame:
    def __init__(self, N):
        # screen dimensions
        screen_width = W_W
        screen_height = W_H
        # flag to know if game menu has been showed
        self.state = GameState.ENV
        self.n = N
        # flag to set game loop
        self.running = True
        # initialize game window
        pygame.display.init()
        # initialize font for text
        pygame.font.init()
        # create game window
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        # title of window
        window_title = "Cheese game"
        # set window caption
        pygame.display.set_caption(window_title)
        # update display
        pygame.display.flip()
        self.Qlearn = QLearning(LEARNING_RATE)
        # set game clock
        self.clock = pygame.time.Clock()


    def start_game(self):
        """Function containing main game loop""" 
        # chess board offset
        self.board_offset_x = 0
        self.board_offset_y = (EXTRA / 2)/2 
        self.board_dimensions = (self.board_offset_x, self.board_offset_y)

        # get the width of a chess board square
        square_length = W_W / self.n

        # initialize list that stores all places to put chess pieces on the board
        self.board_locations = []

        # calculate coordinates of the each square on the board
        for x in range(0, self.n):
            self.board_locations.append([])
            for y in range(0, self.n):
                self.board_locations[x].append([self.board_offset_x+(x*square_length), 
                                                self.board_offset_y+(y*square_length)])

        self.board = Board(self.screen, self.board_locations, square_length, self.n)

        # game loop
        while self.running:
            self.clock.tick(15)
            # poll events
            for event in pygame.event.get():
                # get keys pressed
                key_pressed = pygame.key.get_pressed()
                # check if the game has been closed by the user
                if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                    # set flag to break out of the game loop
                    self.running = False
            

            if self.state == GameState.MENU:
                self.menu()
                if debug:
                    print('menu')
            elif self.state == GameState.ENV:
                self.save()
                if debug:
                    print('save')
            else:
                self.recover()
                if debug:
                    print('recover')
            

            # update display
            pygame.display.flip()
            # update events
            pygame.event.pump()

        # call method to stop pygame
        pygame.quit()



    def select_bar(self):
        white_color = (255, 255, 255)

        #left, top, width, height

        size_of_button = int(W_W / 3)
        gap = 20

        wall_btn = pygame.Rect(size_of_button*0, W_H - (BUTTON_HEIGHT*2) - gap, size_of_button, BUTTON_HEIGHT)
        cheese_btn = pygame.Rect(size_of_button*1, W_H - (BUTTON_HEIGHT*2) - gap, size_of_button, BUTTON_HEIGHT)
        trap_btn = pygame.Rect(size_of_button*2, W_H - (BUTTON_HEIGHT*2) - gap, size_of_button, BUTTON_HEIGHT)


        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        wall_btn_label = small_font.render("Wall", True, white_color)        
        cheese_btn_label = small_font.render("Cheese", True, white_color)        
        trap_btn_label = small_font.render("Trap", True, white_color)      

        pygame.draw.rect(self.screen, BLACK_COLOR, wall_btn)
        pygame.draw.rect(self.screen, YELLOW_COLOR, cheese_btn)  
        pygame.draw.rect(self.screen, PINK_COLOR, trap_btn)  


        self.screen.blit(wall_btn_label, 
                      ((wall_btn.x + (wall_btn.width - wall_btn_label.get_width()) // 2, 
                      wall_btn.y + (wall_btn.height - wall_btn_label.get_height()) // 2)))
        self.screen.blit(cheese_btn_label, 
            ((cheese_btn.x + (cheese_btn.width - cheese_btn_label.get_width()) // 2, 
            cheese_btn.y + (cheese_btn.height - cheese_btn_label.get_height()) // 2)))
        self.screen.blit(trap_btn_label, 
            ((trap_btn.x + (trap_btn.width - trap_btn_label.get_width()) // 2, 
            trap_btn.y + (trap_btn.height - trap_btn_label.get_height()) // 2)))


        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()


        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if "Play" button was clicked
            if wall_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, wall_btn, 3)
                self.board.rect_state = RectState.WALL

            if cheese_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, cheese_btn, 3)
                self.board.rect_state = RectState.CHEESE
            if trap_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, trap_btn, 3)
                self.board.rect_state = RectState.TRAP


            elif key_pressed[K_ESCAPE]:
                self.state = GameState.MENU




    def menu(self):
        """method to show game menu"""
        # background color
        bg_color = (255, 255, 255)
        # set background color
        self.screen.fill(bg_color)
        # black color
        black_color = (0, 0, 0)
        # coordinates for "Play" button


        # save, recover
        save_btn = pygame.Rect(0, 300, W_W, 50)

        gap = 20

        recover_btn = pygame.Rect(0, 350 + gap, W_W, 50)
        
        # show play button
        pygame.draw.rect(self.screen, black_color, save_btn)

        pygame.draw.rect(self.screen, black_color, recover_btn)

        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        welcome_text = big_font.render("Cheese game :=]", False, black_color)
        created_by = small_font.render("Created by Vojtech Prokop", True, black_color)

        save_btn_label = small_font.render("Create ENV", True, white_color)
        recover_btn_label = small_font.render("Learn", True, white_color)
        
        # show welcome text
        self.screen.blit(welcome_text, 
                      ((self.screen.get_width() - welcome_text.get_width()) // 2, 
                      150))
        # show credit text
        self.screen.blit(created_by, 
                      ((self.screen.get_width() - created_by.get_width()) // 2, 
                      self.screen.get_height() - created_by.get_height() - 100))
        # show text on the Play button
        self.screen.blit(save_btn_label, 
                      ((save_btn.x + (save_btn.width - save_btn_label.get_width()) // 2, 
                      save_btn.y + (save_btn.height - save_btn_label.get_height()) // 2)))

        self.screen.blit(recover_btn_label, 
                      ((recover_btn.x + (save_btn.width - recover_btn_label.get_width()) // 2, 
                      recover_btn.y + (save_btn.height - recover_btn_label.get_height()) // 2)))



        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()

        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if "Play" button was clicked
            if save_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, save_btn, 3)
                # change menu flag
                self.state = GameState.ENV

            # check if enter or return key was pressed
            if recover_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, recover_btn, 3)
                # change menu flag
                self.state = GameState.LEARNING


            elif key_pressed[K_RETURN]:
                self.state = GameState.MENU

    def save(self):
        black_color = (0, 0, 0)
        color = (0,255,0)
        self.screen.fill(color)

        gap = 10
        btn_h = BUTTON_HEIGHT
        save_btn = pygame.Rect(0, W_H - btn_h, W_W / 2 - (gap / 2), btn_h)
        back_btn = pygame.Rect(W_W / 2 + (gap / 2), W_H - btn_h, W_W / 2, btn_h)
        pygame.draw.rect(self.screen, black_color, save_btn)
        pygame.draw.rect(self.screen, black_color, back_btn)
        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        save_btn_label = small_font.render("Save", True, white_color)        
        back_btn_label = small_font.render("Back", True, white_color)        
        # show text on the Play button
        self.screen.blit(save_btn_label, 
                      ((save_btn.x + (save_btn.width - save_btn_label.get_width()) // 2, 
                      save_btn.y + (save_btn.height - save_btn_label.get_height()) // 2)))
        self.screen.blit(back_btn_label, 
                      ((back_btn.x + (back_btn.width - back_btn_label.get_width()) // 2, 
                      back_btn.y + (back_btn.height - back_btn_label.get_height()) // 2)))

        self.board.draw_board()
        self.select_bar()

        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()

        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if "Play" button was clicked
            if save_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, save_btn, 3)
                # change menu flag
                matrix = from_dic_matrix(self.board.mem, self.n)
                self.Qlearn.env_matrix = matrix
                print('Created Env Matrix: \n', pd.DataFrame(matrix))
                print('\n')
                self.Qlearn.create_env()

            if back_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                self.state = GameState.MENU


            elif key_pressed[K_ESCAPE]:
                self.state = GameState.MENU

        if debug:
            print('save')


    def recover(self):
        black_color = (0, 0, 0)
        color = (0,255,0)
        self.screen.fill(color)
        btn_h = 50
        gap = 10
        h_gap = 10
        sync_btn = pygame.Rect(0, W_H - btn_h - h_gap, W_W / 2 - (gap / 2), btn_h / 2)
        async_btn = pygame.Rect(W_W / 2 + (gap / 2), W_H - btn_h - h_gap, W_W / 2, btn_h / 2)
        
        back_btn = pygame.Rect(0, W_H - (btn_h / 2), W_W / 2 - (gap / 2), btn_h / 2)
        reset_btn = pygame.Rect(W_W / 2 + (gap / 2), W_H - (btn_h / 2), W_W / 2, btn_h / 2)

        # show play button
        pygame.draw.rect(self.screen, black_color, sync_btn)
        pygame.draw.rect(self.screen, black_color, async_btn)
        pygame.draw.rect(self.screen, black_color, back_btn)
        pygame.draw.rect(self.screen, black_color, reset_btn)
        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        sync_btn_label = small_font.render("Sync", True, white_color)        
        async_btn_label = small_font.render("Async", True, white_color)        
        back_btn_label = small_font.render("Back", True, white_color)        
        reset_btn_label = small_font.render("Reset", True, white_color)        
        # show text on the Play button
        self.screen.blit(sync_btn_label, 
                      ((sync_btn.x + (sync_btn.width - sync_btn_label.get_width()) // 2, 
                      sync_btn.y + (sync_btn.height - sync_btn_label.get_height()) // 2)))
                      
        self.screen.blit(async_btn_label, 
                      ((async_btn.x + (async_btn.width - async_btn_label.get_width()) // 2, 
                      async_btn.y + (async_btn.height - async_btn_label.get_height()) // 2)))
        self.screen.blit(back_btn_label, 
                      ((back_btn.x + (back_btn.width - back_btn_label.get_width()) // 2, 
                      back_btn.y + (back_btn.height - back_btn_label.get_height()) // 2)))
                      
        self.screen.blit(reset_btn_label, 
                      ((reset_btn.x + (reset_btn.width - reset_btn_label.get_width()) // 2, 
                      reset_btn.y + (reset_btn.height - reset_btn_label.get_height()) // 2)))

        self.board.draw_board()
        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()

        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if "Play" button was clicked
            if sync_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, sync_btn, 3)
                # change menu flag
                matrix = from_dic_matrix(self.board.mem, self.n)
                recovered = self.net.recover_sync(matrix)
                r_dic = {(y,x): True if value == 1 else False for y, row in enumerate(recovered) for x, value in enumerate(row)}
                self.board.mem = r_dic

            if back_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                self.state = GameState.MENU

            if reset_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                self.board.reset()

            if async_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, async_btn, 3)
                # change menu flag
                matrix = from_dic_matrix(self.board.mem, self.n)
                recovered = self.net.recover_async(matrix)

                r_dic = {(y,x): True if value == 1 else False for y, row in enumerate(recovered) for x, value in enumerate(row)}
                self.board.mem = r_dic
            

            elif key_pressed[K_ESCAPE]:
                self.state = GameState.MENU


        if debug:
            print('recover')
