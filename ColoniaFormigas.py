import random

class Aresta:
    def __init__(self, o: str, d: str):
        self.origem = o
        self.destino = d

    def getOrigem(self) -> str:
        return self.origem

    def setOrigem(self, origem: str) -> None:
        self.origem = origem

    def getDestino(self) -> str:
        return self.destino

    def setDestino(self, destino: str) -> None:
        self.destino = destino

class Caminho:
    def __init__(self, origem: str, destino: str, dist: int, fero: float):
        self.caminho = Aresta(origem, destino)
        self.adjacentes = []
        self.distancia = dist
        self.feromonio = fero

    def addAdjacente(self, camAdj: "Caminho") -> None:
        self.getAdjacentes().append(camAdj)

    def possuiInicio(self, inicio: str) -> bool:
        return self.getCaminho().getOrigem() == inicio

    def possuiFim(self, fim: str) -> bool:
        return self.getCaminho().getDestino() == fim

    def __str__(self) -> str:
        return f"{self.caminho.getOrigem()}-{self.caminho.getDestino()}: " \
         f"{self.getDistancia()}, {self.getFeromonio()}"

    # getters / setters (mantidos com nomes do Java)
    def getCaminho(self) -> Aresta:
        return self.caminho

    def setCaminho(self, caminho: Aresta) -> None:
        self.caminho = caminho

    def getAdjacentes(self) -> list:
        return self.adjacentes

    def setAdjacentes(self, adjacentes: list) -> None:
        self.adjacentes = adjacentes

    def getDistancia(self) -> int:
        return self.distancia

    def setDistancia(self, distancia: int) -> None:
        self.distancia = distancia

    def getFeromonio(self) -> float:
        return self.feromonio

    def setFeromonio(self, feromonio: float) -> None:
        self.feromonio = feromonio

