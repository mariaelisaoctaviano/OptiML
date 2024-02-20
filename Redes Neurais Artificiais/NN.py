import torch
import time
import pandas as pd
import torch.nn as nn

#Tempo Computacional
inicio = time.time()

# Hiperparâmetros
tamanho_da_entrada = 4
neuronios_camada_oculta = 150
num_camadas = 2
tamanho_da_saida = 1
l_rate = 0.001
epocas = 4000
lookback = 3

# Definindo a classe de rede neural
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

# Inicializando modelo, otimizador e perdas
modelo = LSTMPred(tamanho_da_entrada, neuronios_camada_oculta, tamanho_da_saida, num_camadas) 
otimizador = torch.optim.Adam(modelo.parameters(), lr = l_rate)
criterio = nn.MSELoss() # Critério de perdas

# Treinamento
for epoch in range(epocas):
    otimizador.zero_grad() 
    entradas_n = dados_entrada.clone().detach()
    saidas_n = dados_saida.clone().detach().view(-1,1)
    saida_modelo = modelo(entradas_n)
    perdas = criterio(saida_modelo, saidas_n) # Erro entre modelo e saída esperada
    perdas.backward()
    otimizador.step()

    if epoch % 100 == 0:
        print("Época [{}/{}], Perdas: {:.4f}".format(epoch, epocas, perdas.item()))

# Salvando modelo convergido
torch.save(modelo.state_dict(), 'modelo_resultante.pt')

# Avaliação de Tempo Computacional
fim = time.time()
tempo_tot = (fim - inicio)/3600 # em Horas
print('Tempo de Execução (Horas): {:.2f}'.format(tempo_tot))

a = 1