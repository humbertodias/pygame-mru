# coding: utf-8

"""
Manipula Arquivo.
"""
__author__  = 'Humberto Lino'
__version__ = '1.0'


import sys,os

from geometry import *

class FileManager:
    """
    Classe que gerencia arquivos.
    """
    def __init__(self, inFileName, outFileName):
        """
        Construtor.

        @param inFileName: nome do arquivo de entrada
        @param outFileName: nome do arquivo de saída
        @return: Instância de FileManager
        """
        self.inFileName = inFileName
        self.outFileName = outFileName
        self.fileFormat = {'janela': 2
                          ,'ponto_inicial': 1
                          ,'obstaculo': 3
                          ,'alvo': 3
                          ,'tiro': 2}

    def getFileFormat(self):
        """
        Obtém Formato do Arquivo.
        """
        return """
        janela largura altura
        ponto_inicial x
        obstaculo x altura largura
        alvo x y raio
        tiro velocidade angulo
        tiro velocidade angulo
        ...
        """

    def load(self, fileName, fileFormat, sep=' '):
        """
        Carregar arquivo
        @param fileName:  Nome do arquivo
        @param fileFormat: Formato do arquivo
        @param sep:  Separador
        @return: Mapa preenchido
        """

        if not os.path.exists(self.inFileName):
            raise RuntimeError('Arquivo %s não encontrado!\nCrie-o com o seguinte formato: %s' % (self.inFileName, self.getFileFormat() ))

        map = {}
        with open(fileName, 'r') as lines:
            for line in lines :
                key, values = line.split(sep,1)
                lvalues = values.strip().split(sep)
                if key in fileFormat:
                    if len(lvalues) == fileFormat[key]:
                        if key in map:
                            map[key] += [lvalues]
                        else:
                            map[key] = [lvalues]
                    else:
                        raise RuntimeError('Line with key [%s] must contains [%d] values' % (key,len(lvalues)))
        return map


    def read(self):
        """
        Ler arquivo.
        @return: POJO preenchido
        """
        print('Lendo arquivo [%s]' % self.inFileName)
        map = self.load(self.inFileName, self.fileFormat)
        janela = (int(map['janela'][0][0]), int(map['janela'][0][1]))
        chao = (0.0, float(janela[1]-100) )
        ponto_inicial = Point(float(map['ponto_inicial'][0][0]), chao[1])

        projetil = Circle(ponto_inicial, 10)

        # (x,y,width,height)
        obstaculo_altura  = int(map['obstaculo'][0][1])
        obstaculo_largura = int(map['obstaculo'][0][2])
        obstaculo_x = float(map['obstaculo'][0][0])
        obstaculo_y = ponto_inicial.y-(obstaculo_altura-projetil.radius)
        obstaculo = Rectangle( Point(obstaculo_x, obstaculo_y) , obstaculo_largura, obstaculo_altura)

        alvo_pos = Point(int(map['alvo'][0][0]), int(map['alvo'][0][1]))
        alvo = Circle( alvo_pos, int(map['alvo'][0][2]) )

        self.janela = janela
        self.chao = chao
        self.ponto_inicial = ponto_inicial
        self.projetil = projetil
        self.obstaculo = obstaculo
        self.alvo = alvo
        self.tiros = map['tiro']

        return self


    def write(self, projeteis):
        """
        Escreve arquivo de saída
        @param projeteis:  Projeteis
        @return: Nada
        """
        print('Escrevendo arquivo [%s]' % self.outFileName)

        with open(self.outFileName, 'w') as file:
            for projetil in projeteis:
                file.write('tiro [%d] v0(%s) time(%s) max %s alvo %s  obstaculo %s\r\n' % (projetil.id, projetil.v_zero, projetil.t, projetil.max, projetil.alvo, projetil.obstaculo ) )