class ColoniaFormigas:
    def __init__(self, inicio: str, fim: str):
        self.caminhos = []
        self.inicio = inicio
        self.fim = fim

    def addCaminho(self, umCaminho: Caminho) -> None:
        self.getCaminhos().append(umCaminho)

    # ---- Probabilidade baseada em feromônio * (1 / distância) ----
    def geraProbabilidade(self, umCaminho: Caminho) -> list:
        atratividades = 0.0
        atrativs = []
        probs = []
        adjs = []

        # Encontrar a lista de adjacentes do caminho informado
        for c in self.getCaminhos():
            if c is umCaminho:
                adjs = c.getAdjacentes()
                break

        # Calcula atratividade de cada adjacente
        for adj in adjs:
            distancia = adj.getDistancia()
            feromonio = adj.getFeromonio()
            # evitar divisão por zero
            atratividade = feromonio * (1.0 / distancia if distancia != 0 else 0.0)
            atrativs.append(atratividade)
            atratividades += atratividade

        # Normaliza para probabilidades
        for a in atrativs:
            probabilidade = (a / atratividades) if atratividades > 0 else 0.0
            probs.append(probabilidade)

        return probs

    def geraProbabilidade_lista(self, listaArestas: list) -> list:
        atratividades = 0.0
        atrativs = []
        probs = []

        for cam in listaArestas:
            distancia = cam.getDistancia()
            feromonio = cam.getFeromonio()
            atratividade = feromonio * (1.0 / distancia if distancia != 0 else 0.0)
            atrativs.append(atratividade)
            atratividades += atratividade

        for a in atrativs:
            probabilidade = (a / atratividades) if atratividades > 0 else 0.0
            probs.append(probabilidade)

        return probs

    # ---- Escolhas por roleta (limiares cumulativos) ----
    def escolheAresta(self, umCaminho: Caminho) -> Caminho | None:
        probabilidades = self.geraProbabilidade(umCaminho)
        limiares = []
        escolha = None
        cont = 0
        soma = 0.0
        sorteio = random.random()

        adjs = umCaminho.getAdjacentes()
        if adjs:
            for p in probabilidades:
                soma += p
                limiares.append(soma)

            for lim in limiares:
                if sorteio > lim:
                    cont += 1

            # proteção para não estourar índice
            if cont >= len(adjs):
                cont = len(adjs) - 1

            escolha = adjs[cont]
        return escolha

    def primeiraAresta(self, listaArestas: list) -> Caminho | None:
        probabilidades = self.geraProbabilidade_lista(listaArestas)
        limiares = []
        escolha = None
        cont = 0
        soma = 0.0
        sorteio = random.random()

        for p in probabilidades:
            soma += p
            limiares.append(soma)

        for lim in limiares:
            if sorteio > lim:
                cont += 1

        if listaArestas:
            if cont >= len(listaArestas):
                cont = len(listaArestas) - 1
            escolha = listaArestas[cont]

        return escolha

    # ---- Medidas de caminho e atualização de feromônio ----
    def comprimento(self, caminho: list) -> float:
        soma = 0.0
        for cam in caminho:
            soma += cam.getDistancia()
        return soma

    def evaporaFeromonio(self, taxa: float) -> None:
        for c in self.getCaminhos():
            novoFeromonio = c.getFeromonio() * (1 - taxa)
            c.setFeromonio(novoFeromonio)

    def marcaFeromonio(self, caminho: list) -> None:
        #novoFeromonio = 1.0 / self.comprimento(caminho) if self.comprimento(caminho) > 0 else 0.0
        novoFeromonio = (
            1.0 / self.comprimento(caminho)
            if self.comprimento(caminho) > 0
            else 0.0
        )
        for cam in caminho:
            atual = cam.getFeromonio()
            cam.setFeromonio(atual + novoFeromonio)

    # ---- Simulação de uma formiga (trajeto) ----
    def formiga(self) -> list:
        inicio = self.getInicio()
        fim = self.getFim()
        trajetoFormiga = []
        primeiros = []

        # pega todas as arestas que saem do nó inicial
        for c in self.getCaminhos():
            if c.possuiInicio(inicio):
                primeiros.append(c)

        primeiro = self.primeiraAresta(primeiros)
        if primeiro is None:
            return trajetoFormiga

        trajetoFormiga.append(primeiro)

        if primeiro.possuiFim(fim):
            self.marcaFeromonio(trajetoFormiga)
            return trajetoFormiga

        while True:
            umCaminho = trajetoFormiga[-1]
            proximo = self.escolheAresta(umCaminho)
            if proximo is None:
                break
            trajetoFormiga.append(proximo)
            if proximo.possuiFim(fim):
                break

        self.marcaFeromonio(trajetoFormiga)
        return trajetoFormiga

    # getters / setters no estilo Java
    def getCaminhos(self) -> list:
        return self.caminhos

    def setCaminhos(self, caminhos: list) -> None:
        self.caminhos = caminhos

    def getInicio(self) -> str:
        return self.inicio

    def setInicio(self, inicio: str) -> None:
        self.inicio = inicio

    def getFim(self) -> str:
        return self.fim

    def setFim(self, fim: str) -> None:
        self.fim = fim


# ================== "Teste.main" ==================
if __name__ == "__main__":
    colonia = ColoniaFormigas("A", "D")

    ab = Caminho("A", "B", 8, 1.0)
    ac = Caminho("A", "C", 14, 1.0)
    ad = Caminho("A", "D", 22, 1.0)
    bc = Caminho("B", "C", 9, 1.0)
    cb = Caminho("C", "B", 9, 1.0)
    bd = Caminho("B", "D", 8, 1.0)
    cd = Caminho("C", "D", 10, 1.0)

    # adjacências (saídas) conforme Java
    ab.addAdjacente(bc)
    ab.addAdjacente(bd)
    ac.addAdjacente(cb)
    ac.addAdjacente(cd)
    bc.addAdjacente(cd)
    cb.addAdjacente(bd)

    # registra caminhos na colônia
    colonia.addCaminho(ab)
    colonia.addCaminho(ac)
    colonia.addCaminho(ad)
    colonia.addCaminho(bc)
    colonia.addCaminho(cb)
    colonia.addCaminho(bd)
    colonia.addCaminho(cd)

    primeiraAresta = [ab, ac, ad]

    # Executa iterações: evapora e solta formigas
    formiga_trilhas = []
    for i in range(500):
        colonia.evaporaFeromonio(0.3)
        for j in range(5):
            formiga_trilhas.append(colonia.formiga())

    # Imprime as 500 primeiras trilhas (compatível com o Java)
    for i in range(500):
        trilha = formiga_trilhas[i]
        # imprime como "A-B: dist, ferom" etc.
        print(f"{i} - " + " -> ".join(str(c) for c in trilha))
