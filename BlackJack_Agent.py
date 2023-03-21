import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from QLearning import QLearning
from Sarsa import Sarsa
from Algoritimos import Algoritimo
from numpy import loadtxt
from progress.bar import IncrementalBar
from show_graphics import plot_test_performance
import json
from numpy import savetxt
from test_performance import *
import sys
import warnings
warnings.simplefilter("ignore")


def main():

    # Condições do programa:
    treino = False
    method = 'qlearning'

    # --- Filenames ---
    csv_filename = 'data/q-table-blackjack.csv'
    plot_rewards_filename = 'results/blackjack.jpg'
    parameters_filename = 'data/info_parameters.json'

    if(treino):
        # ----- Parâmetros para GridSearch ----
        list_alpha = [ 0.0001, 0.1 , 0.15  , 0.4]   
        list_gamma = [ 0.01, 0.3 , 0.4, 0.9,  0.98]  
        list_epsilon = [0.001, 0.5,  0.6,0.95 ] 

        epsilon_min = 0.0001
        epsilon_dec = 0.9999
        episodes  = 100000

        # ----- Barra de Progresso ----
        size = len(list_alpha)*len(list_gamma)*len(list_epsilon)
        bar = IncrementalBar(' Progress ', max = size)

        # ----- Melhor conjunto [alpha, gama, epsilon] e dicionario com rewards de teste da performance  -----
        #  {"alpha - gamma - epsilon" = { %acertos , [1,-1,0,1,1 ...] } , ...}    

        best_goal = 0
        dic_goals = {}    
        best_game_results = {'wins': 0 , 'losts' : 0 , 'ties': 0}     

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
                    
                    qtable , rewards_per_episode,usable_ace,not_usable_ace  = algoritimo.train()
                    
                    # ----- Calcula percentual de acertos -----
                    goals , wins, ties, loses, list_rewards = test_performance(algoritimo, qtable) 
                    
                    # ----- Monta dicionário com desempenhos -----
                    parameters_str = f"{alpha} - {gamma} - {epsilon}"
                    dic_goals[parameters_str] = goals
                    
                    # ----- Salva melhores parâmetros -----
                    if(goals > best_goal):
                        best_goal = goals
                        best_set = [alpha, gamma, epsilon]

                        best_game_results['wins'] = wins
                        best_game_results['losts'] = loses
                        best_game_results['ties'] = ties

                        # Salva dados
                        savetxt(csv_filename, qtable, delimiter=',')
                        savetxt('data/usable_ace.csv', usable_ace, delimiter=',')
                        savetxt('data/not_usable_ace.csv', not_usable_ace, delimiter=',')

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
        
        print(f"\n > Percentual de acertos : {wins + ties} % \n")    

        print("\n----------------------------------------------------")
        print("                BEST GAME RESULTS                   ")
        print("----------------------------------------------------\n") 

        print(f"\n > Venceu : {best_game_results['wins']} % \n")
        print(f"\n > Perdeu : {best_game_results['losts']} % \n")
        print(f"\n > Empatou : {best_game_results['ties']} %\n")

        print(f"\n > Percentual de acertos : {best_game_results['wins'] + best_game_results['ties']} % \n")   

        # --- Salva dicionario de Grid Search ---
        with open(parameters_filename, 'w') as fp:
            json.dump(dic_goals ,fp)  

    else:
        
        # ----- Utiliza tabela já treinada -----
        qtable = loadtxt(csv_filename, delimiter=',')

        # ----- Ambiente e algorítimo (Qualquer um) -----
        env = gym.make('Blackjack-v1', render_mode='ansi')
        algoritimo = Algoritimo(env, alpha=0.1, gamma=0.9, epsilon=0.1, epsilon_min=0.0001, epsilon_dec= 0.9999, episodes=1000)

        # ----- Calcula percentual de acertos -----
        goals , wins, ties, loses, list_rewards = test_performance(algoritimo, qtable) 

        print("\n----------------------------------------------------")
        print("                BEST GAME RESULTS                   ")
        print("----------------------------------------------------\n") 

        print(f"\n > Venceu : {wins} % \n")
        print(f"\n > Perdeu : {loses} % \n")
        print(f"\n > Empatou : {ties} %\n")

        print(f"\n > Percentual de acertos : {wins + ties} % \n")        

if __name__ == '__main__':

    main()