# coding: utf-8

"""
Manipula Imagens.
"""
__author__  = 'Humberto Lino'
__version__ = '1.0'


import os

class ImageManager:
    """
    Gerenciador de Imagens
    """
    images = {}
    def __init__(self, pygame, dataDir = 'data/'):
        """
        Construtor.
        @param pygame: Referência do pygame
        @param dataDir: Diretório data
        @return: Instância
        """
        self.pygame = pygame
        self.imageDir = dataDir + 'image/'
        self.load()

    def load(self):
        """
        Carregar imagens.
        @return:
        """

        for file in os.listdir(self.imageDir):
            fileFullPath = os.path.join(self.imageDir, file)
            if os.path.isfile(fileFullPath):
                parts = file.split(".")
                fileName, extension = parts[0], parts[-1]
                self.add(fileName, extension)

    def add(self, imageName, extension):
        """
        Adiciona imagem.
        @param imageName: Nome
        @param extension: Extensão
        @return:
        """
        self.images[imageName] = self.pygame.image.load(self.imageDir + imageName + "." + extension)

    def get(self, imageName):
        """
        Obtém imagem.
        @param imageName: Nome
        @return: Imagem
        """
        return self.images[imageName]