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
    def run(objetos):
        listaDeRemocao = {"players":[], "reward":[]}
        for i in range(len(objetos)):
            if type(objetos[i]).__name__ == "Player":
                colisoes = objetos[i].mob.collidelist([x.mob for x in objetos[:i] + objetos[i + 1:]])

                if colisoes != -1:
                    if type(objetos[colisoes]).__name__ == "Player":
                        #print("É um jogador")
                        pass
                    else:
                        objetos[i] + objetos[colisoes]
                        print(f"Colocando {objetos[colisoes].id}")
                        listaDeRemocao["reward"].insert(0, objetos[colisoes].id)

            objetos[i].desenhar(tela)

        return listaDeRemocao
    
    @staticmethod
    def distancias(lista):
        if len(lista) > 1:
            print(lista[0].calcularDistancia(lista[1].mob))

    @staticmethod
    def spawnPlayer(tela, lista, quantidade):
        for i in range(1, quantidade):
            lista.append(Player(tela, i))
    
    @staticmethod
    def spawnReward(tela, lista, quantidade, textos):
        for i in range(1, quantidade):
            lista.append(Reward(tela, i))
            textos.append(Texto(str(lista[-1].id), lista[-1].coords()))

    
    @staticmethod
    def criaCor():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Texto:
    def __init__(self, nome, posicao):
        fonte = pygame.font.SysFont('Comic Sans MS', 15)
        self.main = fonte.render(nome, False, (0, 0, 0))
        self.posicao = posicao


class Player(Mob):
    def __init__(self, tela, identificador, jogavel = False):
        super().__init__(identificador)
        self.player = jogavel
        self.cor = Engine.criaCor()

        tamanho = pygame.display.Info()
        self.mob = pygame.draw.circle(tela, self.cor, (random.randint(0, tamanho.current_w), random.randint(0, tamanho.current_h)), 10)

    def mover(self, key):
        if key[pygame.K_LEFT] and self.coords()[0] > 0:
           self.mob = self.mob.move(-2, 0)
        if key[pygame.K_RIGHT] and self.coords()[0] < pygame.display.Info().current_w:
           self.mob = self.mob.move(2, 0)
        if key[pygame.K_UP] and self.coords()[1] > 0:
           self.mob = self.mob.move(0, -2)
        if key[pygame.K_DOWN] and self.coords()[1] < pygame.display.Info().current_h:
           self.mob = self.mob.move(0, 2)

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, self.mob[:2], 10)

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

    def calcularDistancia(self, outro):
        return math.sqrt(math.pow(self.mob.x - outro.x, 2) + math.pow(self.mob.y - outro.y, 2))

    def coords(self):
        return self.mob.x, self.mob.y

class Reward:
    def __init__(self, tela, identificador):
        self.id = identificador
        if random.randint(0, 2) == 1:
            self.tipo = "Supply"
            self.recompensa = random.randint(1,3)
        else:
            self.tipo = "Xp"
            self.recompensa = random.randint(10, 100)
        self.cor = Engine.criaCor()

        tamanho = pygame.display.Info()
        self.mob = pygame.draw.rect(tela, self.cor, pygame.Rect(random.randint(0, tamanho.current_w), random.randint(0, tamanho.current_h), 5, 5))
    
    def receive(self):
        print(f"DEVOLVENDO {self.id}")
        return self.recompensa
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.mob, 5)
    def coords(self):
        return self.mob.x, self.mob.y

pygame.init()
pygame.display.set_caption("Evolução genética")

tela = pygame.display.set_mode((640, 480))
tela.fill(WHITE)

pygame.display.flip()

jogadores = [Player(tela, 0, True)]
premios = []
textos = []

tempo = pygame.time

jogando = True
cont = 0

Engine.spawnReward(tela, premios, 10, textos)
Engine.spawnPlayer(tela, jogadores, 10)

while jogando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
    
    jogadores[0].mover(pygame.key.get_pressed())
    remover = Engine.run(jogadores + premios)

    for i in remover['players']:
        for j in jogadores:
            if j.id == i:
                jogadores.remove(j)
                break
    
    for i in remover['reward']:
        print(f"Procurando {i}")
        for j in premios:
            if j.id == i:
                premios.remove(j)
                break
    
    for i in textos:
        tela.blit(i.main, i.posicao)

    pygame.display.flip()
    tela.fill(WHITE)

    tempo.delay(50)