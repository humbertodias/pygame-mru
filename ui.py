# coding: utf-8

"""
User Interface.
"""
__author__  = 'Humberto Lino'
__version__ = '1.0'

import pygame, sys, random

from image import *
from sound import *
from collision import *
from geometry import *
from physics import *

class COLOR:
    """
    Cores
    """
    WHITE = (255, 255, 255)
    """
    Branco
    """
    LIGHT_GREEN = (50, 205, 50)
    """
    Verde claro
    """
    DARK_GREEN = (34, 139, 34)
    """
    Verde escuro
    """
    LIGHT_BLUE = (176, 224, 250)
    """
    Azul claro
    """
    RED = (192, 0, 0)
    """
    Vermelho
    """
    BROWN = (101, 67, 33)
    """
    Marron
    """

    @staticmethod
    def random_color():
        """
        Gera cor aleatória.

        @rtype:   tuple
        @return:  cor(r,g,b).
        """

        reds = random.uniform(0, 255)
        greens = random.uniform(0, 255)
        blues = random.uniform(0, 255)
        return (reds, greens, blues)

class UI:
    """
    User Interface
    """
    def __init__(self, map, title, fator_escala, fps, fontSize=15):
        """
        Construtor.

        @param map: Mapa preenchido
        @param title: Título
        @param fator_escala: Fator Escala
        @param fps: Frames por Segundo
        @param fontSize: Tamanho da Fonte
        @return: Instância
        """
        self.fps_relogio = pygame.time.Clock()
        self.fps = fps
        self.fontSize = fontSize
        self.map = map
        self.fator_escala = fator_escala

        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(self.map.janela, 0, 32)

        self.dataDir = 'data/'
        self.imageManager = ImageManager(pygame, self.dataDir)
        self.soundManager = SoundManager(pygame, self.dataDir)
        self.paused = False
        self.reverted = False

        pygame.display.set_icon(self.imageManager.get('icon'))
        self.font = pygame.font.Font("data/fonts/dejavu.ttf", fontSize)
        # self.font = pygame.font.SysFont("arial", fontSize)
        self.font.set_bold(True)

    def tick(self):
        """
        Update
        """
        pygame.display.update()
        self.fps_relogio.tick(self.fps) 

    def desenhar_fundo(self, rect=None):
        """
        Desenhar fundo
        @param rect: Retângulo
        """
        self.screen.fill(COLOR.LIGHT_BLUE, rect)

    def desenhar_cenario(self):
        """
        Desenhar cenário
        """
        TELA_LARGURA, TELA_ALTURA = self.map.janela

        # fundo
        self.desenhar_fundo()

        # chao
        ORIGEM_Y = self.map.chao[1]
        PROJETIL_RADIUS = self.map.projetil.radius
        pygame.draw.rect(self.screen, COLOR.LIGHT_GREEN, (0, ORIGEM_Y + PROJETIL_RADIUS, TELA_LARGURA, ORIGEM_Y + PROJETIL_RADIUS + 6), 0)
        pygame.draw.rect(self.screen, COLOR.DARK_GREEN, (0, ORIGEM_Y + PROJETIL_RADIUS + 6, TELA_LARGURA,TELA_ALTURA), 0)

        # obstaculo
        pygame.draw.rect(self.screen, COLOR.BROWN, self.map.obstaculo.tuple(), 0)

        # alvo
        pygame.draw.circle(self.screen, COLOR.RED, self.map.alvo.pos.tuple(), self.map.alvo.radius)
        pygame.draw.circle(self.screen, COLOR.WHITE, self.map.alvo.pos.tuple() , 2)

    def desenhar_info_projetil_no_rodape(self, projetil):
        """
        Desenhar Informação do Projétil no Rodapé
        @param projetil: Projétil
        @return:
        """

        # desenha texto no rodapé
        ORIGEM_Y = self.map.chao[1] + projetil.circle.radius + 6
        text_height = 15
        xy_text = (0, ORIGEM_Y + text_height * projetil.id)
        text = "%s - Tempo (%.2f) Velocidade (%.2f) alvo %s  obstaculo %s  XY %s " % (projetil.id, projetil.t, projetil.v, projetil.alvo, projetil.obstaculo, projetil.circle.pos)
        rect = (xy_text[0],xy_text[1], self.map.janela[0], text_height)
        self.screen.fill(COLOR.DARK_GREEN, rect)
        self.write_text(text, xy_text )

    def desenhar_projetil(self, fatorEscala, projetil):
        """
        Desenhar Projétil
        @param fatorEscala: Fator escala
        @param projetil: Projétil
        @return:
        """
        xy = projetil.cartesiano_para_tela(fatorEscala)

        # desenha projetil
        pygame.draw.circle(self.screen, projetil.cor_borda, xy, projetil.circle.radius)
        pygame.draw.circle(self.screen, projetil.cor_fundo, xy, projetil.circle.radius - 2)

        # rotulo do projetil
        fix = self.fontSize/2
        xy_text = (xy[0]-fix, xy[1]-fix)
        self.write_text(projetil.id, xy_text )

        self.desenhar_info_projetil_no_rodape(projetil)

        c1 = Circle( Point(xy[0], xy[1]), projetil.circle.radius )

        if Collision.CircleCollidedWithCircle(c1, self.map.alvo) :
            self.soundManager.playSoundSingle('target')
            if projetil.alvo is None :
                self.mark(c1.pos)
                projetil.alvo = c1.pos

        if Collision.RectangleCollidedWithCircle(c1, self.map.obstaculo) :
            self.soundManager.playSound('obstacle')
            self.mark(c1.pos)
            projetil.obstaculo = c1.pos
            projetil.v = 0

        if projetil.quicou:
            self.soundManager.playSound('bounce')

        if self.projetil_fora_da_tela(projetil):
            projetil.v = 0


    def write_text(self, msg, pos):
        """
        Escreve mensagem na posição informada
        @param msg: Mensagem
        @param pos: Posição
        @return:
        """
        lines = str(msg).split('\n')
        for index, line in enumerate(lines):
            text=self.font.render(str(line), 1,COLOR.WHITE)
            self.screen.blit(text, (pos[0], pos[1] + index * self.fontSize) )

    def write_text_on_top(self, msg):
        """
        Escreve mensagem no canto superior da tela
        @param msg: Mensagem
        @return:
        """
        pos = (0,0)
        text=self.font.render(str(msg), 1,COLOR.WHITE)
        self.desenhar_fundo( (pos[0], pos[1], len(msg)*self.fontSize, self.fontSize) )
        self.screen.blit(text, pos)

    def mark(self, point):
        """
        Marcar coordenada na tela
        @param point: Ponto
        @return:
        """
        pos = point.tuple()
        msg = '(%s,%s)' % (pos[0], pos[1])
        self.write_text(msg , pos)

    def tiros_para_projeteis(self):
        """
        Converte Tiros em Projeteis
        @return: Projeteis
        """
        projeteis = []
        for id, tiro in enumerate(self.map.tiros):
            velocidade_inicial, angle = tiro
            projeteis.append( Projetil(id, self.map.projetil, float(velocidade_inicial), float(angle), cor_fundo=COLOR.random_color(), cor_borda=COLOR.random_color() ) )

        return projeteis

    def loop(self):
        """
        Repetição.

        @return:
        """

        projeteis = self.tiros_para_projeteis()

        self.desenhar_cenario()

        self.soundManager.playSound('shot')

        done = False
        while not done :

            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
            elif event.type == pygame.MOUSEBUTTONUP:

                if self.reverted:
                    self.revert(False)

            elif event.type == pygame.MOUSEBUTTONDOWN :
                button1, button2, button3 = pygame.mouse.get_pressed()

                if button1 :
                    self.revert(True)

                if button3:
                    self.pause()

            if not self.paused and not self.projeteis_parados(projeteis) :
                for projetil in projeteis:
                    projetil.calcular_movimento(self.fps, self.reverted)
                    self.desenhar_projetil(self.fator_escala, projetil)

            self.tick()

        return projeteis

    def pause(self, msg='PAUSED'):
        """
        Pausar.
        @param msg: Mensagem
        @return:
        """
        # invert
        self.paused = not self.paused

        if self.paused :
            self.write_text_on_top(msg)
        else:
            self.write_text_on_top(' '*len(msg))

    def revert(self, enabled, msg='REWINDING'):
        """
        Marcar Revert.
        @param enabled: Habilita/Desabilita
        @param msg: Mensagem
        @return:
        """

        self.reverted = enabled

        if enabled:
            self.write_text_on_top(msg)
        else:
            self.write_text_on_top(' '*len(msg))

    def projetil_fora_da_tela(self, projetil):
        """
        Projetil informado esta fora da tela?
        @param projetil: Projetil
        @return: True/False
        """
        x,y = projetil.cartesiano_para_tela(self.fator_escala)
        x -= projetil.circle.radius
        tela_max_x = self.map.janela[0]
        return x < 0 or x > tela_max_x

    def projeteis_parados(self, projeteis):
        """
        Todos os projéteis estam parados?
        @param projeteis: Lista de projeteis
        @return: True/False
        """
        for projetil in projeteis:
            if not projetil.parado() :
                return False
        return True

    def max_len(self, msg):
        """
        Maior comprimento encontrado na mensagem informada
        @param msg: Mensagem
        @return: max_len
        """
        ml = 0
        lines = msg.split('\n')
        for line in lines:
            ml = max( ml, len(line) )
        return ml

    def info_splash(self):
        """
        Informação Inicial
        @return:
        """

        self.soundManager.playMusic('background.mp3',-1)

        bg = self.imageManager.get('background')
        self.screen.blit(bg,(0,0))

        msg = """
        [Instruções]

        Voltar o tempo = Botão esquerdo do mouse
        Pausar = Botão direito
        ESQ = Sair"""


        w,h = self.map.janela
        max_len = self.max_len(msg)
        center = ( w/2 - max_len, h - 200 )

        done = False
        while not done :

            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN :
                button1, button2, button3 = pygame.mouse.get_pressed()
                done = True

            self.write_text(msg, center)

            # Called at the end after frame is ready!
            pygame.display.flip()

    def quit(self):
        """
        Sair.
        @return:
        """
        sys.exit()

