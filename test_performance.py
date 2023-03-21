from Algoritimos import Algoritimo
import numpy as np
import gymnasium as gym


def test_performance(algoritimo, qtable):
    '''
        Retorna lista de acertos do modelo e percentual de acertos
    '''

    env = gym.make('Blackjack-v1', render_mode='ansi')
    list_rewards = []
    goals = 0

    for i in range(0,100):    
        
        (state, _) = env.reset()
        done = False
        epochs = 0

        while (not done) and (epochs < 100):

            n_state = algoritimo.stateNumber(state)
            action = np.argmax(qtable[n_state])
            state, reward, done, truncated, info = env.step(action)
        
            epochs +=1
        
        goals += reward
        list_rewards.append(reward)

    return goals , list_rewards