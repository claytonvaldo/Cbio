import random
import numpy as np
MAX = 'MAX'
MIN = 'MIN'

# Funções objetivo
def f1(x):
    return -(x-3)**2 + 10

def f2(x):
    return x**2

def f3(x):
    return (np.sin(5 * x) + 1) * np.exp(-((x - 5) ** 2) / 4)

def hillClimbing(f, x_inicio, passo=0.1, iteracoes=1000, limites=(-10, 10), otimizador=MIN):
    x_atual = x_inicio
    vl_atual = f(x_atual)
    
    for _ in range(iteracoes):
        # Gera vizinhos
        vizinhos = [x_atual + passo, x_atual - passo]
        # Mantém vizinhos dentro dos limites
        vizinhos = [x for x in vizinhos 
                    if limites[0] <= x <= limites[1]]
        vls_vizinho = [f(x) for x in vizinhos]
        if not vls_vizinho:
            break
        # Escolhe melhor vizinho conforme modo de otimização
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
            break  # Chegou em ótimo local
    return x_atual, vl_atual

# -----------------------------
# Exemplos de execução:
# -----------------------------
x_inicio = random.uniform(-10, 10)
# Maximização
x, valor = hillClimbing(f1, x_inicio, otimizador=MAX)
print(f"Maximização -> x = {x:.4f}, f(x) = {valor:.4f}")
# Minimização
x, valor = hillClimbing(f2, x_inicio, otimizador=MIN)
print(f"Minimização -> x = {x:.4f}, f(x) = {valor:.4f}")
# Maximização
x, valor = hillClimbing(f3, x_inicio, otimizador=MAX)
print(f"Maximização -> x = {x:.4f}, f(x) = {valor:.4f}")
