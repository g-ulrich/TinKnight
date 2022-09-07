import pygame
import json
from init_fonts import Font
from datetime import datetime
from random import randint, choice
from spaceman import SpaceManTitle, SpaceMan
from asset_classes import BackgroundAssets
from message import Message
from explosion import Explosion
from bible_names import references


class PowerUps:
    def __init__(self, settings, assets, score):
        self.assets = assets
        self.score = score
        self.message = Message()
        self.settings = settings
        self.level_rect = settings.level_rect
        self.random_things = (['points'] * 20) + (['planet_hp', 'player_hp', 'nos', 'nuke', 'big_bullet'] * 2) + ['enemies_added']
        self.sound = self.assets.power_up_sound
        self.all_objects = assets.power_up_objects()
        self.power_up = choice(self.all_objects)
        self.img = self.power_up['img']
        self.rect = self.img.get_rect()
        self.rect.x = randint(self.level_rect.topleft[0] + 60, self.level_rect.bottomright[0] - 60)
        self.rect.y = randint(self.level_rect.topleft[1] + 60, self.level_rect.bottomright[1] - 60)
        self.speed = 1
        rand_dir = (randint(-1, 1), randint(-1, 1))
        self.dir = pygame.math.Vector2(rand_dir)
        self.rotation_index = 0
        self.circle_index = 0
        self.nuke_start_time = 0

    def update_img(self):
        r = self.rect
        lr = self.level_rect
        if r.left <= lr.left:
            self.dir = pygame.math.Vector2((self.dir.x * -1, self.dir.y))
        elif r.right >= lr.right:
            self.dir = pygame.math.Vector2((self.dir.x * -1, self.dir.y))
        elif r.bottom >= lr.bottom:
            self.dir = pygame.math.Vector2((self.dir.x, self.dir.y * -1))
        elif r.top <= lr.top:
            self.dir = pygame.math.Vector2((self.dir.x, self.dir.y * -1))
        self.rect.topleft += self.dir * self.speed
        self.rotation_index = self.rotation_index + 1 if self.rotation_index < 360 else 0

    def play_power_up(self):
        self.sound.play()

    def select_power_up(self, surface, planet, player, player_pos, small_enemy, offset, internal_offset):
        rand_int = randint(-50, 100)
        obj = self.power_up
        if obj['type'] == "random":
            power = choice(self.random_things)
            if power == "nuke":
                self.nuke_start_time = datetime.now()
                surface.fill((255, 0, 0))
                small_enemy.kill_half()
            elif power == "points":
                self.score.update_score(rand_int)
            elif power == "enemies_added":
                for i in range(randint(1, 5)):
                    small_enemy.add_new_enemy()
            elif power == "nos":
                player.update_to_max_zoom()
            elif power == "planet_hp":
                planet.update_to_max_health()
            elif power == "player_hp":
                player.update_to_max_health()
            elif power == "big_bullet":
                player.update_bullets(player.bullet_width + 10, player.bullet_height + 20)
            if power == "points":
                self.message.init_message("", f"{'+' if rand_int > 0.0 else ''}{rand_int} Points!")
            elif obj['type'] == "random" and not power == "points":
                self.message.init_message(power.replace("_", " ").upper(), f"{obj['type'].capitalize()} - {obj['name']}")
            else:
                self.message.init_message(power.replace("_", " ").upper(), f"{obj['name']}")
        else:
            if obj['type'] == "nos":
                player.update_to_max_zoom()
            elif obj['type'] == "planet_hp":
                planet.update_to_max_health()
            elif obj['type'] == "player_hp":
                player.update_to_max_health()
            elif obj['type'] == "nuke":
                self.nuke_start_time = datetime.now()
                surface.fill((255, 0, 0))
                small_enemy.kill_half()
            self.message.init_message(obj['type'].replace("_", " ").upper(), f"{obj['name']}")
        small_enemy.add_new_enemy()

    def power_up_collide(self, surface, planet, player, player_pos, small_enemy, offset, internal_offset):
        pr = pygame.Rect(player_pos[0], player_pos[1], player.rect.w, player.rect.h)
        if pr.colliderect(self.rect):
            self.play_power_up()
            self.select_power_up(surface, planet, player, player_pos, small_enemy, offset, internal_offset)
            self.reset_power_up()

    def blit_power_up(self, surface, offset, internal_offset):
        self.update_img()
        self.message.iterate_message(surface)
        if self.nuke_start_time != 0 and (datetime.now() - self.nuke_start_time).total_seconds() < 1.0:
            surface.fill((randint(200, 255), 0, 0))
        rotated_img = pygame.transform.rotate(self.img, self.rotation_index)
        surface.blit(rotated_img, self.rect.topleft - offset + internal_offset)

    def reset_power_up(self):
        self.power_up = choice(self.all_objects)
        self.img = self.power_up['img']
        self.rect = self.img.get_rect()
        self.rect.x = randint(self.level_rect.topleft[0] + 60, self.level_rect.bottomright[0] - 60)
        self.rect.y = randint(self.level_rect.topleft[1] + 60, self.level_rect.bottomright[1] - 60)
        self.speed = 1
        rand_dir = (randint(-1, 1), randint(-1, 1))
        self.dir = pygame.math.Vector2(rand_dir)


