import gym


#https://gym.openai.com/docs/

def cv5():
    env = gym.make('CartPole-v0')
    print(env.action_space)
    print(env.observation_space)
    print(env.observation_space.high)
    print(env.observation_space.low)




    # env.reset()
    # for _ in range(1000):
    #     env.render()
    #     env.step(env.action_space.sample()) # take a random action
    # env.close()