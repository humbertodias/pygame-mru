# coding: utf-8

"""
Módulo Principal.
"""
__author__  = 'Humberto Lino'
__version__ = '1.0'

from file import *
from ui import *


def main():
    """
    Método principal
    """

    fileManager = FileManager('entrada.txt', 'saida.txt')

    # 1 - ler arquivo de entrada
    map = fileManager.read()

    # 2 - criar user interface
    ui = UI(map, title="SENAC - Lançamento de projétil sobre um obstáculo", fator_escala=0.5, fps=60)

    # 3 - informações
    ui.info_splash()

    # 4 - repetição
    projeteis = ui.loop()

    # 5 - escrever arquivo de saída
    fileManager.write(projeteis)

if __name__ == '__main__':
    main()