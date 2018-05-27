# coding: utf-8

"""
Manipula Aúdio.
"""
__author__  = 'Humberto Lino'
__version__ = '1.0'

import os

class SoundManager:
    """
    Gerenciador de Sons
    """
    sounds = {}
    def __init__(self, pygame, dataDir = 'data/', ):
        """
        Construtor.
        @param pygame: Referência do pygame
        @param dataDir: Diretório data
        @return: Instância
        """
        self.pygame = pygame
        self.soundDir = dataDir + 'sound/'
        self.musicDir = dataDir + 'music/'
        self.load()

    def load(self):
        """
        Carregar arquivos.
        @return:
        """
        for file in os.listdir(self.soundDir):
            fileFullPath = os.path.join(self.soundDir, file)
            if os.path.isfile(fileFullPath):
                parts = file.split(".")
                fileName, extension = parts[0], parts[-1]
                self.add(fileName, extension)

    def add(self, soundName, extension):
        """
        Adicionar audio.
        @param soundName: Nome
        @param extension: Extensão
        @return:
        """
        self.sounds[soundName] = self.pygame.mixer.Sound(self.soundDir + soundName + "." + extension)

    def isPlaying(self):
        """
        Reproduzindo?
        @return: True/False
        """
        return self.pygame.mixer.get_busy()

    def playSoundSingle(self, name, times = 0):
        """
        Reproduzir Audio se não estiver ocupado.
        @param name: Nome
        @param times: Quantas vezes
        @return:
        """
        if not self.isPlaying():
            self.pygame.mixer.Sound.play(self.sounds[name], times)

    def playSound(self, name, times = 0):
        """
        Reproduzir audio.
        @param name: Nome
        @param times: Quantas vezes
        @return:
        """
        self.pygame.mixer.Sound.play(self.sounds[name], times)

    def playMusic(self, filename, times = 0):
        """
        Reproduzir Música.
        @param filename: Nome do arquivo
        @param times: Quantas vezes
        @return:
        """
        self.pygame.mixer.music.load(self.musicDir + filename)
        self.pygame.mixer.music.play(times)
