import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from QLearning import QLearning
from Sarsa import Sarsa
from numpy import loadtxt
from progress.bar import IncrementalBar
from show_graphics import plot_test_performance
import json
from numpy import savetxt
from test_performance import *
import warnings
warnings.simplefilter("ignore")


def main():

    # Condições do programa:
    treino = True
    method = 'qlearning'

    # --- Filenames ---
    csv_filename = 'data/q-table-blackjack.csv'
    plot_rewards_filename = 'results/blackjack.jpg'
    parameters_filename = 'data/info_parameters.json'

    if(treino):
        # ----- Parâmetros para GridSearch ----
        list_alpha = [0.000001, 0.01, 0.03, 0.05 , 0.5, 0.1 , 0.15 , 0.6 ]   
        list_gamma = [0.000001, 0.1, 0.3 , 0.5, 0.85 , 0.95 ]  
        list_epsilon = [0.1, 0.3 , 0.5 , 0.88,  0.9, 0.95 ] 

        epsilon_min = 0.0001
        epsilon_dec = 0.9999
        episodes  = 20000 

        # ----- Barra de Progresso ----
        size = len(list_alpha)*len(list_gamma)*len(list_epsilon)
        bar = IncrementalBar(' Progress ', max = size)

        # ----- Melhor conjunto [alpha, gama, epsilon] e dicionario com rewards de teste da performance  -----
        #  {"alpha - gamma - epsilon" = { %acertos , [1,-1,0,1,1 ...] } , ...}    

        best_goal = 0
        dic_goals = {}         

        # ----- GridSearch -----
        print("\n----------------------------------------------------")
        print("------------------- GRID SEARCH --------------------")
        print("----------------------------------------------------\n")

        for alpha in list_alpha:
            for gamma in list_gamma:
                for epsilon in list_epsilon:

                    # ----- Ambiente -----
                    env = gym.make('Blackjack-v1', render_mode='ansi')

                    # ----- Treina modelo -----
                    if(method ==  'qlearning'):
                        algoritimo = QLearning(env, alpha=alpha, gamma=gamma, epsilon=epsilon, epsilon_min=epsilon_min, epsilon_dec=epsilon_dec, episodes=episodes)
                    elif(method ==  'sarsa'):
                        algoritimo = Sarsa(env, alpha=alpha, gamma=gamma, epsilon=epsilon, epsilon_min=epsilon_min, epsilon_dec=epsilon_dec, episodes=episodes)
                    
                    qtable , rewards_per_episode  = algoritimo.train()
                    
                    # ----- Calcula percentual de acertos -----
                    goals , list_rewards = test_performance(algoritimo, qtable) 
                    
                    # ----- Monta dicionário com desempenhos -----
                    parameters_str = f"{alpha} - {gamma} - {epsilon}"
                    dic_goals[parameters_str] = [goals , list_rewards]
                    
                    # ----- Salva melhores parâmetros -----
                    if(goals > best_goal):
                        best_goal = goals
                        best_set = [alpha, gamma, epsilon]

                        # Salva dados
                        savetxt(csv_filename, qtable, delimiter=',')

                        # Faz grafico de acumulativo de rewards
                        plot_test_performance(algoritimo, list_rewards, 100)

                    # --- Atualiza Progresso ---
                    bar.next()

        print("\n----------------------------------------------------")
        print("                  BEST METRICS FIND                   ")
        print("----------------------------------------------------\n")      
        
        print(f"\n > Alpha : {best_set[0]}\n")
        print(f"\n > Gamma : {best_set[1]}\n")
        print(f"\n > Epsilon : {best_set[2]}\n")
        
        print(f"\n > Percentual de acertos : {best_goal} % \n")

        # --- Salva dicionario de Grid Search ---
        with open(parameters_filename, 'w') as fp:
            json.dump(dic_goals ,fp)  

    else:
        
        # ----- Utiliza tabela já treinada -----
        q_table = loadtxt(csv_filename, delimiter=',')

        # ----- Calcula percentual de acertos -----
        goals , list_rewards = test_performance(qtable) 

        print(f"\n > Percentual de acertos : {best_goal} % \n")        

    # (state, _) = env.reset()
    # done = False

    # while not done:
    #     print(state)
    #     n_state = QLearning.stateNumber(state)
    #     action = np.argmax(q_table[n_state])
    #     state, reward, done, truncated, info = env.step(action)
    #     print(f' Jogando: {action}')
        
    # print(f' Cartas do meu jogador: {env.player}')
    # print(f' Cartas do dealer: {env.dealer}')

    # if reward == 1:
    #     print('Meu jogador venceu')
    # elif reward == 0:
    #     print('Jogo empatou')
    # elif reward == -1:
    #     print('Dealer ganhou')

if __name__ == '__main__':
    main()