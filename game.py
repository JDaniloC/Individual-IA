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
    def run(tela, jogadores, listaDeXp, listaDePower):
        objetos = jogadores + listaDeXp + listaDePower
        listaDeRemocao = {"players":[], "reward":[]}
        for i in range(len(objetos)):
            if type(objetos[i]).__name__ == "Player" and objetos[i].id not in listaDeRemocao['players']:
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

class Texto:
    def __init__(self, nome, posicao):
        fonte = pygame.font.SysFont('Comic Sans MS', 15)
        self.main = fonte.render(nome, False, (0, 0, 0))
        self.posicao = posicao


class Player(Mob):
    def __init__(self, tela, identificador, comportamentos = [[1 for x in range(8)] for x in range(4)]):
        super().__init__(identificador)
        self.comportamentos = comportamentos
        self.cor = Engine.criaCor()

        self.mob = pygame.draw.circle(tela, self.cor, Engine.randomPlace(), 10)

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
        # Calcula os mais próximos
        maiorDist = math.sqrt((math.pow(pygame.display.Info().current_w, 2) + math.pow(pygame.display.Info().current_h, 2)))
        xp = self.calcularDistancia(min(listaDeXp, key = lambda x: self.calcularDistancia(x))) if listaDeXp != [] else maiorDist 
        power = self.calcularDistancia(min(listaDePower, key = lambda x: self.calcularDistancia(x))) if listaDePower != [] else maiorDist
        player = self.calcularDistancia(min(listaDePlayers, key = lambda x: self.calcularDistancia(x) if x.id != self.id else float("inf"))) if listaDePlayers != [] else maiorDist
        
        # Calcula essa média aritimética 
        atributos = [self.nivel, self.ataque, self.defesa] + [self.vida/self.vidaMax*100, self.exp] + [(1 - (x/maiorDist)) * 100 for x in [xp, power, player]]
        
        resultado = {"enemy":0, "xp":0, "power":0, "run":0} # Seguir inimigo, seguir xp, seguir power, fugir inimigo
        for i in range(4):
            resultado[i] = (self.mediaPonderada(atributos[:3], self.comportamentos[i][:3]) + self.mediaPonderada(atributos[3:], self.comportamentos[i][:3])) / 2
        maior = max(resultado, key = lambda x: resultado[x])
        if maior == "enemy":
            self.seguir(player)
        elif maior == "xp":
            self.seguir(xp)
        elif maior == "power":
            self.seguir(power)
        else:
            self.fugir(player)

    def mediaPonderada(self, lista, comportamentos):
        resultado = 0
        for x in range(len(lista)):
            resultado += lista[x] * comportamentos[x]
        return resultado/sum(comportamentos)

    def calcularDistancia(self, outro):
        return math.sqrt(math.pow(self.mob.x - outro.coords()[0], 2) + math.pow(self.mob.y - outro.coords()[1], 2))
    def coords(self):
        return self.mob.x, self.mob.y
    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, self.mob[:2], 10)

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

        pygame.display.flip()

        jogadores = []
        listaDeXp, listaDePower = [], []

        tempo = pygame.time

        jogando = True
        cont = 0

        Engine.spawnReward(tela, listaDeXp, listaDePower, quantidade)
        textos = Engine.spawnPlayer(tela, jogadores, comportamentos, quantidade)

        while jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jogando = False
            
            #jogadores[0].mover(pygame.key.get_pressed())
            remover = Engine.run(tela, jogadores, listaDeXp, listaDePower)

            for i in remover['players']:
                for j in jogadores:
                    if j.id == i:
                        jogadores.remove(j)
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

            tempo.delay(40)

            if len(jogadores) <= 1:
                jogando = False
        
        self.ganhador = jogadores[0]

    def getGanhador(self): return self.ganhador.comportamentos

#print(Game().getGanhador())
