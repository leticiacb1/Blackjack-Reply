import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from QLearning_BlackJack import QLearning
from numpy import loadtxt
import warnings
warnings.simplefilter("ignore")

env = gym.make('Blackjack-v1', render_mode='ansi')

csv_filename = 'data/q-table-blackjack.csv'
plot_rewards_filename = 'results/blackjack'

#
# para treinar a q-table
#

qlearn = QLearning(env, alpha=0.01, gamma=0.001, epsilon=0.9, epsilon_min=0.01, epsilon_dec=0.99, episodes=1000000)
q_table , rewards_per_episode  = qlearn.train()

# Salva dados:
savetxt(csv_filename, self.q_table, delimiter=',')
qlearn.plotactions(plot_rewards_filename, rewards_per_episode)

# para usar a q-table treinada
#q_table = loadtxt('data/q-table-blackjack.csv', delimiter=',')

(state, _) = env.reset()
done = False

while not done:
    print(state)
    n_state = QLearning.stateNumber(state)
    action = np.argmax(q_table[n_state])
    state, reward, done, truncated, info = env.step(action)
    print(f' Jogando: {action}')
    
print(f' Cartas do meu jogador: {env.player}')
print(f' Cartas do dealer: {env.dealer}')

if reward == 1:
    print('Meu jogador venceu')
elif reward == 0:
    print('Jogo empatou')
elif reward == -1:
    print('Dealer ganhou')