import random
import numpy as np
import math

MAX = 'MAX'
MIN = 'MIN'

# Funções objetivo
def f1(x):
    return -(x-3)**2 + 10  # Parabólica invertida (máx em x=3)

def f2(x):
    return x**2  # Parabólica normal (mín em x=0)

def f3(x):
    return (np.sin(5 * x) + 1) * np.exp(-((x - 5) ** 2) / 4)

# Simulated Annealing
def simulatedAnnealing(f, limites=(-10, 10), otimizador=MAX,
                        T_inicial=100, T_final=1e-3, alpha=0.99, iteracoes=1000):
    
    # Ponto inicial aleatório
    x_atual = random.uniform(limites[0], limites[1])
    vl_atual = f(x_atual)
    
    melhor_x, melhor_val = x_atual, vl_atual
    
    T = T_inicial
    
    while T > T_final:
        for _ in range(iteracoes):
            # Gera um vizinho aleatório próximo
            passo = random.uniform(-0.5, 0.5)
            x_novo = x_atual + passo
            if not (limites[0] <= x_novo <= limites[1]):
                continue

            vl_novo = f(x_novo)
            delta = vl_novo - vl_atual

            if otimizador == MAX:
                aceita = delta > 0 or math.exp(delta / T) > random.random()
            else:
                aceita = delta < 0 or math.exp(-delta / T) > random.random()

            if aceita:
                x_atual, vl_atual = x_novo, vl_novo

                # Atualiza melhor solução
                if (otimizador == MAX and vl_atual > melhor_val) or (
                    otimizador == MIN and vl_atual < melhor_val):
                    melhor_x, melhor_val = x_atual, vl_atual

        # Resfriamento
        T *= alpha
    
    return melhor_x, melhor_val

# -----------------------------
# Exemplos de execução:
# -----------------------------
x, valor = simulatedAnnealing(f1, limites=(0, 10), otimizador=MAX,
                               T_inicial=100, T_final=1e-3, alpha=0.95, iteracoes=100)
print(f"Simulated Annealing -> x = {x:.4f}, f(x) = {valor:.4f}")

x, valor = simulatedAnnealing(f2, limites=(0, 10), otimizador=MIN,
                               T_inicial=100, T_final=1e-3, alpha=0.95, iteracoes=100)
print(f"Simulated Annealing -> x = {x:.4f}, f(x) = {valor:.4f}")

x, valor = simulatedAnnealing(f3, limites=(0, 10), otimizador=MAX,
                               T_inicial=100, T_final=1e-3, alpha=0.95, iteracoes=100)
print(f"Simulated Annealing -> x = {x:.4f}, f(x) = {valor:.4f}")

