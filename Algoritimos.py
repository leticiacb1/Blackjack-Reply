import random
import numpy as np
import matplotlib.pyplot as plt

class Algoritimo():

    def __init__(self, env, alpha, gamma, epsilon, epsilon_min, epsilon_dec, episodes):
        self.env = env
        self.q_table = np.zeros([env.observation_space[0].n*env.observation_space[1].n*env.observation_space[2].n, env.action_space.n])
        self.alpha = alpha                  # Taxa de aprendizado , quão maior, maior valor se da ao aprendizado.
        self.gamma = gamma                  # O quão relevante são as ecompensas futuras em relação a atual 
        self.epsilon = epsilon              # Chance de escolha de ação aleatória 
        self.epsilon_min = epsilon_min
        self.epsilon_dec = epsilon_dec
        self.episodes = episodes

    def select_action(self, state):
        rv = random.uniform(0, 1)
        if rv < self.epsilon:
            return self.env.action_space.sample()           # Explore action space
        return np.argmax(self.q_table[state])               # Exploit learned values
    
    def select_random_action(self):
        return self.env.action_space.sample() # Explore action space

    def plotactions(self, filename, y_data, x_data, titulo, x_label , y_label):
        plt.scatter(x_data, y_data)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(titulo)
        plt.xlim(0,100)
        plt.grid(True)
        plt.savefig(filename)     
        plt.close()
    
    @staticmethod
    def stateNumber(state):
        (x,y,z) = state
        y = y * 32
        z = z * 352
        return x+y+z