class SpaceMines(pygame.sprite.Sprite):
    def __init__(self, pos, settings_obj, group, assets):
        super().__init__(group)
        self.assets = assets
        self.all_images = assets.all_mines
        self.image = assets.all_mines[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.max_index = len(self.all_images) - 1
        self.img_index = 0
        self.explosion = Explosion(settings_obj, 800, 21, color=(255, 200, 200), iterate_by=.8, sec_color=(255, 0, 0))
        self.kill_mine = False

    def hit(self):
        self.img_index = self.img_index + 1 if self.img_index < self.max_index else self.max_index
        if self.img_index == self.max_index and self.explosion.exp_index == -1:
            self.explosion.initiate(self.rect.center)
            self.assets.play_long_explosion()

    def update_object(self, surface, offset, internal_offset):
        if self.explosion.exp_index != -1 and not self.explosion.start:  # explosion finished
            self.kill_mine = True
            self.assets.stop_long_explosion()
        else:
            self.image = self.all_images[self.img_index]
            self.explosion.iterate(surface, offset + internal_offset)


class StarNoGroup(pygame.sprite.Sprite):
    def __init__(self, surface, number_of_stars=500):
        self.surface = surface
        self.assets = BackgroundAssets()
        w, h = surface.get_width(), surface.get_height()
        self.images = []
        self.images_append = self.images.append
        for i in range(number_of_stars):
            scaled = randint(1, 20)
            img = pygame.transform.scale(choice(self.assets.stars), (scaled, scaled))
            self.images_append({"img": img, "rect": img.get_rect(topleft=(randint(0, w), randint(0, h)))})

    def blit_stars(self):
        for obj in self.images:
            rect = obj['rect']
            self.surface.blit(obj['img'], (rect.x, rect.y))


class Star(pygame.sprite.Sprite):
    def __init__(self, pos, group, scale_int, all_star_images):
        super().__init__(group)
        self.image = pygame.transform.scale(choice(all_star_images), (scale_int, scale_int))
        self.rect = self.image.get_rect(topleft=pos)


class Background:
    def __init__(self, settings_obj, group, planet_title, sounds, score, keyboard):
        self.camera_group = group
        self.settings = settings_obj
        self.screen = settings_obj.screen
        self.sounds = sounds
        self.assets = BackgroundAssets()
        self.power_up = PowerUps(self.settings, self.assets, score)
        self.high_score = self.high_score_read()
        self.highest_score = max([i['s'] for i in self.high_score['scores']])
        # Fonts
        self.title_font = Font(25)
        self.primary_font = Font(150)
        self.secondary_font = Font(50)

        # planet title
        self.planet_title = planet_title

        # SpaceMan
        self.space_man = SpaceMan(settings_obj)

        # Title screen
        self.restart = False
        self.start = False
        self.title_stars = StarNoGroup(self.screen, 30)

        self.keyboard = keyboard

        self.start_dt = datetime.now()
        self.reference_dt = datetime.now()
        self.reference = choice(references)

        # place the stars and insert into camera group
        self.star_positions = []
        self.star_positions_append = self.star_positions.append

        level_rect = self.settings.level_rect
        for i in range(100):
            # x is a negative value
            pos = pygame.math.Vector2(
                randint(level_rect.topleft[0], level_rect.bottomright[1]),
                randint(level_rect.topleft[0], level_rect.bottomright[1])
            )
            self.star_positions_append(pos)
            Star(pos, self.camera_group, randint(1, 20), self.assets.stars)

        # place the space mines and insert into camera group
        self.mine_positions = []
        self.mine_positions_append = self.mine_positions.append
        self.mines = []
        self.mines_append = self.mines.append
        for i in range(10):
            # x is a negative value
            pos = pygame.math.Vector2(
                randint(level_rect.topleft[0] + 100, level_rect.bottomright[1] - 100),
                randint(level_rect.topleft[0] + 100, level_rect.bottomright[1] - 100)
            )
            self.mine_positions_append(pos)
            self.mines_append(SpaceMines(pos, settings_obj, self.camera_group, self.assets))

        # title screen space man
        self.space_man_title = SpaceManTitle(self.settings)

        # gameover
        self.game_over_index = 0

    def blit_game_over(self, controls, score):
        restart_game = False
        if not self.restart:
            if self.game_over_index == 0:
                self.sounds.stop_menu_select()
                self.sounds.play_game_over()
            elif self.game_over_index == self.settings.fps * 60:
                self.restart = True
            self.game_over_index += 1
            press_r_or_plus = "+" if controls.joysticks else "R"
            over = self.primary_font.mago_bold.render(f"Game Over", True, choice(
                ([(0, 0, 0)]*20) + [(255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100), (50, 50, 50)]))
            self.screen.blit(over, ((self.screen.get_width() / 2 - (over.get_width() / 2)) - 5,
                                    self.screen.get_height() / 2 - over.get_height()-5))
            over = self.primary_font.mago_bold.render(f"Game Over", True, (255, 255, 255))
            self.screen.blit(over, ((self.screen.get_width() / 2 - (over.get_width() / 2)),
                                    self.screen.get_height() / 2 - over.get_height()))
            restart1 = self.secondary_font.mago_bold.render(f"Press     To Restart", True, choice(
                ([(0, 0, 0)]*20) + [(255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100), (50, 50, 50)]))
            self.screen.blit(restart1, ((self.screen.get_width() / 2 - (restart1.get_width() / 2)) - 3,
                                       self.screen.get_height() / 2 + restart1.get_height() - 3))
            restart = self.secondary_font.mago_bold.render(f"Press     To Restart", True, (255, 255, 255))
            space = self.secondary_font.mago_bold.render(f" {press_r_or_plus}       ", True, (255, 255, 255))
            space_dark = self.secondary_font.mago_bold.render(f" {press_r_or_plus}       ", True, (100, 100, 100))
            self.screen.blit(restart, ((self.screen.get_width() / 2 - (restart.get_width() / 2)),
                                       self.screen.get_height() / 2 + restart.get_height()))
            self.screen.blit(space_dark, ((self.screen.get_width() / 2 - (space_dark.get_width() / 2)),
                                          self.screen.get_height() / 2 + restart.get_height()))
            if round((self.start_dt - datetime.now()).total_seconds()) % 2 == 0:
                self.screen.blit(space, ((self.screen.get_width() / 2 - (space.get_width() / 2)),
                                         self.screen.get_height() / 2 + restart.get_height()))
            # restart game if space bar is pressed
            if controls.obj['restart']:
                self.restart = True
        else:
            self.high_score_write(self.keyboard.user_text, score.score)
            self.screen.fill((27, 33, 45))
            loading = self.secondary_font.mago_bold.render(f"Restart Loading...", True, (255, 255, 255))
            self.screen.blit(loading, ((self.screen.get_width() / 2 - (loading.get_width() / 2)),
                                       self.screen.get_height() / 2 - loading.get_height()))
            restart_game = True

        return False if restart_game else True

    def blit_pause_game(self, controls):
        restart_game = False
        if not self.restart:
            press_space_or_minus = "+" if controls.joysticks else "R"
            over = self.primary_font.mago_bold.render(f"PAUSE", True, (255, 255, 255))
            self.screen.blit(over, ((self.screen.get_width() / 2 - (over.get_width() / 2)),
                                    self.screen.get_height() / 2 - over.get_height()))
            restart = self.secondary_font.mago_bold.render(f"Press          To Restart", True, (255, 255, 255))
            space = self.secondary_font.mago_bold.render(f"     {press_space_or_minus}           ", True,
                                                         (255, 255, 255))
            space_dark = self.secondary_font.mago_bold.render(f"     {press_space_or_minus}           ", True,
                                                              (100, 100, 100))
            self.screen.blit(restart, ((self.screen.get_width() / 2 - (restart.get_width() / 2)),
                                       self.screen.get_height() / 2 + restart.get_height()))
            self.screen.blit(space_dark, ((self.screen.get_width() / 2 - (space_dark.get_width() / 2)),
                                          self.screen.get_height() / 2 + restart.get_height()))
            if round((self.start_dt - datetime.now()).total_seconds()) % 2 == 0:
                self.screen.blit(space, ((self.screen.get_width() / 2 - (space.get_width() / 2)),
                                         self.screen.get_height() / 2 + restart.get_height()))
            # restart game if space bar is pressed
            if controls.obj['restart']:
                self.restart = True
        else:
            self.screen.fill((27, 33, 45))
            loading = self.secondary_font.mago_bold.render(f"Restart Loading...", True, (255, 255, 255))
            self.screen.blit(loading, ((self.screen.get_width() / 2 - (loading.get_width() / 2)),
                                       self.screen.get_height() / 2 - loading.get_height()))
            restart_game = True

        return False if restart_game else True

    def blit_scripture_reference(self, surface, title_rect):
        if (datetime.now() - self.reference_dt).total_seconds() < 1.5:
            verse = choice(references)
            text = self.secondary_font.mago_bold.render(verse, True, (0, 0, 0))
            text2 = self.secondary_font.mago_bold.render(verse, True, (127, 127, 127))
        else:
            text = self.secondary_font.mago_bold.render(self.reference, True, choice(
                ([(0, 0, 0)]*20) + [(255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100), (50, 50, 50)]))
            text2 = self.secondary_font.mago_bold.render(self.reference, True, (127, 127, 127))
        # rotated = pygame.transform.rotate(title, 45.0)
        surface.blit(text, ((title_rect.x + title_rect.w) - text.get_width() - 3, title_rect.y - 10 - 3))
        surface.blit(text2, ((title_rect.x + title_rect.w) - text.get_width(), title_rect.y - 10))

    def blit_title_screen(self, controls, left_click):
        remove_title_screen = True
        self.screen.fill((27, 33, 45))
        self.title_stars.blit_stars()
        self.planet_title.blit_next_planet_image(self.screen)
        self.space_man_title.update(self.screen)

        title_bg = self.primary_font.mago_bold.render(f"TIN KNIGHT", True, (0, 0, 0))
        title = self.primary_font.mago_bold.render(f"TIN KNIGHT", True, (255, 255, 255))
        title_rect = title.get_rect()
        title_rect.x = self.screen.get_width() / 2 - (title_rect.w / 2)
        title_rect.y = (self.screen.get_height() / 2 - title_rect.h) - 50
        self.screen.blit(title_bg, (title_rect.x - 4, title_rect.y - 4))
        self.screen.blit(title, (title_rect.x, title_rect.y))
        self.blit_high_scores(self.screen, title_rect)
        self.blit_scripture_reference(self.screen, title_rect)
        self.keyboard.type_name(self.screen, controls, title)
        quit_game = self.keyboard.blit_quit_btn(self.screen, title_rect, controls)
        if quit_game:
            if left_click or controls.obj['esc']:
                quit_game = True
            else:
                quit_game = False
        else:
            quit_game = False
        if self.keyboard.blit_start_btn(self.screen, title_rect, controls):
            if left_click or controls.obj['restart']:
                self.sounds.play_menu_select()
                self.sounds.play_start_game()
                self.start = True
                remove_title_screen = False
        return remove_title_screen, quit_game

    def high_score_write(self, name, score_count):
        high_score_obj = self.high_score_read()
        high_score_obj['scores'].append({'n': name, 's': score_count, 't': 1})
        json_object = json.dumps(high_score_obj, indent=4)
        with open("assets/background/super/secret/user/directory/for/high/scores/highscore.json", "w") as outfile:
            outfile.write(json_object)

    def high_score_read(self):
        with open('assets/background/super/secret/user/directory/for/high/scores/highscore.json', 'r') as openfile:
            self.high_score = json.load(openfile)
        return self.high_score

    def blit_high_scores(self, surface, title_rect):
        rect = pygame.Rect(title_rect.x, title_rect.y + (title_rect.h * 2), title_rect.w, title_rect.h)
        score_array = self.high_score_read()
        score_array['scores'] = sorted(score_array['scores'], key=lambda x: x['s'], reverse=True)
        for index, item in enumerate(score_array['scores'], 1):
            name = self.secondary_font.mago_bold.render(f"{index}) {item['n']}", True, (255, 255, 255))
            score = self.secondary_font.mago_bold.render(f"{item['s']}", True, (255, 255, 255))
            surface.blit(name, (rect.x, rect.y + (index * name.get_height() + 10)))
            surface.blit(score, (rect.topright[0] - score.get_width(), rect.topright[1] + (index * score.get_height() + 10)))
            if index == 5:
                break
