import pygame
import os
from random import choice
from init_fonts import Font


class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.master_volume = 1.0
        self.font = Font(15)
        # music
        self.all_music_paths = self.get_music_list()
        self.song = pygame.mixer.Sound(f"assets/sounds/music/{self.all_music_paths[0]}")
        self.song_name = self.select_random_song()
        self.music_volume = .05

        # explosion
        exp_path = choice(["assets/sounds/explosion/1.wav", "assets/sounds/explosion/2.wav"])
        self.explosion = pygame.mixer.Sound(exp_path)

        # menu
        self.menu_select = pygame.mixer.Sound("assets/sounds/menu_select.wav")

        # start game
        self.start_game = pygame.mixer.Sound("assets/sounds/game_start.wav")

        #game over
        self.game_over = pygame.mixer.Sound("assets/sounds/game_over_power_down.wav")

    def play_explosion(self):
        self.explosion.play()

    def stop_explosion(self):
        self.explosion.stop()

    def play_menu_select(self):
        self.menu_select.set_volume(.3)
        self.menu_select.play()

    def stop_menu_select(self):
        self.menu_select.stop()

    def play_game_over(self):
        self.game_over.set_volume(.3)
        self.game_over.play()

    def stop_game_over(self):
        self.game_over.stop()

    def play_start_game(self):
        self.start_game.set_volume(.1)
        self.start_game.play()

    def get_music_list(self):
        return os.listdir("assets/sounds/music")

    def select_random_song(self):
        pick = choice(self.all_music_paths)
        self.song = pygame.mixer.Sound(f"assets/sounds/music/{pick}")
        return pick.replace(".wav", "")

    def blit_song_name(self, surface):
        text = self.font.mago_bold.render("Press (TAB) to skip song.", True, (127, 127, 127))
        surface.blit(text, (10, surface.get_height() - 10 - (text.get_height() * 2)))
        text = self.font.mago_bold.render(f"{self.song_name}", True, (127, 127, 127))
        surface.blit(text, (10, surface.get_height() - 10 - text.get_height()))

    def play_music(self):
        self.song.set_volume(self.music_volume)
        self.song.play(-1)

    def skip_song(self):
        self.song.fadeout(500)
        self.song_name = self.select_random_song()
        self.play_music()

    def stop_music(self):
        self.song.fadeout(1000)
