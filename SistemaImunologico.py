import random
from copy import deepcopy
import matplotlib.pyplot as plt

class Antigeno:
    def __init__(self):
        # em Java: new ArrayList(121)
        self.um_antigeno = []
        self.add_line(0,0,0,0,0,0,0,0,0,0,0)
        self.add_line(0,0,0,1,1,1,1,1,0,0,0)
        self.add_line(0,0,1,0,0,0,0,0,1,0,0)
        self.add_line(0,0,1,0,0,0,0,0,1,0,0)
        self.add_line(0,0,1,0,0,0,0,0,1,0,0)
        self.add_line(0,0,0,1,1,1,1,1,0,0,0)
        self.add_line(0,0,1,0,0,0,0,0,1,0,0)
        self.add_line(0,0,1,0,0,0,0,0,1,0,0)
        self.add_line(0,0,1,0,0,0,0,0,1,0,0)
        self.add_line(0,0,0,1,1,1,1,1,0,0,0)
        self.add_line(0,0,0,0,0,0,0,0,0,0,0)

    def add_line(self, x1, x2, x3, x4, x5,
                 x6, x7, x8, x9, x10, x11):
        self.um_antigeno.append(x1)
        self.um_antigeno.append(x2)
        self.um_antigeno.append(x3)
        self.um_antigeno.append(x4)
        self.um_antigeno.append(x5)
        self.um_antigeno.append(x6)
        self.um_antigeno.append(x7)
        self.um_antigeno.append(x8)
        self.um_antigeno.append(x9)
        self.um_antigeno.append(x10)
        self.um_antigeno.append(x11)

    def __str__(self):
        nova_linha = 0
        ret = ""
        for i, v in enumerate(self.um_antigeno):
            if nova_linha >= 10:
                nova_linha = 0
                ret += str(v) + "\n"
            else:
                nova_linha += 1
                ret += str(v)
        return ret

    # getter
    def get_um_antigeno(self):
        return self.um_antigeno

class Anticorpo:
    def __init__(self):
        self.um_anticorpo = []
        for _ in range(121):
            # 0 ou 1
            valor = round(random.random())
            self.um_anticorpo.append(valor)
        self.afinidade = 0

    # para poder ordenar como no Comparable 
    def __lt__(self, other):
        return self.afinidade > other.afinidade  # inverte para ordenar decrescente

    def __str__(self):
        nova_linha = 0
        ret = ""
        ret += f"\nRanking: {self.afinidade}\n"
        for v in self.um_anticorpo:
            if nova_linha >= 10:
                nova_linha = 0
                ret += str(v) + "\n"
            else:
                nova_linha += 1
                ret += str(v)
        return ret

    # getters e setters
    def get_um_anticorpo(self):
        return self.um_anticorpo

    def get_afinidade(self):
        return self.afinidade

    def set_afinidade(self, valor):
        self.afinidade = valor

class SistemaImunologico:
    def __init__(self, tam_populacao):
        self.populacao = tam_populacao
        self.um_antigeno = Antigeno()
        self.anticorpos = self.cria_populacao()

    def cria_populacao(self, quantidade=None):
        if quantidade is None:
            quantidade = self.populacao
        temp_anticorpos = []
        for _ in range(quantidade):
            temp_anticorpos.append(Anticorpo())
        return temp_anticorpos

    def afinidades(self):
        for anticorpo in self.anticorpos:
            anticorpo.set_afinidade(
                self.fitness(self.um_antigeno.get_um_antigeno(),
                             anticorpo.get_um_anticorpo())
            )
        # ordenar decrescente de afinidade
        self.anticorpos.sort()
        return self.anticorpos

    def fitness(self, um_antigeno, um_anticorpo):
        afinidade = 0
        for a, b in zip(um_antigeno, um_anticorpo):
            if a == b:
                afinidade += 1
        return afinidade

    def melhores(self, melhores_lista, quantidade):
        lista_melhores = []
        for i in range(quantidade):
            lista_melhores.append(melhores_lista[i])
        return lista_melhores

    def clonagem(self, melhores, cl):
        clones = []
        total_afinidades = 0
        for m in melhores:
            total_afinidades += m.get_afinidade()

        for m in melhores:
            if total_afinidades == 0:
                clonagens = 1
            else:
                temp_afinidade = float(m.get_afinidade())
                total_clonagens = (temp_afinidade / total_afinidades) * cl
                clonagens = round(total_clonagens)

            cont = 0
            while cont < clonagens:
                clones.append(deepcopy(m))
                cont += 1

        return clones

    def hipermutacao(self, clones, fator):
        """
        Hipermutação proporcional à afinidade:
        - quanto MENOR a afinidade, MAIOR a taxa de mutação
        - taxaHip = (1 - (afinidade / 121)) * fator
        """
        antigeno = self.um_antigeno.get_um_antigeno()
        hipermutados = []

        for anticorpo in clones:
            # afinidade atual desse anticorpo com o antígeno da classe
            aff = self.fitness(antigeno, anticorpo.get_um_anticorpo())
            taxa_hip = (1 - (aff / 121)) * fator

            genes_orig = anticorpo.get_um_anticorpo()
            novos_genes = []

            for g in genes_orig:
                rand = random.random()
                if rand <= taxa_hip:
                    # inverte bit
                    if g == 0:
                        novos_genes.append(1)
                    else:
                        novos_genes.append(0)
                else:
                    novos_genes.append(g)

            # atualiza genes no próprio objeto
            anticorpo.um_anticorpo = novos_genes
            # recalcula afinidade após mutação
            anticorpo.set_afinidade(self.fitness(antigeno, novos_genes))

            hipermutados.append(anticorpo)

        # se quiser manter ordenado já aqui:
        hipermutados.sort()
        return hipermutados

    # getters e setters
    def get_populacao(self):
        return self.populacao

    def get_anticorpos(self):
        return self.anticorpos

    def set_anticorpos(self, nova_lista):
        self.anticorpos = nova_lista

    def get_um_antigeno(self):
        return self.um_antigeno


# ====== "Teste" ======
if __name__ == "__main__":
    si = SistemaImunologico(100)
    taxa_mutacao = 0.05
    cont = 0
    while cont < 200:
        populacao = si.afinidades()
        melhores = si.melhores(populacao, 15)
        clonagem = si.clonagem(melhores, 85)
        hipermutacao = si.hipermutacao(clonagem, taxa_mutacao)  # versão Python
        novos = si.get_populacao() - len(hipermutacao)
        print("Cont =", cont)
        #print("Anticorpo=", ag.get_anticorpos)
        # cria novos indivíduos para completar população
        novos_anticorpos = si.cria_populacao(novos)
        hipermutacao.extend(novos_anticorpos)
        si.set_anticorpos(hipermutacao)
        #ag.imprimeImagem()
        print(si.get_anticorpos()[1])
        cont += 1
