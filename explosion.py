import pygame
from random import randint, choice


class Explosion:
    def __init__(self, settings_obj, width=100, radius=3, color=(0, -1, 0), iterate_by=0, sec_color=(0, -1, 0)):
        self.settings = settings_obj
        self.color = color
        self.iterate_by = iterate_by
        self.start = False
        self.width = width
        self.exp_index = -1
        self.center = pygame.math.Vector2()
        self.radius = radius
        self.second_color = self.color if sec_color == (0, -1, 0) else sec_color
        self.hit_box_rect = pygame.Rect(0, 0, 0, 0)

    def initiate(self, center_pos):
        self.center.x = center_pos[0]
        self.center.y = center_pos[1]
        self.start = True
        self.exp_index = 0

    def iterate(self, surface, offset=(0, 0)):
        if self.start:
            if self.width >= 1:
                complete_offset = self.center - offset
                self.radius += round(self.exp_index)
                self.width -= round(self.exp_index)
                if self.iterate_by == 0:
                    self.exp_index = self.exp_index + .08 if self.width > 3 else self.exp_index + .01
                else:
                    self.exp_index += self.iterate_by
                if self.color == (0, -1, 0):
                    pygame.draw.circle(surface, (randint(100, 255), 50, 50),
                                       self.center if offset != (0, 0) else complete_offset,
                                       self.radius, self.width)
                else:
                    color = choice([self.color, self.second_color])
                    pygame.draw.circle(surface, color, complete_offset, self.radius, self.width)
                self.hit_box_rect.x = complete_offset[0] - (self.radius / 2)
                self.hit_box_rect.y = complete_offset[1] - (self.radius / 2)
                self.hit_box_rect.w = self.radius
                self.hit_box_rect.h = self.radius
            elif self.width <= 0:
                self.start = False
                self.width = 100
                self.exp_index = 0
                self.center = pygame.math.Vector2()
                self.radius = 3
