import numpy as np
import math
from sklearn.preprocessing import KBinsDiscretizer
import pandas as pd
from lab.cv5.CONSTANTS import DISCOUNT_FACTOR, LEARNING_RATE, CONSTANT_LR



class QAgent:
    def __init__(self, max_generation, learning_rate, buckets):
        self.Q = np.zeros(buckets + (2, )) #number of actions
        self.generation = 0
        self.max_generation = max_generation
        self.learning_rate = self.l_r(0) #
        self.buckets = buckets
        self.prob = 1
    
    def l_r(self, epoch):
        l = LEARNING_RATE if CONSTANT_LR else max(LEARNING_RATE, min(0.5, 1.0 - math.log10((epoch+1)/25)))
        return l


    def map_state(self, env, state):
        mapped_state = []
        lower_bounds = []
        upper_bounds = []

        l_h_tuples = list(zip(env.observation_space.low, env.observation_space.high))
        for t in l_h_tuples:
            lower_bounds.append(t[0])
            upper_bounds.append(t[1])


        #prepis
        #velocity
        # lower_bounds[1] = -.5
        # upper_bounds[1] = .5

        #angular velocity
        
        lower_bounds[3] = -math.radians(50)
        upper_bounds[3] = math.radians(50)


        ##1
        # for i in range(len(state)):
        #     #keep the state between the bounds
        #     state_value = state[i] 
        #     if state_value <= lower_bounds[i]:
        #         bucket_index = 0 
        #     elif state_value >= upper_bounds[i]:
        #         bucket_index = self.buckets[i] - 1
        #     else:
        #         bound_width =  upper_bounds[i] - lower_bounds[i]

        #         offset = (self.buckets[i] - 1) * lower_bounds[i] / bound_width
        #         scaling = (self.buckets[i] - 1) / bound_width

        #         bucket_index = int(round(scaling * state[i] - offset))
            
        #     mapped_state.append(bucket_index)
        

        ##2
        # for index, state_value in enumerate(state):
        #     low, high = l_h_tuples[index]
        #     number_of_buckets = self.buckets[index]
        #     res = np.linspace(low, high, number_of_buckets + 1)

        #     for index in range(1, len(res)):
        #         value = res[index]
        #         if state_value <= value:
        #             mapped_state.append(index - 1)
        #             break


        ##3
        # est = KBinsDiscretizer(n_bins=self.buckets, encode='ordinal', strategy='uniform')
        # est.fit([lower_bounds, upper_bounds ])
        # mapped_state = list(map(int,est.transform([state])[0]))



        #4
        for i in range(len(state)):
            current_state = state[i]
            current_bucket = self.buckets[i]
            current_upper_b = upper_bounds[i]
            current_lower_b = lower_bounds[i]
            scaling = (current_state + abs(current_lower_b)) / (current_upper_b - current_lower_b)
            new_state = int(round((current_bucket - 1) * scaling))
            new_state = min(current_bucket - 1, max(0, new_state)) #bounderies
            mapped_state.append(new_state)           

        return mapped_state


    def update_prob(self):
        self.prob = (self.max_generation - self.generation) / self.max_generation
        self.generation += 1


    def get_action(self, env, state, test):
        r = np.random.uniform()

        is_random = r <= self.prob

        if test:
            is_random = False

        action = None
        if is_random:
            action = env.action_space.sample()
        else:
            action = np.argmax(self.Q[tuple(state)])
        return action


    def update_Q(self, state, action, next_state, reward):
        max_value = np.max(self.Q[tuple(next_state)])
        update = self.learning_rate * (DISCOUNT_FACTOR * max_value + reward - self.Q[tuple(state)][action])
        self.Q[tuple(state)][action] += update
        #1-self.learning?


