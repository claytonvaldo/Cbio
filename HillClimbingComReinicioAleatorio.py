import random
import numpy as np

MAX = 'MAX'
MIN = 'MIN'

# Funções objetivo
def f1(x):
    return -(x-3)**2 + 10  # Parabólica invertida (máx em x=3)

def f2(x):
    return x**2  # Parabólica normal (mín em x=0)

def f3(x):
    return (np.sin(5 * x) + 1) * np.exp(-((x - 5) ** 2) / 4)

# Algoritmo Hill Climbing
def hillClimbing(f, x_inicio, passo=0.1, iteracoes=1000, 
                 limites=(-10, 10), otimizador=MIN):
    x_atual = x_inicio
    vl_atual = f(x_atual)
    for _ in range(iteracoes):
      # Gera vizinhos
      vizinhos = [x_atual + passo, x_atual - passo]
      # Mantém dentro dos limites
      vizinhos = [x for x in vizinhos 
                  if limites[0] <= x <= limites[1]]
      vls_vizinho = [f(x) for x in vizinhos]
      if not vls_vizinho:
        break
      # Escolhe melhor vizinho conforme modo
      if otimizador == MIN:
        melhor_vl = min(vls_vizinho)
      else:
        melhor_vl = max(vls_vizinho)  
      melhor_x = vizinhos[vls_vizinho.index(melhor_vl)]
      # Atualiza se encontrou melhor vizinho
      if (otimizador == MIN and melhor_vl < vl_atual) or (
        otimizador == MAX and melhor_vl > vl_atual):
        x_atual = melhor_x
        vl_atual = melhor_vl
      else:
        break # chegou em ótimo local
    return x_atual, vl_atual

# Hill Climbing com Reinício Aleatório
def hillClimbingReinicioAleatorio(f, reinicios=10, passo=0.1, iteracoes=1000,
                                  limites=(-10, 10), otimizador=MIN):
    melhor_x = None
    melhor_valor = None
    for _ in range(reinicios):
      x_inicio = random.uniform(limites[0], limites[1])
      x, valor = hillClimbing(f, x_inicio, passo, iteracoes, 
                                limites, otimizador)
      if melhor_x is None:
        melhor_x, melhor_valor = x, valor
      else:
        if (otimizador == MIN and valor < melhor_valor) or (
          otimizador == MAX and valor > melhor_valor):
          melhor_x, melhor_valor = x, valor
    return melhor_x, melhor_valor

# Maximização
x, valor = hillClimbingReinicioAleatorio(f1, reinicios=20, otimizador=MAX)
print(f"Maximização -> x = {x:.4f}, f(x) = {valor:.4f}")
# Minimização
x, valor = hillClimbingReinicioAleatorio(f2, reinicios=20, otimizador=MIN)
print(f"Minimização -> x = {x:.4f}, f(x) = {valor:.4f}")
# Maximização
x, valor = hillClimbingReinicioAleatorio(f3, reinicios=20, otimizador=MAX)
print(f"Maximização -> x = {x:.4f}, f(x) = {valor:.4f}")