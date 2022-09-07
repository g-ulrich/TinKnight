import pygame
from datetime import datetime
from spriteObject import SpriteSheet
from explosion import Explosion
from init_fonts import Font
import json
from random import randint, choice
from asset_classes import SpaceManAssets
from message import Message


class SpaceMan(pygame.sprite.Sprite):
    def __init__(self, settings_obj):
        self.message = Message()
        self.assets = SpaceManAssets()
        self.settings = settings_obj
        self.level_rect = self.settings.level_rect
        self.image_inc_dt = datetime.now()
        self.help_inc_dt = datetime.now()
        self.image = self.assets.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = randint(self.level_rect.topleft[0], self.level_rect.bottomright[1])
        self.rect.y = randint(self.level_rect.topleft[0], self.level_rect.bottomright[1])
        self.direction = pygame.math.Vector2(choice([(1, 0), (-1, 0), (0, 1), (0, -1)]))
        self.explosion = Explosion(settings_obj, color=(254, 254, 254))
        self.angle = 0
        self.image_index = 0
        self.hide_man_counter = 0
        self.man_saved_counter = 0
        self.points_for_saving = 100
        self.points_for_killing = -200
        self.spaceman_timer = datetime.now()

    def angle_increment(self):
        if self.angle == 360:
            self.angle = 0
        else:
            self.angle += 1

    def image_increment(self):
        if (datetime.now() - self.image_inc_dt).total_seconds() > .1:
            self.image_inc_dt = datetime.now()
            if self.image_index == 9:
                self.image_index = 0
            else:
                self.image_index += 1

    def hit_spaceman_or_save(self, surface, player_bullets, small_enemy, player_pos, offset, internal_offset):
        points = 0
        if self.hide_man_counter == 0:
            for pb in player_bullets:
                pb['rect'].x = pb['pos'][0]
                pb['rect'].y = pb['pos'][1]
                if self.rect.colliderect(pb['rect']):
                    self.explosion.initiate(pb['rect'].center)
                    for add_enemy in range(5):
                        small_enemy.add_new_enemy()
                    self.hide_man_counter = 60 * 2 # randint(60*2, 60*10)
                    self.message.init_message("", "NO BULLETS (5secs)!")
                    points = self.points_for_killing
                    self.rect.x = randint(self.level_rect.topleft[0] + 100, self.level_rect.bottomright[0] - 100)
                    self.rect.y = randint(self.level_rect.topleft[1] + 100, self.level_rect.bottomright[1] - 100)
                    break
            player_rect = pygame.Rect(player_pos[0], player_pos[1], 64, 64)
            man_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
            if man_rect.colliderect(player_rect):
                for add_enemy in range(2):
                    small_enemy.add_new_enemy()
                self.man_saved_counter = 60 * 2
                self.hide_man_counter = 60 * 2 # randint(60*2, 60*10)
                points = self.points_for_saving
                syn = ['MOMENTARY', 'TRIVIAL', 'ITSY BITSY', 'BLESSED', 'HOPEFUL']
                self.message.init_message("", f"{choice(syn)} PEACE!")
                self.rect.x = randint(self.level_rect.topleft[0] + 100, self.level_rect.bottomright[0] - 100)
                self.rect.y = randint(self.level_rect.topleft[1] + 100, self.level_rect.bottomright[1] - 100)
        else:
            if self.man_saved_counter == 0:
                self.explosion.iterate(surface, offset + internal_offset)
        return points

    def does_man_hit_wall(self):
        pr, lr = self.rect, self.level_rect
        speed = 1
        if pr.top < lr.top:
            self.direction = (0, speed)
            self.rect.x = randint(lr.topleft[0] + 100, lr.topright[0] - 100)
            self.rect.y += speed
        elif pr.left < lr.left:
            self.direction = (speed, 0)
            self.rect.x += speed
            self.rect.y = randint(lr.topleft[1] + 100, lr.bottomleft[1] - 100)
        elif pr.right > lr.right:
            self.direction = (-speed, 0)
            self.rect.x += -speed
            self.rect.y = randint(lr.topright[1] + 100, lr.bottomright[1] - 100)
        elif pr.bottom > lr.bottom:
            self.direction = (0, -speed)
            self.rect.x = randint(lr.bottomleft[0] + 100, lr.bottomright[0] - 100)
            self.rect.y += -speed
        else:
            self.rect.x += self.direction[0]
            self.rect.y += self.direction[1]
        return self.rect

    def blit_help_me_message(self, surface, pos, player_name):
        jump_int = 0

        rect = pos
        text = self.assets.mago_bold.render(f"{player_name} save me!", True, (100, 100, 100))
        # main box
        pygame.draw.rect(surface, (250, 250, 250), (rect.x + 10, rect.y - 35 + jump_int, text.get_width() + 20, 30))
        # shadow
        pygame.draw.rect(surface, (225, 225, 225), (rect.x + 10, rect.y - 35 + jump_int, text.get_width() + 20, 3))
        pygame.draw.rect(surface, (225, 225, 225), (rect.x + 10, rect.y - 35 + jump_int, 3, 30))
        pygame.draw.polygon(surface, (250, 250, 250), [(rect.x + 10, rect.y - 5 + jump_int),
                                                       (rect.x + 20, rect.y - 5 + jump_int),
                                                       (rect.x + 15, rect.y + jump_int)])

        surface.blit(text, (rect.x + 20, rect.y - 30 + jump_int))

    def blit_thank_you(self, surface, player_name):
        jump_int = 0
        text = self.assets.mago_bold.render(f"Thank you!", True, (100, 100, 100))
        rect = pygame.Rect(self.settings.screen_width / 2, self.settings.screen_height / 2, 64, 64)
        # main box
        pygame.draw.rect(surface, (250, 250, 250), (rect.x + 10, rect.y - 35 + jump_int, text.get_width() + 20, 30))
        # shadow
        pygame.draw.rect(surface, (225, 225, 225), (rect.x + 10, rect.y - 35 + jump_int, text.get_width() + 20, 3))
        pygame.draw.rect(surface, (225, 225, 225), (rect.x + 10, rect.y - 35 + jump_int, 3, 30))
        pygame.draw.polygon(surface, (250, 250, 250), [(rect.x + 10, rect.y - 5 + jump_int),
                                                       (rect.x + 20, rect.y - 5 + jump_int),
                                                       (rect.x + 15, rect.y + jump_int)])

        surface.blit(text, (rect.x + 20, rect.y - 30 + jump_int))

    def update(self, surface, offset, internal_offset, player_name):
        """
        increment rotation and iterate through sprite
        """
        self.message.iterate_message(surface)
        if self.man_saved_counter != 0:
            self.man_saved_counter = self.man_saved_counter - 1 if self.man_saved_counter >= 1 else 0
            # blit thank you message
            self.blit_thank_you(surface, player_name)
        if self.hide_man_counter == 0:
            self.angle_increment()
            self.image_increment()
            rect = self.does_man_hit_wall()
            self.blit_help_me_message(surface, rect.topleft - offset - internal_offset, player_name)
            self.image = self.assets.images[self.image_index]
            rotated = pygame.transform.rotate(self.image, self.angle)
            surface.blit(rotated, rect.topleft - offset - internal_offset)
        else:
            self.hide_man_counter = self.hide_man_counter - 1 if self.hide_man_counter >= 1 else 0


