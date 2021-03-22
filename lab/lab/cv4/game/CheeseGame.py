import os
import pygame
from pygame.locals import *
from lab.cv4.game.utils import Utils
from lab.cv4.game.GameState import GameState
from lab.cv4.game.RectState import RectState
from lab.cv4.game.board import Board
from models.QLearning import QLearning
from lab.cv4.CONSTANTS import (
    BLACK_COLOR,
    YELLOW_COLOR,
    PINK_COLOR,
    LEARNING_RATE,
    GREEN_COLOR,
    MOUSE_NAME,
    FAST_LEARN,
    TESTING_FRAMES,
    PREDICT_FRAMES,
)
import numpy as np
import pandas as pd

W_W = 600
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
        self.learning = False
        self.prediction = False

        self.mouse = pygame.image.load(f".//lab//cv4//game//images//animal.png")
        self.trap = pygame.image.load(f".//lab//cv4//game//images//trap.png")
        self.grass = pygame.image.load(f".//lab//cv4//game//images//grass.jpg")
        self.cheese = pygame.image.load(f".//lab//cv4//game//images//cheese.png")
        self.wall = pygame.image.load(f".//lab//cv4//game//images//wall.jpg")

        self.square_length = 0

    def start_game(self):
        """Function containing main game loop"""
        # chess board offset
        self.board_offset_x = 0
        self.board_offset_y = (EXTRA / 2) / 2
        self.board_dimensions = (self.board_offset_x, self.board_offset_y)

        # get the width of a chess board square
        self.square_length = int(W_W / self.n)
        self.mouse = pygame.transform.scale(
            self.mouse, (self.square_length, self.square_length)
        )
        self.trap = pygame.transform.scale(
            self.trap, (self.square_length, self.square_length)
        )
        self.grass = pygame.transform.scale(
            self.grass, (self.square_length, self.square_length)
        )
        self.cheese = pygame.transform.scale(
            self.cheese, (self.square_length, self.square_length)
        )
        self.wall = pygame.transform.scale(
            self.wall, (self.square_length, self.square_length)
        )

        # initialize list that stores all places to put chess pieces on the board
        self.board_locations = []

        # calculate coordinates of the each square on the board
        for x in range(0, self.n):
            self.board_locations.append([])
            for y in range(0, self.n):
                self.board_locations[x].append(
                    [
                        self.board_offset_x + (x * self.square_length),
                        self.board_offset_y + (y * self.square_length),
                    ]
                )

        self.board = Board(
            self.screen,
            self.board_locations,
            self.square_length,
            self.n,
            self.trap,
            self.grass,
            self.cheese,
            self.wall,
        )

        # game loop
        while self.running:
            self.clock.tick(TESTING_FRAMES if self.learning else PREDICT_FRAMES)
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
            elif self.state == GameState.ENV:
                self.save()
            elif self.state == GameState.LEARNING:
                self.learn()
            elif self.state == GameState.TESTING:
                self.predict()
            pygame.display.flip()
            pygame.event.pump()
        pygame.quit()

    def select_bar(self):
        white_color = (255, 255, 255)

        # left, top, width, height

        size_of_button = int(W_W / 3)
        gap = 20

        wall_btn = pygame.Rect(
            size_of_button * 0,
            W_H - (BUTTON_HEIGHT * 2) - gap,
            size_of_button,
            BUTTON_HEIGHT,
        )
        cheese_btn = pygame.Rect(
            size_of_button * 1,
            W_H - (BUTTON_HEIGHT * 2) - gap,
            size_of_button,
            BUTTON_HEIGHT,
        )
        trap_btn = pygame.Rect(
            size_of_button * 2,
            W_H - (BUTTON_HEIGHT * 2) - gap,
            size_of_button,
            BUTTON_HEIGHT,
        )

        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        wall_btn_label = small_font.render("Wall", True, white_color)
        cheese_btn_label = small_font.render("Cheese", True, white_color)
        trap_btn_label = small_font.render("Trap", True, white_color)

        pygame.draw.rect(self.screen, BLACK_COLOR, wall_btn)
        pygame.draw.rect(self.screen, YELLOW_COLOR, cheese_btn)
        pygame.draw.rect(self.screen, PINK_COLOR, trap_btn)

        self.screen.blit(
            wall_btn_label,
            (
                (
                    wall_btn.x + (wall_btn.width - wall_btn_label.get_width()) // 2,
                    wall_btn.y + (wall_btn.height - wall_btn_label.get_height()) // 2,
                )
            ),
        )
        self.screen.blit(
            cheese_btn_label,
            (
                (
                    cheese_btn.x
                    + (cheese_btn.width - cheese_btn_label.get_width()) // 2,
                    cheese_btn.y
                    + (cheese_btn.height - cheese_btn_label.get_height()) // 2,
                )
            ),
        )
        self.screen.blit(
            trap_btn_label,
            (
                (
                    trap_btn.x + (trap_btn.width - trap_btn_label.get_width()) // 2,
                    trap_btn.y + (trap_btn.height - trap_btn_label.get_height()) // 2,
                )
            ),
        )

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

        gap = 20

        save_btn = pygame.Rect(0, 300, W_W, 50)
        recover_btn = pygame.Rect(0, 350 + gap, W_W, 50)
        testing_btn = pygame.Rect(0, 400 + gap * 2, W_W, 50)

        # show play button
        pygame.draw.rect(self.screen, black_color, save_btn)
        pygame.draw.rect(self.screen, black_color, recover_btn)
        pygame.draw.rect(self.screen, black_color, testing_btn)

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
        testing_btn_label = small_font.render("Testing", True, white_color)

        # show welcome text
        self.screen.blit(
            welcome_text,
            ((self.screen.get_width() - welcome_text.get_width()) // 2, 150),
        )
        # show credit text
        self.screen.blit(
            created_by,
            (
                (self.screen.get_width() - created_by.get_width()) // 2,
                self.screen.get_height() - created_by.get_height() - 100,
            ),
        )
        # show text on the Play button
        self.screen.blit(
            save_btn_label,
            (
                (
                    save_btn.x + (save_btn.width - save_btn_label.get_width()) // 2,
                    save_btn.y + (save_btn.height - save_btn_label.get_height()) // 2,
                )
            ),
        )

        self.screen.blit(
            recover_btn_label,
            (
                (
                    recover_btn.x
                    + (save_btn.width - recover_btn_label.get_width()) // 2,
                    recover_btn.y
                    + (save_btn.height - recover_btn_label.get_height()) // 2,
                )
            ),
        )

        self.screen.blit(
            testing_btn_label,
            (
                (
                    testing_btn.x
                    + (testing_btn.width - testing_btn_label.get_width()) // 2,
                    testing_btn.y
                    + (testing_btn.height - testing_btn_label.get_height()) // 2,
                )
            ),
        )

        key_pressed = pygame.key.get_pressed()
        util = Utils()

        if util.left_click_event():
            mouse_coords = util.get_mouse_event()

            if save_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, save_btn, 3)
                self.state = GameState.ENV

            if recover_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, recover_btn, 3)
                self.state = GameState.LEARNING
                self.Qlearn.generation = 0

            if testing_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, testing_btn, 3)
                self.state = GameState.TESTING

            elif key_pressed[K_RETURN]:
                self.state = GameState.MENU

    def save(self):
        black_color = (0, 0, 0)
        color = (0, 255, 0)
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

        self.screen.blit(
            save_btn_label,
            (
                (
                    save_btn.x + (save_btn.width - save_btn_label.get_width()) // 2,
                    save_btn.y + (save_btn.height - save_btn_label.get_height()) // 2,
                )
            ),
        )
        self.screen.blit(
            back_btn_label,
            (
                (
                    back_btn.x + (back_btn.width - back_btn_label.get_width()) // 2,
                    back_btn.y + (back_btn.height - back_btn_label.get_height()) // 2,
                )
            ),
        )

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
                print("Created Env Matrix: \n", pd.DataFrame(matrix))
                print("\n")
                self.Qlearn.create_env(FAST_LEARN)

            if back_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                self.state = GameState.MENU

            elif key_pressed[K_ESCAPE]:
                self.state = GameState.MENU

        if debug:
            print("save")

    def predict(self):
        black_color = (0, 0, 0)
        color = (0, 255, 0)
        self.screen.fill(color)
        btn_h = 50
        gap = 10
        h_gap = 10
        start_btn = pygame.Rect(0, W_H - btn_h - h_gap, W_W, btn_h / 2)
        back_btn = pygame.Rect(0, W_H - (btn_h / 2), W_W, btn_h / 2)
        pygame.draw.rect(self.screen, black_color, start_btn)
        pygame.draw.rect(self.screen, black_color, back_btn)
        white_color = (255, 255, 255)
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        start_btn_label = small_font.render("Start Testing", True, white_color)
        back_btn_label = small_font.render("Back", True, white_color)

        self.screen.blit(
            start_btn_label,
            (
                (
                    start_btn.x + (start_btn.width - start_btn_label.get_width()) // 2,
                    start_btn.y
                    + (start_btn.height - start_btn_label.get_height()) // 2,
                )
            ),
        )

        self.screen.blit(
            back_btn_label,
            (
                (
                    back_btn.x + (back_btn.width - back_btn_label.get_width()) // 2,
                    back_btn.y + (back_btn.height - back_btn_label.get_height()) // 2,
                )
            ),
        )

        res = self.board.draw_board(False, True)
        if res is not None:
            self.Qlearn.position = res[0] * self.n + res[1]

        reminder = self.Qlearn.position % (self.n)
        row = int(self.Qlearn.position / self.n)

        box = pygame.Rect(
            reminder * self.square_length,
            self.board_offset_y + row * self.square_length,
            self.square_length,
            self.square_length,
        )
        # pygame.draw.rect(self.screen, GREEN_COLOR, box)
        # mouse_label = small_font.render(MOUSE_NAME, True, white_color)

        self.screen.blit(
            self.mouse,
            (
                (
                    box.x,
                    box.y,
                )
            ),
        )

        if self.prediction:

            if self.Qlearn.game_process(False):
                self.prediction = False

        key_pressed = pygame.key.get_pressed()
        util = Utils()
        if util.left_click_event():
            mouse_coords = util.get_mouse_event()
            if start_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, start_btn, 3)
                self.prediction = True

            if back_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                self.prediction = False
                self.state = GameState.MENU

            elif key_pressed[K_ESCAPE]:
                self.state = GameState.MENU

    def learn(self):
        black_color = (0, 0, 0)
        color = (0, 255, 0)
        self.screen.fill(color)
        btn_h = 50
        gap = 10
        h_gap = 10

        start_btn = pygame.Rect(0, W_H - btn_h - h_gap, W_W, btn_h / 2)
        back_btn = pygame.Rect(0, W_H - (btn_h / 2), W_W, btn_h / 2)

        # show play button
        pygame.draw.rect(self.screen, black_color, start_btn)
        pygame.draw.rect(self.screen, black_color, back_btn)

        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        start_btn_label = small_font.render("Start Learn", True, white_color)
        back_btn_label = small_font.render("Back", True, white_color)
        # show text on the Play button

        self.screen.blit(
            start_btn_label,
            (
                (
                    start_btn.x + (start_btn.width - start_btn_label.get_width()) // 2,
                    start_btn.y
                    + (start_btn.height - start_btn_label.get_height()) // 2,
                )
            ),
        )

        self.screen.blit(
            back_btn_label,
            (
                (
                    back_btn.x + (back_btn.width - back_btn_label.get_width()) // 2,
                    back_btn.y + (back_btn.height - back_btn_label.get_height()) // 2,
                )
            ),
        )

        self.board.draw_board(False)

        reminder = self.Qlearn.position % (self.n)
        row = int(self.Qlearn.position / self.n)
        box = pygame.Rect(
            reminder * self.square_length,
            self.board_offset_y + row * self.square_length,
            self.square_length,
            self.square_length,
        )

        self.screen.blit(
            self.mouse,
            (
                (
                    box.x,
                    box.y,
                )
            ),
        )

        if self.learning:
            self.Qlearn.game_process(True)
            # print('learning')

        # stop learning
        if self.Qlearn.generation == self.Qlearn.max_generation:
            self.learning = False

        key_pressed = pygame.key.get_pressed()
        util = Utils()

        if util.left_click_event():
            mouse_coords = util.get_mouse_event()

            if start_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, start_btn, 3)
                self.learning = True

            if back_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                self.state = GameState.MENU
                self.learning = False

            elif key_pressed[K_ESCAPE]:
                self.state = GameState.MENU

        if debug:
            print("learn")
