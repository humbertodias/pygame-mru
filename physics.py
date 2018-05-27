# coding: utf-8

"""
Física.
"""
__author__  = 'Humberto Lino'
__version__ = '1.0'

import math
from geometry import *


ACELERACAO_GRAVIDADE = 9.80665
"""
Aceleração da Gravidade.\012
U{https://pt.wikipedia.org/wiki/Acelera%C3%A7%C3%A3o_da_gravidade}
"""

class Projetil:
    """
    Projétil
    """
    def __init__(self, id, circle, v_zero, angulo_graus, cor_borda, cor_fundo):
        """
        Construtor.

        @param id: Identificador
        @param circle: Circulo
        @param v_zero: Velocidade Incial
        @param angulo_graus: Ângulo
        @param cor_borda: Cor da Borda
        @param cor_fundo: Cor do Fundo
        @return: Instância
        """
        self.id = id
        self.circle = circle
        self.origem = self.circle.pos
        self.max = self.circle.pos
        self.x_zero = 0.0
        self.v_zero = v_zero
        self.v = v_zero
        self.angulo_graus = angulo_graus
        self.t = 0.0

        self.alvo = None
        self.obstaculo = None
        self.quicou = False

        # cores
        self.cor_borda = cor_borda
        self.cor_fundo = cor_fundo


    def calcular_movimento(self, fps, revert=False):
        """
        Calcular movimento (MRU e MRUV).

        @param fps: Frames por Segundo
        @param revert: Sentido (True/False)
        @return: Instância
        """
        angulo_rad = math.radians(self.angulo_graus)

        if revert:
            self.t -= (1/float(fps))
            if self.t < 0 :
                self.t = 0
        else:
            self.t += (1/float(fps))

        # print('id', self.id, 'fps', fps, 't', self.t)

        # MRU - Movimento Retilineo Uniformemente
        # s = s0 + v*t
        x = self.x_zero + self.v * math.cos(angulo_rad) * self.t

        # MRUV - Movimento Retilineo Uniformemente Variado
        # s = s0 + v0 * t - a * t^2/2

        y =  self.v * math.sin(angulo_rad) * self.t - (ACELERACAO_GRAVIDADE * self.t**2) / 2

        self.circle.pos = Point(x,y)
        self.max = Point( max(self.max.x,x) , max(self.max.y,y) )

        if self.tocouNoChao():
            self.quicar()
        else:
            self.quicou = False

        return self

    def tocouNoChao(self):
        """
        Tocou no Chão
        @return: True/False
        """
        return self.circle.pos.y <= 0.0 and self.t >= 0.0

    def parado(self):
        """
        Projétil Parado?
        @return: True/False
        """
        return self.v == 0

    def quicar(self, v = 0.6):
        """
        Quicar
        @param v: Velocidade
        @return:
        """
        # parar de quicar, mais natural
        if self.v <= 0.2:
            self.v = 0

        self.v *= v
        self.x_zero = self.circle.pos.x
        self.circle.pos.y, self.t = (0.0, 0.0)
        self.quicou = (self.v > 0)

    def cartesiano_para_tela(self,fatorEscala):
        """
        Retorna (x,y) na tela segundo o fator escala
        @param fatorEscala:
        @return: Posição (x,y)
        """
        x_tela = int(self.origem.x + fatorEscala * self.circle.pos.x)
        y_tela = int(self.origem.y - fatorEscala * self.circle.pos.y)
        return (x_tela, y_tela)


def aceleracao_corpo_superficie_terra(m, r):
    """
    Obtém aceleração de corpo na superfície terrestre.

    A = (G * m) / r ** 2\012\012

    Onde:\012
    A = aceleração da gravidade.\012
    m = massa do astro.\012
    r = distância do centro do objeto.\012
    G = constante universal da gravitação.\012

    @param m: Massa
    @param r: Raio
    @return: Aceleração
    """
    G = ACELERACAO_GRAVIDADE
    A = (G * m) / r ** 2
    return A
