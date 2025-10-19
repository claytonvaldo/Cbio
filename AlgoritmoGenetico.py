import random   # Biblioteca padrão para geração de números aleatórios

# ---------------- Classe Produto ----------------
class Produto:
    def __init__(self, nome, espaco, valor):
        # Estrutura que representa um item disponível para escolha
        self.nome = nome        # Nome do produto
        self.espaco = espaco    # Espaço ocupado (restrição da mochila)
        self.valor = valor      # Valor do produto (benefício a ser maximizado)


# ---------------- Classe Individuo ----------------
class Individuo:
    def __init__(self, espacos, valores, limiteEspacos):
        # Cada indivíduo é uma possível solução (cromossomo) do problema
        self.espacos = espacos              # Lista com espaços de todos os produtos
        self.valores = valores              # Lista com valores de todos os produtos
        self.limiteEspacos = limiteEspacos  # Capacidade máxima permitida
        self.notaAvaliacao = 0.0            # Fitness do indivíduo (valor total da solução)
        self.espacoUsado = 0.0              # Espaço total consumido pelos itens escolhidos
        self.geracao = 0                    # Geração em que o indivíduo foi criado
        self.cromossomo = []                # Vetor binário de 0/1 indicando se item foi escolhido
        self.criacao()                      # Inicializa o cromossomo aleatoriamente

    def criacao(self):
        # Inicializa cromossomo aleatório: cada gene tem 50% de chance de ser 1
        self.cromossomo = ["1" if random.random() < 0.5
                           else "0" for _ in self.espacos]

    def avaliacao(self):
        # Calcula a "aptidão" do indivíduo
        nota = 0.0
        somaEspacos = 0.0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == "1":     # Se o gene for "1", produto é incluído
                nota += self.valores[i]       # Soma valor do produto
                somaEspacos += self.espacos[i]# Soma espaço do produto

        if somaEspacos > self.limiteEspacos:  # Se ultrapassar o limite, aplica penalidade
            nota = 1.0

        self.notaAvaliacao = nota             # Armazena valor final (fitness)
        self.espacoUsado = somaEspacos        # Armazena espaço usado

    def crossover(self, outro):
        # Realiza crossover (recombinação) com outro indivíduo
        corte = round(random.random() * len(self.cromossomo)) # Ponto de corte
        filho1 = outro.cromossomo[:corte] + self.cromossomo[corte:] # Combina prefixo/sufixo
        filho2 = self.cromossomo[:corte] + outro.cromossomo[corte:]

        # Cria filhos como novos indivíduos
        f1 = Individuo(self.espacos, self.valores, self.limiteEspacos)
        f1.cromossomo = filho1
        f1.geracao = self.geracao + 1

        f2 = Individuo(self.espacos, self.valores, self.limiteEspacos)
        f2.cromossomo = filho2
        f2.geracao = self.geracao + 1

        return [f1, f2]

    def mutacao(self, taxaMutacao):
        # Aplica mutação em cada gene do cromossomo
        for i in range(len(self.cromossomo)):
            if random.random() < taxaMutacao: # Se cair dentro da taxa de mutação
                # Inverte o gene: 0 -> 1 ou 1 -> 0
                self.cromossomo[i] = "0" if self.cromossomo[i] == "1" else "1"
        return self


