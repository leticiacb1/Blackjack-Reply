##  blackjack-reply98 🃏️


### Bibliotecas ⚙️

Instale as dependências:

```bash
  pip install -r requirements.txt
```

### Parâmetros para o código 📌️

Nas primeiras linhas do código temos o seguinte:

```bash
    # Condições do programa:
    treino = True
    method = 'qlearning'
```

O parâmetro de treino indica se será feita uma GridSearch para a busca dos melhores parâmetros (**treino = True**) , ou se deseja utilizar a tabela já pronta em `data/q-table-blackjack.csv` (**treino = False**).

o parâmetro método define com qual algorítimo o treino será feito Sarsa (**method = sarsa**) ou QLearning (**method = qlearning**).

### Melhores Hyperparâmetros


| Atributo        |  Valor     |
|:----------------|:----------:|
| Algoritmo       |       |
| alpha           |        |
| gamma           |        |
| epsilon         |       |
| epsilon_dec     |     |
| epsilon_min     |      |
| qtd_episodios   |      |

### Gráfico Qtable
