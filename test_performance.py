from QLearning import *
import gymnasium as gym

def test_performance(qtable):
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

        while (not done) and (epochs < 300):

            n_state = QLearning.stateNumber(state)
            action = np.argmax(qtable[n_state])
            state, reward, done, truncated, info = env.step(action)
            #print(f' Jogando: {action}')
            
            list_rewards.append(reward)
            epochs +=1
        
        goals += reward

    return goals , list_rewards