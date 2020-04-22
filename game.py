import time, random, pygame, math

from classes import *

# definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Engine:
    @staticmethod
    def run(tela, jogadores, listaDeXp, listaDePower, end):
        objetos = jogadores + listaDeXp + listaDePower
        listaDeRemocao = {"players":[], "reward":[]}
        for i in range(len(objetos)):
            if type(objetos[i]).__name__ == "Player" and objetos[i].id not in listaDeRemocao['players']:
                if objetos[i].id != -1:
                    if end:
                        print("SuddenDeath")
                        objetos[i].seguir([x for x in jogadores if x != objetos[i]][0])
                    else:
                        objetos[i].pensar(listaDeXp, listaDePower, jogadores)
                colisoes = objetos[i].mob.collidelist([objetos[x].mob for x in range(len(objetos)) if x != i])

                if colisoes != -1:
                    if colisoes >= i: colisoes += 1
                    if type(objetos[colisoes]).__name__ == "Player":
                        ataque = objetos[colisoes] - objetos[i]
                        if ataque == 1:
                            objetos[i] - objetos[colisoes]
                        elif ataque == 2:
                            listaDeRemocao['players'].insert(0, objetos[colisoes].id)
                    else:
                        objetos[i] + objetos[colisoes]
                        listaDeRemocao["reward"].insert(0, objetos[colisoes].id)

            objetos[i].desenhar(tela)

        return listaDeRemocao

    @staticmethod
    def spawnPlayer(tela, lista, comportamentos, quantidade):
        for i in range(quantidade):
            lista.append(Player(tela, i, comportamentos[i]))
    
    @staticmethod
    def spawnReward(tela, listaDeXp, listaDePower, quantidade):
        for i in range(1, quantidade):
            listaDeXp.append(Xp(tela, i))
            listaDePower.append(PowerUp(tela, i * -1))
            
    @staticmethod
    def criaCor():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def randomPlace():
        tamanho = pygame.display.Info()
        return random.randint(0, tamanho.current_w), random.randint(0, tamanho.current_h)

def criaTexto(nome):
    fonte = pygame.font.SysFont('Comic Sans MS', 15)
    fonte.set_bold(True)
    return fonte.render(str(nome), False, (255, 255, 255))


