import gym
from lab.cv5.CONSTANTS import EPISODES, TIMESTAMPS, LEARNING_RATE, BUCKETS
from lab.cv5.QAgent import QAgent
import numpy as np
import matplotlib.pyplot as plt


VERBOSE_TIME = True
HISTORY = []
#https://gym.openai.com/docs/

def print_info(env, state, t, reward,  episode, agent, action):
    # print_info(env, next_mapped_state, t, reward, epoch_i, agent, action)

    print("\nepisode: %d" % episode)
    print("t: %d" % t)
    print("action: %d" % action)
    print("state: %s" % str(state))
    print("reward: %f" % reward)
    print("best Q: %f" % np.max(agent.Q))
    print(f"prob {agent.prob}")
    print("\n")

def cv5():
    env = gym.make('CartPole-v0')
    #position, velocity, angle, and angular velocity - observations
    agent = QAgent(EPISODES, LEARNING_RATE, BUCKETS)
    def run_condition(t, done, state, test, epoch, agent):
        run = True
        if done:
            run = False
            if VERBOSE_TIME:
                print(f'Ended in timestemp -> t={t}; e={epoch}; l={agent.learning_rate}')
        if t > TIMESTAMPS:
            print(test)
            if not test:

                if VERBOSE_TIME:
                    print(f'Ended in timestemp -> t={t}; e={epoch}; l={agent.learning_rate}')
                run = False
        return run


    epoch_i = 0
    HISTORY = []
    SAVED = False

    while True:
        state = env.reset()
        mapped_state = agent.map_state(env, state)
        done = False
        t = 0

        test = False
        if epoch_i > EPISODES:
            input_value = input('Wanna see learned agent? [y/n]\n')
            test = True if input_value == 'y' else False
            if not test:
                print('Ending program.. bye')
                if not SAVED:
                    X, y = zip(*HISTORY)
                    plt.clf()
                    plt.plot(X, y)
                    plt.title('pole balancing problem')
                    plt.xlabel('epoch index')
                    plt.ylabel('time')
                    plt.savefig(f'.//lab//cv5//graph2.png')
                    plt.show()
                    SAVED = True
                exit()


        while run_condition(t, done, state, test, epoch_i, agent):
            #Get actions deps on probability
            action = agent.get_action(env, mapped_state, test)
            #Moves in env
            next_state, reward, done, info = env.step(action)
            #State to buckets
            next_mapped_state = agent.map_state(env, next_state)
            #Update of Q matrix
            agent.update_Q(mapped_state, action, next_mapped_state, reward)
            #Set new state
            state = next_state
            #Set new bucket state
            mapped_state = next_mapped_state

            env.render()
            t += 1

        HISTORY.append((epoch_i, t))
        #Update probability after one episode (generation)
        epoch_i += 1
        agent.update_prob()
        agent.learning_rate = agent.l_r(epoch_i)

    env.close()




    # print(agent.Q)
