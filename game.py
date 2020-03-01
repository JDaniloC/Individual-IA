import time
import random
import pygame

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
        for i in range(len(objetos)):
            colisoes = objetos[i].mob.collidelist([x.mob for x in objetos[:i] + objetos[i + 1:]])

            objetos[i].desenhar(tela)
    
    @staticmethod
    def spawnPlayer(tela, lista, quantidade):
        for i in range(1, quantidade):
            lista.append(Player(tela, i))
    
    @staticmethod
    def spawnReward(tela, lista, quantidade):
        for i in range(1, quantidade):
            lista.append(Reward(tela))
    
    @staticmethod
    def criaCor():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Player(Mob):
    def __init__(self, tela, identificador, jogavel = False):
        super().__init__(identificador)
        self.player = jogavel
        self.cor = Engine.criaCor()

        tamanho = pygame.display.Info()
        self.mob = pygame.draw.circle(tela, self.cor, (random.randint(0, tamanho.current_w), random.randint(0, tamanho.current_h)), 10)

    def mover(self, key):
        if key[pygame.K_LEFT]:
           self.mob = self.mob.move(-2, 0)
        if key[pygame.K_RIGHT]:
           self.mob = self.mob.move(2, 0)
        if key[pygame.K_UP]:
           self.mob = self.mob.move(0, -2)
        if key[pygame.K_DOWN]:
           self.mob = self.mob.move(0, 2)

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, self.mob[:2], 10)

class Reward():
    def __init__(self, tela):
        self.cor = Engine.criaCor()

        tamanho = pygame.display.Info()
        self.mob = pygame.draw.rect(tela, self.cor, pygame.Rect(random.randint(0, tamanho.current_w), random.randint(0, tamanho.current_h), 5, 5))
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.mob, 5)

pygame.init()
pygame.display.set_caption("Artificial Intelligence")

tela = pygame.display.set_mode((640, 480))
tela.fill(WHITE)

pygame.display.flip()

jogadores = [Player(tela, 0, True)]
premios = []

tempo = pygame.time

jogando = True
cont = 0

Engine.spawnReward(tela, premios, 10)
Engine.spawnPlayer(tela, jogadores, 10)

while jogando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False

    jogadores[0].mover(pygame.key.get_pressed())
    Engine.run(jogadores)
    
    pygame.display.flip()
    tela.fill(WHITE)

    tempo.delay(50)