import pygame
from init_fonts import Font
from minimap import MiniMap
from datetime import datetime
from random import choice


class CameraGroup(pygame.sprite.Group):
    def __init__(self, settings_obj, sounds, message):
        super().__init__()
        self.minimap = MiniMap(settings_obj)
        self.sounds = sounds
        self.settings = settings_obj
        self.screen = settings_obj.screen
        self.display_surface = pygame.display.get_surface()
        self.enemy_timer = datetime.now()
        self.message = message
        self.last_amount_small_enemy_kills = 0
        # camera offset
        self.offset = pygame.math.Vector2()
        self.w = self.display_surface.get_size()[0]
        self.h = self.display_surface.get_size()[1]
        self.half_w = self.w // 2
        self.half_h = self.h // 2

        # box setup
        self.w_quart = self.w / 2.5
        self.h_quart = self.h / 2.5
        self.camera_borders = {'left': self.w_quart, 'right': self.w_quart, 'top': self.h_quart, 'bottom': self.h_quart}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # controller instructions
        self.controller_img = pygame.image.load("assets/background/keyboard/xbox_controller.png").convert()
        self.controller_img.set_colorkey((0, 0, 0))

        # key_pad player instructions
        key = pygame.image.load("assets/background/keyboard/key_pad.png").convert()
        key.set_colorkey((0, 0, 0))
        self.key_pad_img = pygame.transform.scale(key, (
            key.get_width() - (key.get_width() / 5), key.get_height() - (key.get_height() / 5)))
        self.key_pad_rect = self.key_pad_img.get_rect()

        key = pygame.image.load("assets/background/keyboard/pressed/z.png").convert()
        key.set_colorkey((0, 0, 0))
        self.key_z = pygame.transform.scale(key, (
            key.get_width() - (key.get_width() / 5), key.get_height() - (key.get_height() / 5)))

        key = pygame.image.load("assets/background/keyboard/pressed/up.png").convert()
        key.set_colorkey((0, 0, 0))
        self.key_up = pygame.transform.scale(key, (
            key.get_width() - (key.get_width() / 5), key.get_height() - (key.get_height() / 5)))

        key = pygame.image.load("assets/background/keyboard/pressed/down.png").convert()
        key.set_colorkey((0, 0, 0))
        self.key_down = pygame.transform.scale(key, (
            key.get_width() - (key.get_width() / 5), key.get_height() - (key.get_height() / 5)))

        key = pygame.image.load("assets/background/keyboard/pressed/left.png").convert()
        key.set_colorkey((0, 0, 0))
        self.key_left = pygame.transform.scale(key, (
            key.get_width() - (key.get_width() / 5), key.get_height() - (key.get_height() / 5)))

        key = pygame.image.load("assets/background/keyboard/pressed/right.png").convert()
        key.set_colorkey((0, 0, 0))
        self.key_right = pygame.transform.scale(key, (
            key.get_width() - (key.get_width() / 5), key.get_height() - (key.get_height() / 5)))

        key = pygame.image.load("assets/background/keyboard/pressed/space.png").convert()
        key.set_colorkey((0, 0, 0))
        self.key_space = pygame.transform.scale(key, (
            key.get_width() - (key.get_width() / 5), key.get_height() - (key.get_height() / 5)))

        key = pygame.image.load("assets/background/keyboard/pressed/esc.png").convert()
        key.set_colorkey((0, 0, 0))
        self.key_esc = pygame.transform.scale(key, (
            key.get_width() - (key.get_width() / 5), key.get_height() - (key.get_height() / 5)))

        # zoom
        self.zoom_scale = 1
        self.internal_surf_size = (self.screen.get_width(), self.screen.get_height())
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)  # keep all colors
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] / 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] / 2 - self.half_h

        # fonts
        self.fonts = Font(size=25)
        self.bold_font = self.fonts.mago_bold

        # space man
        self.space_man_points = 0
        self.peace_timer = 0
        self.no_peace_timer = 0

    def update_settings(self, settings):
        self.settings = settings

    def center_target_camera(self, target):
        #  placement of player.image
        self.offset.x = target.rect.centerx - (self.settings.screen.get_width() / 2)
        self.offset.y = target.rect.centery - (self.settings.screen.get_height() / 2)

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.zoom_scale += 0.1
        if keys[pygame.K_2]:
            self.zoom_scale -= 0.1

    def blit_stary_background(self, background_settings):
        level = background_settings['lev']
        x, y = background_settings['offset_pos']
        # level background
        pygame.draw.rect(self.internal_surf, (27, 33, 45), pygame.Rect(x, y, level.width, level.height))

    def blit_background_border(self, background_settings):
        level = background_settings['lev']
        x, y = background_settings['offset_pos']
        r = pygame.Rect(x, y, level.width, level.height)
        pygame.draw.rect(self.internal_surf,
            choice(([(0, 0, 0)] * 20) + [(255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100), (50, 50, 50)]), r, 4)
        r.x = r.x - 3
        r.y = r.y - 3
        pygame.draw.rect(self.internal_surf, (127, 127, 127), r, 4)

    def blit_key_pad_instructions(self, controls):
        if controls.joysticks:
            self.internal_surf.blit(self.controller_img, (self.screen.get_width() - 10 - self.controller_img.get_width(),
                                                          self.screen.get_height() - 10 - self.controller_img.get_height()))
        else:
            pad_rect = self.key_pad_rect
            self.key_pad_rect.x = self.screen.get_width() - pad_rect.w - 10
            self.key_pad_rect.y = self.screen.get_height() - pad_rect.h - 10
            self.internal_surf.blit(self.key_pad_img, (pad_rect.x, pad_rect.y))
            if controls.obj['up']:
                x, y = pad_rect.x + self.key_up.get_width(), pad_rect.y
                pygame.draw.rect(self.internal_surf, (27, 33, 45),
                                 (x, y, self.key_up.get_width(), self.key_up.get_height()))
                self.internal_surf.blit(self.key_up, (x, y))
            if controls.obj['down']:
                x, y = pad_rect.x + self.key_down.get_width(), pad_rect.y + self.key_down.get_height()
                pygame.draw.rect(self.internal_surf, (27, 33, 45),
                                 (x, y, self.key_down.get_width(), self.key_down.get_height()))
                self.internal_surf.blit(self.key_down, (x, y))
            if controls.obj['left']:
                x, y = pad_rect.x, pad_rect.y + self.key_left.get_height()
                pygame.draw.rect(self.internal_surf, (27, 33, 45),
                                 (x, y, self.key_left.get_width(), self.key_left.get_height()))
                self.internal_surf.blit(self.key_left, (x, y))
            if controls.obj['right']:
                x, y = pad_rect.x + (self.key_right.get_width() * 2), pad_rect.y + self.key_right.get_height()
                pygame.draw.rect(self.internal_surf, (27, 33, 45),
                                 (x, y, self.key_right.get_width(), self.key_right.get_height()))
                self.internal_surf.blit(self.key_right, (x, y))
            if controls.obj['space']:
                x, y = pad_rect.x, pad_rect.bottomleft[1] - self.key_space.get_height()
                pygame.draw.rect(self.internal_surf, (27, 33, 45),
                                 (x, y - 3, self.key_space.get_width(), self.key_space.get_height()))
                self.internal_surf.blit(self.key_space, (x, y))
            if controls.obj['esc']:
                x, y = pad_rect.x + (self.key_up.get_width() * 2), pad_rect.y
                pygame.draw.rect(self.internal_surf, (27, 33, 45),
                                 (x, y, self.key_esc.get_width(), self.key_esc.get_height()))
                self.internal_surf.blit(self.key_esc, (x, y))
            if controls.obj['zoom']:
                x, y = pad_rect.x, pad_rect.y
                pygame.draw.rect(self.internal_surf, (27, 33, 45), (x, y, self.key_z.get_width(), self.key_z.get_height()))
                self.internal_surf.blit(self.key_z, (x, y))

    def blit_fps(self, clock):
        fps_text = self.bold_font.render(f'FPS: {round(float(clock.get_fps()), 2)}', True, (255, 255, 255))
        self.internal_surf.blit(fps_text, (10, self.screen.get_height() - 10 - fps_text.get_height()))  # height

    def hit_mine(self, surface, mine, player, planet, small_enemy, score, offset, internal_offset, controls):
        mine_pos = (0, 0)
        if not mine.kill_mine:
            mine_pos = mine.rect.topleft - offset + internal_offset
            # if not mine.explosion.start:
            surface.blit(mine.image, mine_pos)
            mine.update_object(surface, offset, internal_offset)
            p_bullets = player.boom
            for index, pb in enumerate(p_bullets, 0):
                offset_x = pb['rect'].x - mine.rect.x
                offset_y = pb['rect'].y - mine.rect.y
                if pb['dir'][0] == 0:
                    mask_check = mine.mask.overlap(player.bullet_we_mask, (offset_x, offset_y))
                elif pb['dir'][1] == 0:
                    mask_check = mine.mask.overlap(player.bullet_ns_mask, (offset_x, offset_y))
                else:
                    mask_check = False
                if mask_check:
                    score.update_score(10)
                    mine.hit()
                    del player.boom[index]  # hide mine from blit queue
            player_off = player.rect.topleft - offset + internal_offset
            player_r = pygame.Rect(player_off[0], player_off[1], player.rect.w, player.rect.h)
            if mine.explosion.hit_box_rect.colliderect(player_r) and mine.explosion.exp_index != -1:
                player.update_health_neg_5()
                controls.start_rumble(100)
            planet_off = player.rect.topleft - offset + internal_offset
            planet_r = pygame.Rect(planet_off[0], planet_off[1], planet.rect.w, planet.rect.h)
            if mine.explosion.hit_box_rect.colliderect(planet_r) and mine.explosion.exp_index != -1:
                planet.current_health_points = planet.current_health_points - 5 if planet.current_health_points > 5 else 0
            for index, enemy in enumerate(small_enemy.enemies, 0):
                enemy_off = enemy['rect'].topleft - offset + internal_offset
                enemy_r = pygame.Rect(enemy_off[0], enemy_off[1], enemy['rect'].w, enemy['rect'].h)
                if mine.explosion.hit_box_rect.colliderect(enemy_r) and mine.explosion.exp_index != -1:
                    score.update_score(20)
                    del small_enemy.enemies[index]
                    small_enemy.add_new_enemy()
        return mine_pos

    def custom_draw(self, pressed, clock, player, background, score, small_enemy, planet, start_explosion, controls, player_name):
        self.center_target_camera(player)
        self.internal_surf.fill('black')
        # blit borders
        background_settings = {
            "lev": self.settings.level_rect,
            "offset_pos": self.settings.level_rect.topleft - self.offset + self.internal_offset
        }
        self.blit_stary_background(background_settings)

        # blit level borders
        self.blit_background_border(background_settings)

        # active elements
        sprites = self.sprites()
        sprites.reverse()
        player = sprites[-1]
        # blit stars

        if player.current_health_points > 0:
            mines_pos = []
            mines_pos_append = mines_pos.append
            for sprite in sprites[::-3]:
                offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
                if sprite.rect.w == 96:  # a mine
                    mines_pos_append(
                        self.hit_mine(self.internal_surf, sprite, player, planet, small_enemy, score, self.offset,
                                      self.internal_offset, controls))
                else:
                    self.internal_surf.blit(sprite.image, offset_pos)

            # planet
            planet.blit_next_planet_image(self.internal_surf, self.offset, self.internal_offset)

            # blit path behind player
            player.blit_player_path(self.internal_surf, self.offset, self.internal_offset)

            # blit player
            player.blit_player(self.internal_surf, self.offset, self.internal_offset, controls)

            # blit big sale
            background.power_up.blit_power_up(self.internal_surf, self.offset, self.internal_offset)
            background.power_up.power_up_collide(self.internal_surf, planet, player, self.minimap.player_pos,
                                                 small_enemy, self.offset, self.internal_offset)

            # small enemy

            if self.peace_timer != 0 and (datetime.now() - self.peace_timer).total_seconds() < 2:
                pass
            else:
                self.peace_timer == 0
                small_enemy.blit_enemy(self.internal_surf, planet, player, score, self.offset, self.internal_offset, controls)
                small_enemy.enemy_hit(self.internal_surf, player, score, self.offset, self.internal_offset)



            # blit Spaceman
            background.space_man.update(self.internal_surf, self.offset, self.internal_offset, player_name)

            # blit projectile
            if self.no_peace_timer != 0 and (datetime.now() - self.no_peace_timer).total_seconds() < 5:
                pass
            else:
                self.no_peace_timer = 0
                player.blit_player_projectile(self.internal_surf, self.offset, self.internal_offset)

            # blit explosion
            player.explosion.iterate(self.internal_surf, self.offset + self.internal_offset)

            # blit player pos & minimap
            self.minimap.blit_player_pos(self.internal_surf, self.offset, self.internal_offset,
                                         background.mine_positions, small_enemy.enemies)

            # health bar
            player.blit_health_bar(self.internal_surf)

            # zoom bar
            player.blit_zoom_bar(self.internal_surf)

            # planet health
            planet.blit_health_bar(self.internal_surf)

            # blit score
            score.blit_score(self.internal_surf)

            # key_pad for player instructions
            self.blit_key_pad_instructions(controls)

            # blit fps
            self.blit_fps(clock)

            # check bullets against planet bulbs apply white surface briefly
            number_of_hits, player_bullets = player.check_bullet_hit_planet(self.internal_surf, planet, self.offset,
                                                                            self.internal_offset)
            planet_dead = planet.update_planet_health(number_of_hits, score)

            # kill spaceman or save
            self.space_man_points = background.space_man.hit_spaceman_or_save(self.internal_surf, player_bullets,
                                                                         small_enemy,
                                                                         self.minimap.player_pos, self.offset,
                                                                         self.internal_offset)
            score.update_score(self.space_man_points)
            if self.space_man_points > 0:
                self.peace_timer = datetime.now()
                planet.current_health_points = planet.current_health_points + 200 if planet.current_health_points < planet.health_points_threshold - 200 else planet.health_points_threshold
                player.current_health_points = player.current_health_points + 50 if player.current_health_points < player.health_points_threshold - 50 else player.health_points_threshold
                player.update_to_max_zoom()
            elif self.space_man_points < 0:
                self.no_peace_timer = datetime.now()
                planet.update_to_half_damage()
                player.update_to_half_zoom()
                player.update_to_half_health()

            # play highscore sound
            if score.score > background.highest_score and background.assets.play_high_score_index < 1:
                self.message.init_message("High Score!", "High Score!")
                background.assets.play_high_score()

            # check if score is 0 and player time is over 1 minute
            if score.score == 0 and (datetime.now() - score.start_time).total_seconds() > 60:
                for i in range(10):
                    small_enemy.add_new_enemy()

            # Start explosion
            start_explosion.iterate(self.internal_surf)

            # escape to Game over screen
            if planet_dead:
                player.update_health_points(threshold=200 * 2, current_points=0)

            self.zoom_scale = .5 if self.zoom_scale <= 0.5 else self.zoom_scale
            self.zoom_scale = 2 if self.zoom_scale >= 2 else self.zoom_scale
            scaled_surf = pygame.transform.scale(self.internal_surf,
                                                 self.internal_surface_size_vector * self.zoom_scale)
            scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))
            self.display_surface.blit(scaled_surf, scaled_rect)
