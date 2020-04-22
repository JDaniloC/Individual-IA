from random import randint, choice
from game import Game

class Darwin:
    def __init__(self, objeto, valores, populacao = 10):
        self.objeto = objeto
        self.valores = valores
        self.populacao = populacao

    def treinar(self, geracoes):
        for i in range(geracoes):
            print(f"Gen {i}: {self.objeto}")
            objetos = [self.objeto] + [Darwin.genGenerator(self.objeto, self.valores) for x in range(self.populacao)]
            self.objeto = Game(objetos, len(objetos)).getGanhador()
        return self.objeto

    @staticmethod
    def genGenerator(objeto, valores):
        objeto = [x[:] for x in objeto]
        index = randint(0, len(objeto) - 1)
        indice = randint(0, len(objeto[0]) - 1)
        objeto[index][indice] = choice(valores)
        return objeto
    
    @staticmethod
    def naturalSelection(objetos, rankFunction):
        melhor, posicao = rankFunction(objetos[0]), 0
        for i in range(1, len(objetos)):
            calculo = rankFunction(objetos[i])
            if melhor < calculo:
                melhor, posicao = calculo, i
        return objetos[posicao]

inteligencia = Darwin([[1 for x in range(8)] for x in range(4)], [x for x in range(11)], 19)

print(inteligencia.treinar(10))
