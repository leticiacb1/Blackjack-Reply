import numpy as np
import random
from numpy import savetxt
import matplotlib.pyplot as plt
from Algoritimos import Algoritimo

#
# Esta é uma versão do Q-Learning com adicao de um metodo para tratamento dos estados
# do ambiente BlackJack. 
#

class QLearning(Algoritimo):

    def __init__(self, env, alpha, gamma, epsilon, epsilon_min, epsilon_dec, episodes):
        super().__init__(env, alpha, gamma, epsilon, epsilon_min, epsilon_dec, episodes)


    def train(self):
        rewards_per_episode = []
        rewards = 0
        usable_ace = np.zeros((21,10))
        not_usable_ace = np.zeros((21,10))
        for i in range(1, self.episodes+1):
            (state, _) = self.env.reset()
            done = False

            while not done:
                n_state = QLearning.stateNumber(state)
                action = self.select_action(n_state)
                if state[2]:
                    usable_ace[state[0]-1,state[1]-1] = action
                else:
                    not_usable_ace[state[0]-1,state[1]-1] = action
                next_state, reward, done, _, _ = self.env.step(action) 
                n_next_state = QLearning.stateNumber(next_state)

                # Adjust Q value for current state
                old_value = self.q_table[n_state, action]
                next_max = np.max(self.q_table[n_next_state])
                new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
                self.q_table[n_state, action] = new_value
                
                state = next_state
                rewards += reward

            # if i % 1000 == 0:
            #     rewards_per_episode.append(rewards)
            #     print("Episodes: " + str(i) +' Rewards: '+str(rewards))
            #     rewards = 0
            
            if self.epsilon > self.epsilon_min:
                self.epsilon = self.epsilon * self.epsilon_dec
        return self.q_table , rewards_per_episode, usable_ace, not_usable_ace