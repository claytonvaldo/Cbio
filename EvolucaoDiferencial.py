import random
from typing import List, Tuple

# ------------------------------ Classe Prato ------------------------------
class Prato:
    def __init__(self, tamanho: int = 5, inicializar: bool = True):
        # Lista de valores (genes). Cada gene ~ quantidade/peso de um alimento.
        self.alimentos: List[float] = []
        if inicializar:
            # Inicializa com valores aleatórios uniformes em [0, 200)
            for _ in range(tamanho):
                self.alimentos.append(random.random() * 200.0)
        else:
            # Constrói o vetor vazio (será preenchido depois)
            self.alimentos = []

    def add(self, valor: float) -> None:
        # Adiciona um gene (valor) ao vetor de alimentos.
        self.alimentos.append(float(valor))

    def __repr__(self) -> str:
        # Representação simplificada para logs: 2 casas decimais
        nums = ", ".join(f"{x:.2f}" for x in self.alimentos)
        return f"Prato([{nums}])"


# ----------------------- Classe Evolucao Diferencial -----------------------
class EvolucaoDiferencial:
    # Parâmetros:
    #  - tamanho: tamanho da população (número de pratos/candidatos)
    #  - F: fator diferencial (peso do termo (B - C)), tipicamente em [0, 2]
    #  - CR: taxa de cruzamento (crossover binomial), tipicamente em [0, 1]
    # O objetivo é MINIMIZAR a função de fitness (quanto menor, melhor).

    def __init__(self, tamanho: int, F: float = 0.8, CR: float = 0.3):
        self.tamanho = tamanho
        self.F = F
        self.CR = CR
        # População de pratos (candidatos)
        self.pratos: List[Prato] = []

    # ---------- Inicialização ----------
    def populacao(self) -> List[Prato]:
        # Cria a população inicial com 'tamanho' pratos aleatórios.
        self.pratos = [Prato(tamanho=5, inicializar=True)
        for _ in range(self.tamanho)]
        return self.pratos

    # ---------- Função de avaliação (fitness) ----------
    @staticmethod
    def fitness(um_prato: Prato) -> float:
        # Calcula o 'erro' em relação às proporções ideais da refeição:
        #  - 55% carboidratos, 30% proteínas, 15% gorduras.
        # A função soma as diferenças absolutas entre as porcentagens obtidas e as ideais.
        # Quanto MENOR o retorno, MELHOR o prato (minimização).

        a = um_prato.alimentos

        carboidratos = a[0] * 0.05 + a[1] * 0.24 + a[2] * 0.26 + \
                       a[3] * 0.15 + a[4] * 0.29
        proteinas    = a[0] * 0.23 + a[1] * 0.02 + a[2] * 0.026 + \
                       a[3] * 0.13 + a[4] * 0.095
        gorduras     = a[0] * 0.05 + a[1] * 0.00 + a[2] * 0.01 + \
                       a[3] * 0.089 + a[4] * 0.014

        total = carboidratos + proteinas + gorduras

        # Evita divisão por zero (se tudo zerado). Penaliza fortemente esse caso.
        if total <= 1e-12:
            return 1e9

        # Converte para porcentagens
        porcao_carbo = (carboidratos / total) * 100.0
        porcao_prot  = (proteinas / total) * 100.0
        porcao_gord  = (gorduras / total) * 100.0

        # Diferenças absolutas para os alvos (55/30/15)
        diff_carbo = abs(porcao_carbo - 55.0)
        diff_prot  = abs(porcao_prot - 30.0)
        diff_gord  = abs(porcao_gord - 15.0)

        # Soma das diferenças: objetivo é minimizar
        diff_total = diff_carbo + diff_prot + diff_gord
        return diff_total

    # ---------- Seleção de 3 vetores (A, B, C) diferentes do parental ----------
    def seleciona3(self, parental: int) -> Tuple[Prato, Prato, Prato]:
        # Seleciona aleatoriamente 3 indivíduos distintos do 'parental'.

        indices = [i for i in range(self.tamanho) if i != parental]

        # Embaralha e pega 3 primeiros
        random.shuffle(indices)
        iA, iB, iC = indices[:3]
        return self.pratos[iA], self.pratos[iB], self.pratos[iC]

    # ---------- Mutação + crossover binomial (gera 'tentativa') ----------
    def mutacao(self, parental: int, trio: Tuple[Prato, Prato, Prato]) -> Prato:
        # Constrói um vetor 'tentativa' (trial vector).
        # Para cada gene:
        #  - Com prob. CR, usa: X = A + F * (B - C)
        #  - Caso contrário, copia o gene do parental
        # Genes negativos são truncados para 0 (como no Java).
        A, B, C = trio
        prato_parental = self.pratos[parental]

        tentativa = Prato(tamanho=5, inicializar=False)  # vazio; iremos preencher

        for i in range(len(prato_parental.alimentos)):
            R = random.random()
            if R < self.CR:
                # DE/rand/1: componente mutante
                X = A.alimentos[i] + self.F * (B.alimentos[i] - C.alimentos[i])
            else:
                # Copia componente do parental (crossover binomial)
                X = prato_parental.alimentos[i]

            # Restrição: não permitir valores negativos
            if X < 0.0:
                X = 0.0

            tentativa.add(X)

        return tentativa

    # ---------- Índice do melhor vetor (menor fitness) ----------
    def melhor_vetor(self) -> int:
        # Retorna o índice do indivíduo com MENOR fitness na população.
        melhor_idx = 0
        melhor_fit = self.fitness(self.pratos[0])
        for i in range(1, self.tamanho):
            f = self.fitness(self.pratos[i])
            if f < melhor_fit:
                melhor_idx = i
                melhor_fit = f
        return melhor_idx

    # ---------- Operações utilitárias (substituição) ----------
    def substituir_se_melhor(self, j: int, candidato: Prato) -> None:
        # Substitui o indivíduo j pelo candidato se o fitness do candidato for melhor (menor).
        if self.fitness(candidato) < self.fitness(self.pratos[j]):
            self.pratos[j] = candidato

# ------------------------------- Execução --------------------------------
if __name__ == "__main__":
    # Parâmetros da DE
    F = 0.8   # peso diferencial (0..2)
    CR = 0.3  # taxa de crossover binomial (0..1)

    # Define tamanho da população (número de pratos) e iterações
    tamanho_pop = 5
    iteracoes = 1000

    # Instancia e inicializa a população
    ed = EvolucaoDiferencial(tamanho=tamanho_pop, F=F, CR=CR)
    ed.populacao()

    # Loop principal (duas camadas: externa = gerações, interna = indivíduos)
    for _ in range(iteracoes):
        for j in range(tamanho_pop):
            # Seleciona 3 vetores (A, B, C) diferentes do parental j
            trio = ed.seleciona3(j)
            # Gera o vetor tentativa via mutação + crossover
            tentativa = ed.mutacao(j, trio)
            # Aplica a regra de substituição se o trial for melhor (menor fitness)
            ed.substituir_se_melhor(j, tentativa)

        # Mostra o melhor da geração atual
        idx = ed.melhor_vetor()
        melhor = ed.pratos[idx]
        print(f"Melhor Vetor: {idx} - {melhor}")
        print(f"Fitness: {EvolucaoDiferencial.fitness(melhor):.6f}")