class Player(Mob):
    def __init__(self, tela, identificador, comportamentos = [[1 for x in range(8)] for x in range(4)]):
        super().__init__(identificador)
        self.comportamentos = comportamentos
        self.cor = Engine.criaCor()
        self.tela = tela

        self.mob = pygame.draw.circle(tela, self.cor, Engine.randomPlace(), 10)
        self.fonte = criaTexto(identificador)

    def mover(self, key):
        if key[pygame.K_LEFT] and self.coords()[0] > 0:
           self.mob = self.mob.move(-2, 0)
        if key[pygame.K_RIGHT] and self.coords()[0] < pygame.display.Info().current_w:
           self.mob = self.mob.move(2, 0)
        if key[pygame.K_UP] and self.coords()[1] > 0:
           self.mob = self.mob.move(0, -2)
        if key[pygame.K_DOWN] and self.coords()[1] < pygame.display.Info().current_h:
           self.mob = self.mob.move(0, 2)

    def seguir(self, outro):
        outroX, outroY = outro.coords()
        x, y = self.coords()
        key = { pygame.K_RIGHT: False,
                pygame.K_LEFT: False,
                pygame.K_UP: False,
                pygame.K_DOWN: False
              }

        if outroX > x:
            key[pygame.K_RIGHT] = True
        elif outroX < x:
            key[pygame.K_LEFT] = True
        if outroY > y:
            key[pygame.K_DOWN] = True
        elif outroY < y:
            key[pygame.K_UP] = True
        self.mover(key)
    
    def fugir(self, outro):
        outroX, outroY = outro.coords()
        x, y = self.coords()
        key = {pygame.K_RIGHT: False,
                pygame.K_LEFT: False,
                pygame.K_UP: False,
                pygame.K_DOWN: False}
        if outroX <= x and x < pygame.display.Info().current_w:
            key[pygame.K_RIGHT] = True
        elif outroX >= x and x > 0:
            key[pygame.K_LEFT] = True
        if outroY <= y and y < pygame.display.Info().current_h:
            key[pygame.K_DOWN] = True
        elif outroY >= y and y > 0:
            key[pygame.K_UP] = True
        self.mover(key)

    def pensar(self, listaDeXp, listaDePower, listaDePlayers):
        # A maior distância possível no mapa
        maiorDist = math.sqrt((
            math.pow(pygame.display.Info().current_w, 2) + 
            math.pow(pygame.display.Info().current_h, 2)
        ))

        #
        xp = min(listaDeXp, key = lambda x: self.calcularDistancia(x)) if listaDeXp != [] else maiorDist 
        power = min(listaDePower, key = lambda x: self.calcularDistancia(x)) if listaDePower != [] else maiorDist
        player = min(listaDePlayers, key = lambda x: self.calcularDistancia(x) if x.id != self.id else float("inf")) if listaDePlayers != [] else maiorDist

        # Atributos
        atributos = (
            [self.nivel, self.ataque, self.defesa] + 
            [self.vida/self.vidaMax*100, self.exp] + 
            [(1 - (x/maiorDist)) * 100 for x in 
                [self.calcularDistancia(xp) if type(xp) != float else xp, 
                self.calcularDistancia(power) if type(power) != float else power, 
                self.calcularDistancia(player) if type(player) != float else player]
            ]
        )
        
        resultado = {"enemy":0, "xp":0, "power":0, "run":0}
        keys = ['enemy', 'xp', 'power', 'run']

        # Média aritimética entre as médias ponderadas
        for i in range(4):
            resultado[keys[i]] = (
            self.mediaPonderada(atributos[:3], self.comportamentos[i][:3]) + 
            self.mediaPonderada(atributos[3:], self.comportamentos[i][3:])
            ) / 2
        
        maior = max(resultado, key = lambda x: resultado[x])
        if not self.escolherAcaso(maior, player, xp, power):
            random.shuffle(keys)
            for i in range(4):
                if self.escolherAcaso(keys[i], player, xp, power):
                    break

    def escolherAcaso(self, escolha, player, xp, power):
        if escolha == "enemy" and type(player) != float:
            self.cor = (255, 0, 0)
            self.seguir(player)
        elif escolha == "xp" and type(xp) != float:
            self.cor = (255, 255, 0)
            self.seguir(xp)
        elif escolha == "power" and type(power) != float:
            self.cor = (0, 0, 255)
            self.seguir(power)
        elif escolha == 'run' and type(player) != float:
            self.cor = (0, 0, 0)
            self.fugir(player)
        else:
            return False
        return True

    def mediaPonderada(self, lista, comportamentos):
        resultado = 0
        for x in range(len(lista)):
            resultado += lista[x] * comportamentos[x]
        return resultado/sum(comportamentos) if sum(comportamentos) > 0 else resultado

    def calcularDistancia(self, outro):
        return math.sqrt(math.pow(self.mob.x - outro.coords()[0], 2) + math.pow(self.mob.y - outro.coords()[1], 2))
    def coords(self):
        return self.mob.x, self.mob.y
    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, self.mob[:2], 10)
        self.tela.blit(self.fonte, (self.mob[0] - 4, self.mob[1] - 11))

class Reward:
    def __init__(self, tela, identificador):
        self.id = identificador
        self.cor = (255, 0, 0) if self.tipo == "Supply" else (255, 255, 0)

        tamanho = pygame.display.Info()
        self.mob = pygame.draw.rect(tela, self.cor, pygame.Rect(Engine.randomPlace(), (5, 5)))
    
    def receive(self):
        return self.recompensa
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.mob, 5)
    def coords(self):
        return self.mob.x, self.mob.y

