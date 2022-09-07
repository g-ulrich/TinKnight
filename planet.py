import pygame
from datetime import datetime
from asset_classes import PlanetAssets


class Planet(pygame.sprite.Sprite):
    def __init__(self, group, settings_obj, planet_assets):
        super().__init__(group)
        self.assets = planet_assets
        self.settings = settings_obj
        self.start_dt = datetime.now()
        self.planet_index = 1
        self.image = self.assets.planet['images'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = self.rect.topleft

        # heart
        self.health_points_threshold = 200 * 3
        self.current_health_points = 200 * 3
        self.planet_health_rect = pygame.Rect((self.settings.screen_width / 2) - (self.health_points_threshold / 2),
                                              self.settings.screen_height - 30,
                                              self.health_points_threshold, 20)

    def update_image(self):
        self.planet_index += .2
        try:
            self.image = self.assets.planet['images'][round(self.planet_index)]
        except:
            self.image = self.assets.planet['images'][0]
            self.planet_index = 0

    def update_to_half_damage(self):
        self.current_health_points = self.current_health_points // 2

    def update_to_max_health(self):
        self.current_health_points = self.health_points_threshold

    def update_planet_health(self, number_of_hits, score):
        if number_of_hits > 0:
            score.update_score(-(number_of_hits * 5))
            self.current_health_points -= number_of_hits * (self.health_points_threshold / 16)
        return True if self.current_health_points < 1 else False

    def blit_next_planet_image(self, surface, offset, internal_offset):
        self.update_image()
        self.rect.x
        offset = offset + internal_offset
        rect = self.rect
        surface.blit(self.image, rect.topleft - offset)
        self.pos = rect.topleft - offset

    def blit_health_bar(self, surface):
        rect = self.planet_health_rect
        offset = 5
        cool_down = self.current_health_points - offset + 1
        x, y, w, h = rect.x, rect.y, cool_down, rect.h
        limit = self.health_points_threshold - offset - 1
        # gray border
        pygame.draw.rect(surface, (127, 127, 127), pygame.Rect(x, y, limit, h), 2)
        # main
        pygame.draw.rect(surface, (67, 158, 95), pygame.Rect(x, y, w, h))
        # rounded light affect
        pygame.draw.rect(surface, (95, 161, 115), pygame.Rect(x, y, w, 10))
        # blit bolt image
        text = self.assets.bold_font.render(f"Planet HP {round(self.current_health_points)}", True, (255, 255, 255))
        surface.blit(text, (rect.centerx - (text.get_width() / 2), rect.centery - (text.get_height() / 2)))


class PlanetTitle(pygame.sprite.Sprite):
    def __init__(self, settings_obj, planet_assets):
        self.assets = planet_assets
        self.settings = settings_obj
        self.start_dt = datetime.now()
        self.planet_index = 1
        self.image = self.assets.planet['images'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = self.rect.topleft

        # heart
        self.health_points_threshold = 200 * 3
        self.current_health_points = 200 * 3
        self.planet_health_rect = pygame.Rect((self.settings.screen_width / 2) - (self.health_points_threshold / 2),
                                              self.settings.screen_height - 30,
                                              self.health_points_threshold, 20)

    def update_image(self):
        self.planet_index += .2
        try:
            self.image = self.assets.planet['images'][round(self.planet_index)]
        except:
            self.image = self.assets.planet['images'][0]
            self.planet_index = 0

    def update_to_half_damage(self):
        self.current_health_points = self.current_health_points // 2

    def update_to_max_health(self):
        self.current_health_points = self.health_points_threshold

    def update_planet_health(self, number_of_hits):
        if number_of_hits > 0:
            self.current_health_points -= number_of_hits * (self.health_points_threshold / 16)
        return True if self.current_health_points < 1 else False

    def blit_next_planet_image(self, surface):
        self.update_image()
        rect = self.rect
        rect.x = 100
        rect.y = 50
        surface.blit(self.image, rect)
        self.pos = (100, 100)

    def blit_health_bar(self, surface):
        rect = self.planet_health_rect
        offset = 5
        cool_down = self.current_health_points - offset + 1
        x, y, w, h = rect.x, rect.y, cool_down, rect.h
        limit = self.health_points_threshold - offset - 1
        # gray border
        pygame.draw.rect(surface, (127, 127, 127), pygame.Rect(x, y, limit, h), 2)
        # main
        pygame.draw.rect(surface, (67, 158, 95), pygame.Rect(x, y, w, h))
        # rounded light affect
        pygame.draw.rect(surface, (95, 161, 115), pygame.Rect(x, y, w, 10))
        # blit bolt image
        text = self.assets.bold_font.render(f"Planet HP {self.current_health_points}", True, (255, 255, 255))
        surface.blit(text, (rect.centerx - (text.get_width() / 2), rect.centery - (text.get_height() / 2)))
