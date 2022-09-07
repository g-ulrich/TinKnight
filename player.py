import pygame
from datetime import datetime
from explosion import Explosion
from random import randint
from asset_classes import PlayerAssets


class Player(pygame.sprite.Sprite):
    def __init__(self, settings_obj, group):
        super().__init__(group)
        self.assets = PlayerAssets()
        self.settings = settings_obj
        self.screen = settings_obj.screen
        self.start_dt = datetime.now()
        pos = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.explosion = Explosion(self.settings)
        self.explosion_planet = Explosion(self.settings, color=(255, 255, 255))
        self.explosion_mine = Explosion(self.settings, width=20, radius=1, color=(200, 255, 200))
        self.last_bullet_planet_impact_pos = (0, 0)

        self.image = self.assets.north[0]
        self.rect = self.image.get_rect(center=pos)
        self.speed = 5
        self.boost_speed = 10
        self.current_speed = self.speed

        self.direction = pygame.math.Vector2()
        # set movement north
        self.direction.y = -1
        self.previous_move = ""
        self.current_move = ""
        self.is_zoom = False
        self.zoom_cool_down = 0
        self.pressed = []
        # pixel width on screen and amount of ticks the player can zoom
        self.zoom_threshold = 200 * 2

        # player health
        self.health_points_threshold = 200 * 2
        self.current_health_points = 200 * 2
        # player zoom
        self.path = []
        self.path_append = self.path.append
        self.path_tick_limit = 100
        # mini map
        self.map_offset = 10

        # weapons
        self.shoot = False
        self.weapon_color = (0, 255, 21)
        self.boom = []
        self.boom_append = self.boom.append
        self.last_shot_dt = datetime.now()
        self.bullet_width = 3
        self.bullet_height = 11
        self.bullet_we_mask = pygame.mask.from_surface(pygame.Surface((self.bullet_height, self.bullet_width)))
        self.bullet_ns_mask = pygame.mask.from_surface(pygame.Surface((self.bullet_width, self.bullet_height)))

    def update_bullets(self, width, height):
        self.bullet_width = width
        self.bullet_height = height
        self.bullet_we_mask = pygame.mask.from_surface(pygame.Surface((self.bullet_height, self.bullet_width)))
        self.bullet_ns_mask = pygame.mask.from_surface(pygame.Surface((self.bullet_width, self.bullet_height)))

    def update_to_max_health(self):
        self.current_health_points = self.health_points_threshold

    def update_to_half_health(self):
        self.current_health_points = self.current_health_points // 2

    def update_health_neg_5(self):
        self.current_health_points -= 5

    def update_to_max_zoom(self):
        self.zoom_cool_down = self.zoom_threshold

    def update_to_half_zoom(self):
        self.zoom_cool_down = self.zoom_cool_down // 2

    def is_current_equal_previous_move(self):
        return True if self.current_move == self.previous_move else False

    def update_move_sprite(self):
        self.sprite_index = 0
        if self.current_move == "west":
            self.image = self.assets.west[self.sprite_index]
        elif self.current_move == "east":
            self.image = self.assets.east[self.sprite_index]
        elif self.current_move == "south":
            self.image = self.assets.south[self.sprite_index]
        elif self.current_move == "north":
            self.image = self.assets.north[self.sprite_index]

    def update_zoom_sprite(self):
        self.sprite_index = 1
        if self.current_move == "west":
            self.image = self.assets.west_boost[self.sprite_index]
        elif self.current_move == "east":
            self.image = self.assets.east_boost[self.sprite_index]
        elif self.current_move == "south":
            self.image = self.assets.south_boost[self.sprite_index]
        elif self.current_move == "north":
            self.image = self.assets.north_boost[self.sprite_index]

    def check_zoom(self, zoom):
        if not zoom:
            if 0 <= self.zoom_cool_down <= self.zoom_threshold:
                # self.assets.stop_zoom_sound(500)
                self.boost_speed = self.speed
                self.zoom_cool_down += 1
        if zoom and self.zoom_cool_down > 5:
            # self.assets.play_zoom_sound()
            self.update_zoom_sprite()
            self.zoom_cool_down -= 1
            self.is_zoom = True
            if self.zoom_cool_down <= 5:
                # self.assets.stop_zoom_sound(500)
                self.is_zoom = False
                self.speed = self.speed
                self.update_move_sprite()
            else:
                self.update_zoom_sprite()
                self.speed = 10
            if self.previous_move == "west":
                self.direction.x = -1
            elif self.previous_move == "east":
                self.direction.x = 1
            elif self.previous_move == "north":
                self.direction.y = -1
            elif self.previous_move == "south":
                self.direction.y = 1
        if not zoom or not self.is_zoom:
            self.update_move_sprite()

    def input(self, controls):
        self.pressed = controls['pressed']
        self.speed = 2
        if controls['left']:
            self.direction.y = 0
            self.direction.x = -1
            self.current_move = "west"
            self.speed = 5
        elif controls['right']:
            self.direction.y = 0
            self.direction.x = 1
            self.current_move = "east"
            self.speed = 5
        elif controls['up']:
            self.direction.x = 0
            self.direction.y = -1
            self.current_move = "north"
            self.speed = 5
        elif controls['down']:
            self.direction.x = 0
            self.direction.y = 1
            self.current_move = "south"
            self.speed = 5

        self.check_zoom(controls['zoom'])
        self.stop_player_for_boundary(controls)
        if controls['space']:
            self.shoot = True
        else:
            self.shoot = False

    def update_health_points(self, threshold=200, current_points=200):
        self.health_points_threshold = threshold
        self.current_health_points = current_points

    def blit_health_bar(self, surface):
        offset = 5
        cool_down = self.current_health_points - offset + 1
        x, y, w, h = 10, 10, cool_down, 20
        limit = self.health_points_threshold - offset - 1
        # gray border
        pygame.draw.rect(surface, (127, 127, 127), pygame.Rect(x, y, limit, h), 2)
        # main
        pygame.draw.rect(surface, (209, 0, 0), pygame.Rect(x, y, w, h))
        # rounded light affect
        pygame.draw.rect(surface, (206, 66, 66), pygame.Rect(x, y, w, 10))
        # blit bolt image
        surface.blit(self.assets.heart_img, (x + 3, y - 6))
        text = self.assets.bold_font.render(f"HP {round(self.current_health_points)}", True, (255, 255, 255))
        surface.blit(text, (limit + 20, y - 2))

    def blit_zoom_bar(self, surface):
        offset = 5
        cool_down = self.zoom_cool_down - offset
        x, y, w, h = 10, 40, cool_down, 20
        cool_down_limit = self.zoom_threshold - offset - 1
        # gray border
        pygame.draw.rect(surface, (127, 127, 127), pygame.Rect(x, y, cool_down_limit, h), 2)
        # main
        pygame.draw.rect(surface, (98, 189, 198), pygame.Rect(x, y, w, h))
        # rounded light affect
        pygame.draw.rect(surface, (125, 200, 209), pygame.Rect(x, y, w, 10))
        # blit bolt image
        surface.blit(self.assets.bolt_img, (x + 2, y - 4))
        nos = self.zoom_cool_down - 1 if self.zoom_cool_down - 1 != 4 else 0
        percent = self.assets.bold_font.render(f"NOS {nos}", True, (255, 255, 255))
        surface.blit(percent, (cool_down_limit + 20, y - 2))

    def check_bullet_hit_planet(self, surface, planet, offset, internal_offset):
        """
        count bullets hits and remove bullet
        return [], 0
        """
        number_of_hits = 0
        planet_rect = pygame.Rect(planet.pos.x, planet.pos.y, planet.assets.planet_size, planet.assets.planet_size)
        self.explosion_planet.iterate(surface, offset + internal_offset)
        for index, bullet in enumerate(self.boom, 0):
            offset_x = bullet['rect'].x - planet_rect.x
            offset_y = bullet['rect'].y - planet_rect.y
            if bullet['dir'][0] == 0:
                mask_check = planet.mask.overlap(self.bullet_we_mask, (offset_x, offset_y))
            elif bullet['dir'][1] == 0:
                mask_check = planet.mask.overlap(self.bullet_ns_mask, (offset_x, offset_y))
            else:
                mask_check = False
            # print(mask_check)
            if mask_check:
                pygame.draw.circle(surface, (255, 255, 255), planet_rect.center,  planet.assets.planet_size / 2)
                self.explosion_planet.initiate(mask_check)
                del self.boom[index]
                number_of_hits += 1
        return number_of_hits, self.boom

    def blit_player_projectile(self, surface, offset, internal_offset):
        """
        - called from camera module
        :param surface: - internal_surf
        :param offset: - for camera movement
        :param internal_offset: - for camera movement
        """

        if self.shoot or len(self.boom) > 0:
            if (datetime.now() - self.last_shot_dt).total_seconds() > .2:
                self.last_shot_dt = datetime.now()
                if self.shoot:
                    self.assets.play_laser_sound()
                    pos = (self.screen.get_width() / 2, self.screen.get_height() / 2)
                    path_offset = pos + offset + internal_offset
                    current_move = self.current_move
                    if current_move == "north":
                        self.boom_append({"pos": path_offset - (0, 5), "dir": (0, -15), "dt": datetime.now(),
                                          "rect": pygame.Rect(0, 0, 0, 0)})
                    elif current_move == "south":
                        self.boom_append({"pos": path_offset + (0, 5), "dir": (0, 15), "dt": datetime.now(),
                                          "rect": pygame.Rect(0, 0, 0, 0)})
                    elif current_move == "east":
                        self.boom_append({"pos": path_offset + (5, 0), "dir": (15, 0), "dt": datetime.now(),
                                          "rect": pygame.Rect(0, 0, 0, 0)})
                    elif current_move == "west":
                        self.boom_append({"pos": path_offset - (5, 0), "dir": (-15, 0), "dt": datetime.now(),
                                          "rect": pygame.Rect(0, 0, 0, 0)})
            else:
                self.shoot = False
            level = self.settings.level_rect
            new_boom = []
            new_boom_append = new_boom.append
            for item in self.boom:
                x, y = item['pos'] - offset - internal_offset
                bw, bh = self.bullet_height if item['dir'][0] != 0.0 else self.bullet_width, self.bullet_height if item['dir'][1] != 0.0 else self.bullet_width
                bullet = pygame.Rect(item['pos'][0], item['pos'][1], bw, bh)
                if level.colliderect(bullet):
                    bx, by = item['dir'][0] if item['dir'][0] != 0.0 else 0, item['dir'][1] if item['dir'][
                                                                                                   1] != 0.0 else 0
                    item['pos'] += (bx, by)
                    new_boom_append(
                        {"pos": item['pos'], "dir": item['dir'], "dt": item["dt"], "rect": pygame.Rect(x, y, bw, bh)})
                pygame.draw.rect(surface, (0, 255, 21), (x, y, bw, bh))
            self.boom = new_boom
            self.boom_append = self.boom.append

    def stop_player_for_boundary(self, controls):
        lev = self.settings.level_rect
        pos = (0, 0)
        if self.rect.top < lev.top and self.direction.y == -1:
            self.direction = pygame.math.Vector2()
            pos, d = (0, 1), "south"
        elif self.rect.bottom > lev.bottom and self.direction.y == 1:
            self.direction = pygame.math.Vector2()
            pos, d = (0, -1), "north"
        elif self.rect.right > lev.right and self.direction.x == 1:
            self.direction = pygame.math.Vector2()
            pos, d = (-1, 0), "west"
        elif self.rect.left < lev.left and self.direction.x == -1:
            self.direction = pygame.math.Vector2()
            pos, d = (1, 0), "east"
        if self.direction == pygame.math.Vector2():
            self.explosion.initiate((self.screen.get_width() / 2, self.screen.get_height() / 2))
            try:
                controls.start_rumble(1000)
            except:
                pass
            # self.assets.stop_zoom_sound()
            self.assets.play_explosion_sound()
            self.direction = pygame.math.Vector2(pos)
            self.current_move = d
            if self.current_speed > 6:
                self.current_health_points = 0 if self.current_health_points <= 0 else self.current_health_points - (
                        self.current_health_points // 4)
            else:
                self.current_health_points = 0 if self.current_health_points <= 0 else self.current_health_points - (
                        self.current_health_points // 6)

    def blit_player(self, surface, offset, internal_offset, controls):
        player_x, player_y = self.rect.topleft - offset + internal_offset
        surface.blit(self.image, (player_x, player_y))
        self.stop_player_for_boundary(controls)

    def destroy_object(self, x, y, topleft_tuple, botright_tuple):
        results = [
            x > botright_tuple[0],
            x < topleft_tuple[0],
            y < topleft_tuple[1],
            y > botright_tuple[1]
        ]
        return True if True in results else False

    def blit_player_path(self, surface, offset, internal_offset):
        """
        - called from camera module
        :param surface: - internal_surf
        :param offset: - for camera movement
        :param internal_offset: - for camera movement
        """
        pos = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        path_offset = pos + offset + internal_offset
        moving = True if self.direction.x != 0 or self.direction.y != 0 else False
        if moving and round((datetime.now() - self.start_dt).total_seconds()) % 2 == 0:
            self.path_append({'pos': path_offset, 'tick': 0})
        elif self.is_zoom or self.speed > 2:
            self.path_append({'pos': path_offset, 'tick': 0})
        new_path = []
        new_path_append = new_path.append
        for item in self.path:
            if item['tick'] < self.path_tick_limit:
                new_path_append({'pos': item['pos'], 'tick': item['tick'] + 4})
                color = (89, 35, 13)  # orange
                if item['tick'] < self.path_tick_limit / 6:
                    color = (230, 0, 0)  # red
                pygame.draw.circle(surface, color, item['pos'] - offset - internal_offset,
                                   (self.path_tick_limit - item['tick']) / randint(10, 15))
        self.path = new_path
        self.path_append = self.path.append

    def update(self, controls):
        if self.current_health_points > 0:
            self.input(controls)
            speed = self.speed
            self.current_speed = speed
            self.rect.center += self.direction * speed

    def update_settings(self, settings_class):
        self.settings = settings_class
