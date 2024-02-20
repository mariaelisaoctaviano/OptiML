import torch
import pandas as pd
import torch.nn as nn
import matplotlib.pyplot as plt

# Definição de Hiperparâmetros
tamanho_da_entrada = 4
neuronios_camada_oculta = 150
num_camadas = 2
tamanho_da_saida = 1
l_rate = 0.001
epocas = 4000
lookback = 3

# Definição da classe de rede neural
class LSTMPred(nn.Module):
    def __init__(self, tamanho_da_entrada, neuronios_camada_oculta, tamanho_da_saida, num_camadas):
        super(LSTMPred, self).__init__()
        self.neuronios_camada_oculta = neuronios_camada_oculta
        self.num_camadas = num_camadas
        self.lstm1 = nn.LSTM(tamanho_da_entrada, neuronios_camada_oculta, 1, batch_first=True)
        self.lstm2 = nn.LSTM(neuronios_camada_oculta, neuronios_camada_oculta, 1, batch_first=True)  # Adjusted input size
        self.fc = nn.Linear(neuronios_camada_oculta, tamanho_da_saida)  # Adjusted input size

    def forward(self, x):
        h0 = torch.zeros(self.num_camadas, x.size(0), self.neuronios_camada_oculta)
        c0 = torch.zeros(self.num_camadas, x.size(0), self.neuronios_camada_oculta)
        out, _ = self.lstm1(x, (h0[0:1], c0[0:1]))
        out, _ = self.lstm2(out, (h0[1:], c0[1:]))
        out = self.fc(out[:, -1, :])
        return out
    
# Definição do modelo
modelo = LSTMPred(tamanho_da_entrada, neuronios_camada_oculta, tamanho_da_saida, num_camadas) 
modelo.load_state_dict(torch.load('modelo_resultante.pt'))

# Carregando o arquivo CSV para um DataFrame
df = pd.read_csv("data.csv")
linhas = 365

# Dividindo a coluna concatenada em várias colunas
df[['t_0', 't_1', 't_2', 't_3', 't_4']] = df['t_0;t_1;t_2;t_3;t_4'].str.split(';', expand=True)

# Convertendo as colunas numéricas para float e lidar com valores não numéricos
for coluna in ['t_0', 't_1', 't_2', 't_3', 't_4']:
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

# Descartando a coluna original concatenada
df.drop(columns=['t_0;t_1;t_2;t_3;t_4'], inplace=True)

# Removendo linhas com valores não numéricos
df = df.dropna()

# Convertendo os valores para tensores float
entradas_ini = torch.tensor(df[['t_0', 't_1', 't_2', 't_3', 't_4']].values).float()

# Definindo dados de entrada da rede
entradas_tot = entradas_ini[:, :-1] 

# Definindo dados de saídas esperadas da rede
labels_tot = entradas_ini[:, -1] 

entradas = entradas_tot[:linhas].float().unsqueeze(0)
saidas_esp = labels_tot[:linhas+1].float().unsqueeze(0).unsqueeze(-1)

# Preparando dados para rede usando lookback
amostras = entradas.shape[1] - lookback
dados_entrada = torch.zeros((amostras, lookback, tamanho_da_entrada))

for i in range(amostras):
    dados_entrada[i] = entradas[:, i:i+lookback, :]

dados_saida = []
for i in range(lookback, linhas):
    dados_s = saidas_esp[:, i, :].flatten()
    dados_saida.append(dados_s)

dados_saida = torch.cat(dados_saida) # De acordo com a observação de três entradas anteriores, é gerada uma saída

# Definição do vetor de tempo
t1 = [i for i in range(3,365)]

# Aplicação do modelo aos dados
output = modelo(dados_entrada)

# Gráfico de Resultados
plt.figure(1)
plt.plot(t1, dados_saida.detach().numpy(), color='blue', label='Saída Real')
plt.plot(t1, output.detach().numpy(), color = 'red', label = 'Resposta da RNA')
plt.xlabel('Tempo')
plt.ylabel('Temperatura')
plt.title('Resultados da Previsão de Temperaturas')
plt.legend()
plt.savefig('Resultados da Previsão de Temperaturas')
plt.show()

a = 1