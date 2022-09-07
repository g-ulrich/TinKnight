import pygame
FONTS_PATH = "assets/fonts"


class Font:
    def __init__(self, size=15):
        self.san_bold = pygame.font.Font('freesansbold.ttf', size)
        self.squares = pygame.font.Font(f'{FONTS_PATH}/Squares.ttf', size)
        # icons included with 1 and 3
        # heart1 - U+005E
        # heart2 - U+005F
        # twitter - U+0060
        # patreon - U007B
        # facebook - U007C
        # twitch - U007D
        # smile1 - U007E
        # smile2 - U00A1
        # smile3 - U00A2
        # pacghost - U00A3
        # bob - U00A4
        # skull - U20A0
        self.mago_light = pygame.font.Font(f'{FONTS_PATH}/mago1.ttf', size)
        self.mago_normal = pygame.font.Font(f'{FONTS_PATH}/mago2.ttf', size)
        self.mago_bold = pygame.font.Font(f'{FONTS_PATH}/mago3.ttf', size)