class SpaceManTitle(pygame.sprite.Sprite):
    def __init__(self, settings_obj):
        self.assets = SpaceManAssets()
        self.settings = settings_obj
        self.level_rect = self.settings.level_rect
        self.image_inc_dt = datetime.now()
        self.help_inc_dt = datetime.now()
        self.image = self.assets.images[0]
        self.rect = self.image.get_rect()
        self.screen = self.settings.screen
        self.rect.x = randint(-100, self.screen.get_width() + 100)
        self.rect.y = randint(-100, self.screen.get_height() + 100)
        self.direction = pygame.math.Vector2(choice([(0, 5), (0, -5)]))
        self.explosion = Explosion(settings_obj, color=(254, 254, 254))
        self.angle = 0
        self.image_index = 0
        self.hide_man_counter = 0
        self.man_saved_counter = 0
        self.points_for_saving = 100
        self.points_for_killing = -100

    def angle_increment(self):
        if self.angle == 360:
            self.angle = 0
        else:
            self.angle += 1

    def image_increment(self):
        if (datetime.now() - self.image_inc_dt).total_seconds() > .1:
            self.image_inc_dt = datetime.now()
            if self.image_index == 9:
                self.image_index = 0
            else:
                self.image_index += 1

    def hit_spaceman_or_save(self, surface, player_bullets, player_pos, offset, internal_offset):
        points = 0
        if self.hide_man_counter == 0:
            for pb in player_bullets:
                pb['rect'].x = pb['pos'][0]
                pb['rect'].y = pb['pos'][1]
                if self.rect.colliderect(pb['rect']):
                    self.explosion.initiate(pb['rect'].center)
                    self.hide_man_counter = 60 * 2
                    points = self.points_for_killing
                    break
            player_rect = pygame.Rect(player_pos[0], player_pos[1], 64, 64)
            man_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
            if man_rect.colliderect(player_rect):
                self.man_saved_counter = 60 * 2
                self.hide_man_counter = 60 * 2
                points = self.points_for_saving
        else:
            if self.man_saved_counter == 0:
                self.explosion.iterate(surface, offset + internal_offset)
        return points

    def does_man_hit_wall(self, surface):
        surface_rect = surface.get_rect()
        surface_rect.x -= 1000
        surface_rect.y -= 1000
        surface_rect.w += 1000
        surface_rect.h += 1000
        pr, lr = self.rect, surface_rect
        if pr.top < lr.top:
            self.direction = (0, 5)
            self.rect.x = randint(lr.topleft[0] + 100, lr.topright[0] - 100)
            self.rect.y += 5
        elif pr.left < lr.left:
            self.direction = (5, 0)
            self.rect.x += 5
            self.rect.y = randint(lr.topleft[1] + 100, lr.bottomleft[1] - 100)
        elif pr.right > lr.right:
            self.direction = (-5, 0)
            self.rect.x += -5
            self.rect.y = randint(lr.topright[1] + 100, lr.bottomright[1] - 100)
        elif pr.bottom > lr.bottom:
            self.direction = (0, -5)
            self.rect.x = randint(lr.bottomleft[0] + 100, lr.bottomright[0] - 100)
            self.rect.y += -5
        else:
            self.rect.x += self.direction[0]
            self.rect.y += self.direction[1]
        return self.rect

    def blit_help_me_message(self, surface, pos):
        jump_int = 0

        rect = pos
        # main box
        pygame.draw.rect(surface, (250, 250, 250), (rect.x + 10, rect.y - 35 + jump_int, 100, 30))
        # shadow
        pygame.draw.rect(surface, (225, 225, 225), (rect.x + 10, rect.y - 35 + jump_int, 100, 3))
        pygame.draw.rect(surface, (225, 225, 225), (rect.x + 10, rect.y - 35 + jump_int, 3, 30))
        pygame.draw.polygon(surface, (250, 250, 250), [(rect.x + 10, rect.y - 5 + jump_int),
                                                       (rect.x + 20, rect.y - 5 + jump_int),
                                                       (rect.x + 15, rect.y + jump_int)])
        text = self.assets.mago_bold.render(f"Save me!", True, (100, 100, 100))
        surface.blit(text, (rect.x + 20, rect.y - 30 + jump_int))

    def blit_thank_you(self, surface):
        jump_int = 0

        rect = pygame.Rect(self.settings.screen_width / 2, self.settings.screen_height / 2, 64, 64)
        # main box
        pygame.draw.rect(surface, (250, 250, 250), (rect.x + 10, rect.y - 35 + jump_int, 120, 30))
        # shadow
        pygame.draw.rect(surface, (225, 225, 225), (rect.x + 10, rect.y - 35 + jump_int, 120, 3))
        pygame.draw.rect(surface, (225, 225, 225), (rect.x + 10, rect.y - 35 + jump_int, 3, 30))
        pygame.draw.polygon(surface, (250, 250, 250), [(rect.x + 10, rect.y - 5 + jump_int),
                                                       (rect.x + 20, rect.y - 5 + jump_int),
                                                       (rect.x + 15, rect.y + jump_int)])
        text = self.assets.mago_bold.render(f"Thank you!", True, (100, 100, 100))
        surface.blit(text, (rect.x + 20, rect.y - 30 + jump_int))

    def update(self, surface):
        """
        increment rotation and iterate through sprite
        """
        if self.man_saved_counter != 0:
            self.man_saved_counter = self.man_saved_counter - 1 if self.man_saved_counter >= 1 else 0
            # blit thank you message
            self.blit_thank_you(surface)
        if self.hide_man_counter == 0:
            self.angle_increment()
            self.image_increment()
            rect = self.does_man_hit_wall(surface)
            self.blit_help_me_message(surface, rect)
            self.image = self.assets.images[self.image_index]
            rotated = pygame.transform.rotate(self.image, self.angle)
            surface.blit(rotated, rect)
        else:
            self.hide_man_counter = self.hide_man_counter - 1 if self.hide_man_counter >= 1 else 0
