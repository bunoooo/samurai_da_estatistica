import pygame
from scripts.Config import *


class MusicManager:
    def __init__(self):
        pygame.mixer.init()

        self.path = music_path

        self.path_animacao = music_path + "animacao/"

        self.musicas = {
            0 : self.path + "tutorial.mp3",
            1: self.path + "fase1.mp3",
            2: self.path + "fase2.mp3",
            3: self.path + "fase3.mp3",
            4: self.path + "fase4.mp3",
            5: self.path + "fase5.mp3",
            6: self.path + "fase6.mp3"
        }
        self.volume = 0.2

        

    def tocar_musica(self, fase_id):
        """Toca a música da fase correspondente"""
        if fase_id in self.musicas:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.musicas[fase_id])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)  # -1 = loop infinito
        else:
            print(f"[Aviso] Nenhuma música definida para a fase {fase_id}.")


    def animations_sounds(self, nome_som):
        self.volume_animacao = 0.3

        try:
            som = pygame.mixer.Sound(self.path_animacao + f"{nome_som}.wav")
            som.set_volume(self.volume_animacao)
            som.play()
        except pygame.error as e:
            print(f"[Erro ao carregar som '{nome_som}']: {e}")


    def parar(self):
        pygame.mixer.music.stop()

    def pausar(self):
        pygame.mixer.music.pause()

    def continuar(self):
        pygame.mixer.music.unpause()

    def ajustar_volume(self, novo_volume):
        """Ajusta o volume (0.0 a 1.0)"""
        self.volume = max(0.0, min(1.0, novo_volume))
        pygame.mixer.music.set_volume(self.volume)