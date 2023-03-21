import numpy as np
import random
from numpy import savetxt
import sys
import matplotlib.pyplot as plt

from Algoritimos import Algoritimo

class Sarsa(Algoritimo):

    def __init__(self, env, alpha, gamma, epsilon, epsilon_min, epsilon_dec, episodes):
        super().__init__(env, alpha, gamma, epsilon, epsilon_min, epsilon_dec, episodes)
        
    def train(self):
    
        reward_per_episode = []
        rewards = 0

        for i in range(1, self.episodes+1):
            (state, _) = self.env.reset()     
            done = False
           
            # Escolhe uma ação inicial
            n_state = Sarsa.stateNumber(state)
            action = self.select_action(n_state) 

            while not done:
                                               
                next_state, reward, done, truncated, _ = self.env.step(action)     # Executa uma ação

                # Next action:
                n_next_state = Sarsa.stateNumber(next_state)
                next_action = self.select_action(n_next_state) 

                # Itera sobre Q-table:
                old_value = self.q_table[n_state,action]                             # Valor da ação escolhida no estado atual 
                next_q_value = self.q_table[n_next_state, next_action]               # Melhor valor de um estado futuro
                
                # Atualiza o valor do estado atual considerando o Algoritimo Sarsa (on policy) 
                new_value = old_value + self.alpha*(reward + self.gamma*next_q_value - old_value)             
                self.q_table[n_state, action] = new_value
                
                # Atualiza para o novo estado
                n_state = n_next_state
                rewards+=reward

                # Aplica a ação escolhida:
                action = next_action
            
            reward_per_episode.append(rewards)

            if self.epsilon > self.epsilon_min:
                self.epsilon = self.epsilon * self.epsilon_dec
        
        return self.q_table , reward_per_episode ,_,_