import random
from time import sleep

class Mob:
    def __init__(self, identificador):
        self.id = identificador
        self.vidaMax = 1
        self.sorte = 1

        self.vida = 1
        self.ataque = 1
        self.defesa = 0

        self.nivel = 1
        self.exp = 0
        self.resistencia = 3

    def __sub__(self, inimigo):
        codigo = 0

        if inimigo.ataque < self.defesa and self.resistencia > 0:
            #print('Contra-ataque')
            escolha = [False] + [True for x in range(self.sorte)]
            if random.choice(escolha):
                codigo = 1
            else:
                self.resistencia -= 1
        elif inimigo.ataque > self.defesa or self.resistencia == 0:
            #print(self.id, 'recebeu',inimigo.ataque-self.defesa, 'de dano!')
            self.vida -= inimigo.ataque - self.defesa if self.resistencia > 0 else inimigo.ataque
            self.resistencia = 3
            
        if self.vida <= 0:
            inimigo.exp += 100
            inimigo.up()
            #print(self.id, 'morreu.')
            codigo = 2
        
        return codigo

    def __add__(self, powerup):
        if powerup.tipo == 'Supply':
            tipo = random.choice(['vida', 'ataque', 'defesa', 'sorte'])
            if tipo == 'vida':     self.vida = (self.vida + powerup.receive()) if (self.vida + powerup.receive()) <= self.vidaMax else self.vidaMax
            elif tipo == 'ataque': self.ataque += powerup.receive()
            elif tipo == 'defesa': self.defesa += powerup.receive()
            else:                  self.sorte += 1
        else:
            self.exp += powerup.receive()
            if self.exp >= 100: self.up()
        ##print(self)

    def __str__(self):
        for i,o in self.__dict__.items():
            print(i+':',o)
        print()
        return ''
    
    def __del__(self):
        print(self.id,"morreu ao nível:", self.nivel, "ataque:", self.ataque, "defesa:", self.defesa)
    
    def up(self):
        self.exp -= 100
        self.nivel += 1
        self.vidaMax += 1
        self.ataque += 1
        self.defesa += 1

        if self.exp >= 100: self.up()
