from random import randint, choice

class Darwin:
    def __init__(self, objeto, valores, funcao, populacao = 10):
        self.objeto = objeto
        self.valores = valores
        self.funcao = funcao
        self.populacao = populacao

    def treinar(self, geracoes):
        for i in range(geracoes):
            print(f"Gen {i}: {''.join(self.objeto)}")
            objetos = [self.objeto] + [Darwin.genGenerator(self.objeto, self.valores) for x in range(self.populacao)]
            self.objeto = Darwin.naturalSelection(objetos, self.funcao)
            if self.funcao(self.objeto) == 100:
                break
        return self.objeto

    @staticmethod
    def genGenerator(atributos, valores):
        atributos = atributos[:]
        index = randint(0, len(atributos) - 1)
        atributos[index] = choice(valores)
        return atributos
    
    @staticmethod
    def naturalSelection(objetos, rankFunction):
        melhor, posicao = rankFunction(objetos[0]), 0
        for i in range(1, len(objetos)):
            calculo = rankFunction(objetos[i])
            if melhor < calculo:
                melhor, posicao = calculo, i
        return objetos[posicao]

def comparador(pivo):
    pontuacao = 0
    for i in range(len(pivo)):
        if pivo[i] == objetivo[i]:
            pontuacao += 1
    return pontuacao/len(objetivo) * 100

objetivo = 'prefiro morrer do que perder a vida'
valores = [chr(x) for x in range(ord('a'), ord('a') + 26)] + [' ']
aleatorio = [choice(valores) for x in range(len(objetivo))]

inteligencia = Darwin(aleatorio, valores, comparador)

print(''.join(inteligencia.treinar(10000)))
