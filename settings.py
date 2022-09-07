import pygame


class Settings:
    def __init__(self, fullscreen=False):
        self.fullscreen = self.get_fullscreen()
        display = pygame.display.Info()
        if self.fullscreen or fullscreen:
            self.screen_width = display.current_w
            self.screen_height = display.current_h
        else:
            self.screen_width = 1500
            self.screen_height = 800
        base = 1000
        self.level_rect = pygame.Rect(-base, -base, base * 2, base * 2)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.fps = 60
        pygame.display.set_caption('Tin Knight - by Gabe U.')
        pygame.display.set_icon(pygame.image.load('assets/background/favicon.png'))
        self.clock = pygame.time.Clock()

    def get_fullscreen(self):
        output = ""
        try:
            with open('assets/settings.txt') as f:
                for line in f:
                    output += line.strip().replace(" ", "").lower()
        except:
            pass
        fullscreen = True if "fullscreen=true" in output else False
        return fullscreen

    def update_screen_dimensions(self, w, h):
        self.screen_width = w
        self.screen_height = h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.level_borders = (
            -w * 4,
            h * 4
        )

    def update_fps(self, fps):
        self.fps = fps

    def update_display_caption(self, title):
        pygame.display.set_caption(title)

    def get_clock(self):
        return self.clock

    def get_screen(self):
        return self.screen

    def get_screen_width(self):
        return self.screen_width

    def get_screen_height(self):
        return self.screen_height

    def get_fps(self):
        return self.fps
