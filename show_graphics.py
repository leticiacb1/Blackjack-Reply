import numpy as np
import matplotlib.pyplot as plt
import json


def plot_test_performance(algoritimo, list_rewards , episodes):

    filename = "results/acumulative_rewards.jpg"

    acumulative_rewards = np.cumsum(list_rewards)
    episodes_list = np.arange(1, episodes+1 , 1)

    algoritimo.plotactions(filename, acumulative_rewards, episodes_list, "Acumulative Rewards per Episodes", "Episodes" , "Acumulative Rewards")