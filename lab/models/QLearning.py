import numpy as np
from lab.cv4.CONSTANTS import NOT_ALLOWED, EPOCHS
import pandas as pd
import random
from lab.cv4.game.RectState import RectState


QLearningDebug = False


class QLearning():
    def __init__(self, learning_rate, epochs=EPOCHS):
        self.env_matrix = None
        self.env = []
        self.Q = []
        self.generation = 0
        self.prob = 1
        self.learning_rate = learning_rate
        self.position = 0
        self.max_generation = epochs
        self.not_allowed_start = []

    def predict(self):
        print('predict')

    def fit(self):
        print('fit')

    def move(self):
        current_room = self.env[self.position]

        def check_condition(x):
            return x != NOT_ALLOWED
        
        possible_actions = np.argwhere(check_condition(current_room)).flatten()
        action = random.choice(possible_actions)


        next_state_room = self.env[action]
        next_state_all_actions = np.argwhere(check_condition(next_state_room)).flatten()

        next_state_Qs = np.array([self.Q[action][next_state_action] for next_state_action in next_state_all_actions])
        maximum = np.max(next_state_Qs)


        if QLearningDebug:
            print('currentRoom\n', current_room)
            print('currentAction\n', action)

            print('\n')
            print('nextRoom\n', next_state_room)
            print('nextActions\n', next_state_all_actions)

            print('\n')
            print('nextStateQs\n', next_state_Qs)
            print('maximum\n', maximum)


        update = self.env[self.position][action] + self.learning_rate * maximum

        if QLearningDebug:
            print('update\n', update)

        self.Q[self.position][action] = update
        
        if QLearningDebug:
            print('cheese?\n', self.env[self.position][action])

        if self.env[self.position][action] == RectState.CHEESE.value:
            return True

        self.position = action
        return False

    def run_epochs(self):
        while self.generation < self.max_generation:
            print(f'Epoch {self.generation}')
            self.epoch()
        print('Finished all epochs')

    def epoch(self):
        verticies = list(range(len(self.env)))
        options = list(filter(lambda v: v not in self.not_allowed_start, verticies))
        self.position = random.choice(options)
        while not self.move():
            # print('moving')
            pass
        self.generation += 1
        self.prob = 1 / self.generation

    def create_env(self):
        if self.env_matrix is None:
            raise ValueError('Env matrix is NONE!')
        #y, x
        movement = [
            (1, 0), #top
            (0, 1), #right
            (-1, 0), #bottom
            (0, -1), #left
        ]

        def check_fn(matrix):
            return (matrix == RectState.CHEESE.value) | (matrix == RectState.WALL.value)


        size = len(self.env_matrix)
        graph_size = size**2
        blacklist = np.argwhere(check_fn(self.env_matrix))
        self.not_allowed_start = [item[0] * size + item[1] for item in blacklist]
        self.Q = np.zeros(shape=(graph_size, graph_size))
        self.env = np.zeros(shape=(graph_size, graph_size))
        self.env.fill(NOT_ALLOWED)

        for y in range(size):
            for x in range(size):
                vertex_id = y * size + x
                for _y, _x in movement:
                    edge_y = y + _y  
                    edge_x = x + _x
                    in_env = (edge_y >= 0 and edge_y < size) and (edge_x >= 0 and edge_x < size)
                    if not in_env:
                        continue
                    _vertex_id = edge_y * size + edge_x

                    self.env[vertex_id][_vertex_id] = self.env_matrix[edge_y][edge_x]



        self.run_epochs()

        # if QLearningDebug:
        print(pd.DataFrame(self.Q))
        
        # print(pd.DataFrame(self.env))
        print('Creating ENV')




