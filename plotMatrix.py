from numpy import loadtxt
import seaborn as sns
import matplotlib.pyplot as plt

def plot_matrix(data,namefile):
    plt.title(namefile)
    ax = sns.heatmap(data, cmap="PiYG", cbar=False, linewidth=.5)
    ax.set_xlabel('Dealer Showing')
    ax.set_ylabel('Player Sum')
    ax.set_yticklabels(range(1, 22))
    ax.set_xticklabels(["A"] + list(range(2, 11)), fontsize=12)
    plt.savefig(namefile+'.png')

usable_ace = loadtxt('usable_ace.csv',delimiter=',')
not_usable_ace = loadtxt('not_usable_ace.csv',delimiter=',')

plot_matrix(usable_ace,'Usable_ace')
plot_matrix(not_usable_ace,'Not_usable_ace')