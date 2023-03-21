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

    win = 0
    tie = 0
    lose = 0

    for i in range(0,100):    
        
        (state, _) = env.reset()
        done = False
        epochs = 0

        while (not done) and (epochs < 100):

            n_state = algoritimo.stateNumber(state)
            action = np.argmax(qtable[n_state])
            state, reward, done, truncated, info = env.step(action)
        
            epochs +=1
        
        if(reward == 1):
            win+=1
        elif(reward == -1):
            lose+=1
        else:
            tie+=1

        goals += reward
        list_rewards.append(reward)

    return goals, win, tie, lose, list_rewards