class Xp(Reward):
    def __init__(self, tela, identificador):
        self.tipo = "Xp"
        self.recompensa = random.randint(10, 100)
        super().__init__(tela, identificador)

class PowerUp(Reward):
    def __init__(self, tela, identificador):
        self.tipo = "Supply"
        self.recompensa = random.randint(1,3)
        super().__init__(tela, identificador)

class Game:
    def __init__(self, comportamentos, quantidade):
        pygame.init()
        pygame.display.set_caption("Evolução genética")

        tela = pygame.display.set_mode((640, 480))
        tela.fill(WHITE)

        tempo = pygame.time
        pygame.display.flip()

        jogando = True
        suddenDeath = 1000
        velocidade = 120

        jogadores, listaDeXp, listaDePower = [], [], []

        Engine.spawnReward(tela, listaDeXp, listaDePower, quantidade*3)
        textos = Engine.spawnPlayer(tela, jogadores, comportamentos, quantidade)

        while jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jogando = False
                
                tecla = pygame.key.get_pressed()
                if tecla[pygame.K_EQUALS]:
                    velocidade -= 10
                elif tecla[pygame.K_MINUS]:
                    velocidade += 10
                elif tecla[pygame.K_p]:
                    suddenDeath = 0
            
            #jogadores[0].mover(pygame.key.get_pressed())

            remover = Engine.run(tela, jogadores, listaDeXp, listaDePower, suddenDeath <= 0)

            for i in remover['players']:
                for j in jogadores:
                    if j.id == i:
                        suddenDeath = 1000
                        jogadores.remove(j)
                        del j
                        break

            for i in remover['reward']:
                ver = False
                cont = 0
                while not ver and (cont < len(listaDeXp) or cont < len(listaDePower)):
                    if cont < len(listaDePower) and listaDePower[cont].id == i:
                        listaDePower.pop(cont)
                        ver = True
                    elif cont < len(listaDeXp) and listaDeXp[cont].id == i:
                        listaDeXp.pop(cont)
                        ver = True
                    cont += 1

            pygame.display.flip()
            tela.fill(WHITE)

            tempo.delay(velocidade)

            if suddenDeath < -500:
                print("HOLLY SUDDENDEATHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
                jogadores = jogadores[1:]

            if len(jogadores) <= 1:
                jogando = False
            
            suddenDeath -= 1
        
        self.ganhador = jogadores[0]

    def getGanhador(self): return self.ganhador.comportamentos

def transform(string):
    lista = [x[1:].split(', ') for x in string[1:len(string) - 1].split("], ")]
    lista[3][7] = lista[3][7][:len(lista[3][7]) - 1]
    return [list(map(int, x)) for x in lista]

def battleRoyal():
    oponentes = []
    pontuacao = {}
    for i in range(int(input("Quantos oponentes: "))):
        caracteristica = transform(input())
        oponentes.append(caracteristica)
        pontuacao[str(caracteristica)] = 0
    
    for i in range(int(input("Quantas rodadas: "))):
        ganhador = Game(oponentes, len(oponentes)).getGanhador()
        pontuacao[str(ganhador)] += 1

    print("\n")
    for i, j in pontuacao.items():
        print(j, ":", i)

    print("Ganhador: ", max(pontuacao, key = lambda x: pontuacao[x]), sep='\n')
        

battleRoyal()
'''print(Game([
    [[6, 1, 8, 3, 10, 1, 4, 4], [4, 1, 3, 1, 1, 8, 1, 3], [4, 1, 5, 6, 10, 6, 9, 1], [8, 6, 5, 5, 8, 5, 1, 1]], 
    [[1, 5, 7, 3, 1, 3, 9, 5], [1, 0, 4, 8, 5, 0, 9, 8], [5, 10, 4, 2, 0, 6, 1, 7], [5, 2, 8, 3, 2, 1, 1, 5]]
    ], 2).getGanhador())'''