# ---------------- Classe Algoritmo Genético ----------------
class AlgoritmoGenetico:
    def __init__(self, tamanhoPopulacao):
        self.tamanhoPopulacao = tamanhoPopulacao # Número de indivíduos
        self.populacao = []                      # Lista da população atual
        self.melhorSolucao = None                # Guarda o melhor indivíduo já encontrado

    def inicializaPopulacao(self, espacos, valores, limiteEspacos):
        # Cria população inicial com indivíduos aleatórios
        self.populacao = [Individuo(espacos, valores, limiteEspacos)
                          for _ in range(self.tamanhoPopulacao)]
        self.melhorSolucao = self.populacao[0]

    def ordenaPopulacao(self):
        # Ordena população em ordem decrescente de aptidão (fitness)
        self.populacao.sort(key=lambda ind: ind.notaAvaliacao,
                            reverse=True)

    def melhorIndividuo(self, individuo):
        # Atualiza o melhor indivíduo global se encontrar um superior
        if individuo.notaAvaliacao > self.melhorSolucao.notaAvaliacao:
            self.melhorSolucao = individuo

    def somaAvaliacoes(self):
        # Retorna a soma dos fitness da população (usada na seleção por roleta)
        return sum(ind.notaAvaliacao for ind in self.populacao)

    def selecionaPai(self, somaAvaliacao):
        # Seleção por roleta: sorteia um pai proporcional ao fitness
        valorSorteado = random.random() * somaAvaliacao
        soma = 0.0
        for i, ind in enumerate(self.populacao):
            soma += ind.notaAvaliacao
            if soma >= valorSorteado:
                return i
        return len(self.populacao) - 1  # Retorna último caso não encontre antes

    def visualizaGeracao(self):
        # Mostra informações do melhor indivíduo da geração atual
        melhor = self.populacao[0]
        print(f"G: {melhor.geracao} "
              f"Valor: {melhor.notaAvaliacao:.2f} "
              f"Espaco: {melhor.espacoUsado:.3f} "
              f"Cromossomo: {melhor.cromossomo}")

    def resolver(self, taxaMutacao, numeroGeracoes, espacos,
                 valores, limiteEspacos):
        # Algoritmo principal (loop evolutivo)
        self.inicializaPopulacao(espacos, valores, limiteEspacos)

        # Avalia e ordena população inicial
        for ind in self.populacao:
            ind.avaliacao()
        self.ordenaPopulacao()
        self.visualizaGeracao()

        # Loop das gerações
        for _ in range(numeroGeracoes):
            somaAvaliacao = self.somaAvaliacoes()
            novaPopulacao = []

            # Gera nova população através de seleção, crossover e mutação
            for _ in range(0, self.tamanhoPopulacao // 2):
                pai1 = self.selecionaPai(somaAvaliacao)
                pai2 = self.selecionaPai(somaAvaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                novaPopulacao.append(filhos[0].mutacao(taxaMutacao))
                novaPopulacao.append(filhos[1].mutacao(taxaMutacao))

            # Substitui população antiga pela nova
            self.populacao = novaPopulacao
            for ind in self.populacao:
                ind.avaliacao()
            self.ordenaPopulacao()
            self.visualizaGeracao()
            self.melhorIndividuo(self.populacao[0])

        # Exibe e retorna a melhor solução encontrada
        print(f"\nMelhor solução -> Geração {self.melhorSolucao.geracao} "
              f"Valor: {self.melhorSolucao.notaAvaliacao:.2f} "
              f"Espaço: {self.melhorSolucao.espacoUsado:.3f} "
              f"Cromossomo: {self.melhorSolucao.cromossomo}")
        return self.melhorSolucao.cromossomo


# ---------------- Execução principal ----------------
if __name__ == "__main__":
    # Lista de produtos com nome, espaço ocupado e valor
    listaProdutos = [
        Produto("Geladeira Dako", 0.751, 999.90),
        Produto("Iphone 6", 0.000089, 2911.12),
        Produto("TV 55'", 0.400, 4346.99),
        Produto("TV 50'", 0.290, 3999.90),
        Produto("TV 42'", 0.200, 2999.00),
        Produto("Notebook Dell", 0.00350, 2499.90),
        Produto("Ventilador Panasonic", 0.496, 199.90),
        Produto("Microondas Electrolux", 0.0424, 308.66),
        Produto("Microondas LG", 0.0544, 429.90),
        Produto("Microondas Panasonic", 0.0319, 299.29),
        Produto("Geladeira Brastemp", 0.635, 849.00),
        Produto("Geladeira Consul", 0.870, 1199.89),
        Produto("Notebook Lenovo", 0.498, 1999.90),
        Produto("Notebook Asus", 0.527, 3999.00),
    ]

    # Extração dos atributos para uso no AG
    espacos = [p.espaco for p in listaProdutos]
    valores = [p.valor for p in listaProdutos]
    nomes = [p.nome for p in listaProdutos]  # Criado mas não utilizado

    # Parâmetros do problema e do AG
    limite = 3.0             # Capacidade máxima
    tamanhoPopulacao = 100   # Quantidade de indivíduos
    taxaMutacao = 0.01       # Probabilidade de mutação por gene
    numeroGeracoes = 100     # Quantidade de gerações

    # Criação e execução do Algoritmo Genético
    ag = AlgoritmoGenetico(tamanhoPopulacao)
    resultado = ag.resolver(taxaMutacao, numeroGeracoes,
                            espacos, valores, limite)

    # Exibe os produtos escolhidos na melhor solução final
    print("\nProdutos escolhidos:")
    for i in range(len(listaProdutos)):
        if resultado[i] == "1":
            print("Nome:", listaProdutos[i].nome)
