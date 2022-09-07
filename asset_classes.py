import pygame
from spriteObject import SpriteSheet
import json
from init_fonts import Font
from random import randint, choice


class EnemyAssets:
    def __init__(self):
        self.white_quare_sheet = SpriteSheet('assets/enemy/white.png')
        self.font = Font(50)
        self.bold_font = self.font.mago_bold
        self.explosion = pygame.mixer.Sound("assets/sounds/explosion/1.wav")
        self.explosion.set_volume(.3)
        self.sprite_json = {}
        self.sheet = SpriteSheet('assets/enemy/small/ships_sheet.png')
        self.read_json_data('assets/enemy/small/ships_sheet.json')
        frames = [self.sprite_json['frames'][key]['frame'] for key in self.sprite_json['frames'].keys()]
        self.enemy_ships = [i for i in self.get_frames(0, len(frames) - 1, frames)]

    def play_explosion(self):
        self.explosion.play()

    def get_frames(self, start, end, frames):
        images = []
        for i in frames[start:end]:
            images.append(self.sheet.get_image(i['x'], i['y'], i['w'], i['h'], color_key=(0, 0, 0)))
        return images

    def read_json_data(self, path):
        file = open(path)
        self.sprite_json = json.load(file)
        file.close()


class BackgroundAssets:
    def __init__(self):
        self.long_explosion = pygame.mixer.Sound("assets/sounds/explosion/3.wav")
        self.high_score_sound = pygame.mixer.Sound("assets/sounds/high_score.wav")
        self.play_high_score_index = 0
        self.sprite_json = {}
        self.sheet = SpriteSheet('assets/background/stars_sheet.png')
        self.read_json_data('assets/background/stars.json')
        self.stars = [i for i in self.get_frames(0, 55)]
        self.mine_sprite_json = {}
        self.sheet_mine = SpriteSheet('assets/background/mine.png')
        self.read_mine_json_data('assets/background/mine.json')
        self.all_mines = [i for i in self.get_mine_frames(0, 16)]
        self.power_up_sound = pygame.mixer.Sound("assets/sounds/power_up.wav")
        self.power_up_sound.set_volume(.3)

    def play_power_up(self):
        self.power_up_sound.play()

    def power_up_objects(self):
        nos = pygame.image.load('assets/player/power_up/bolt.png').convert()
        nos.set_colorkey((0, 0, 0))
        planet_hp = pygame.image.load('assets/player/power_up/green_heart.png').convert()
        planet_hp.set_colorkey((0, 0, 0))
        player_hp = pygame.image.load('assets/player/power_up/red_heart.png').convert()
        player_hp.set_colorkey((0, 0, 0))
        nuke = pygame.image.load('assets/player/power_up/nuke.png').convert()
        nuke.set_colorkey((0, 0, 0))
        orange = pygame.image.load('assets/player/power_up/orange.png').convert()
        orange.set_colorkey((0, 0, 0))
        strawberry = pygame.image.load('assets/player/power_up/strawberry.png').convert()
        strawberry.set_colorkey((0, 0, 0))
        watermelon = pygame.image.load('assets/player/power_up/watermelon.png').convert()
        watermelon.set_colorkey((0, 0, 0))
        lemon = pygame.image.load('assets/player/power_up/lemon.png').convert()
        lemon.set_colorkey((0, 0, 0))
        pineapple = pygame.image.load('assets/player/power_up/pineapple.png').convert()
        pineapple.set_colorkey((0, 0, 0))
        banana = pygame.image.load('assets/player/power_up/banana.png').convert()
        banana.set_colorkey((0, 0, 0))
        obj = [
            {'name': 'Nos 100%', 'type': 'nos', 'img': pygame.transform.scale(nos, (64, 64))},
            {'name': 'Planet HP 100%', 'type': 'planet_hp', 'img': pygame.transform.scale(planet_hp, (64, 64))},
            {'name': 'Player HP 100%', 'type': 'player_hp', 'img': pygame.transform.scale(player_hp, (64, 64))},
            {'name': 'Kill 50% Enemies', 'type': 'nuke', 'img': pygame.transform.scale(nuke, (64, 64))},
            {'name': 'Orange!', 'type': 'random', 'img': pygame.transform.scale(orange, (64, 64))},
            {'name': 'Strawberry!', 'type': 'random', 'img': pygame.transform.scale(strawberry, (64, 64))},
            {'name': 'Watermelon!', 'type': 'random', 'img': pygame.transform.scale(watermelon, (64, 64))},
            {'name': 'Lemon!', 'type': 'random', 'img': pygame.transform.scale(lemon, (64, 64))},
            {'name': 'Pineapple!', 'type': 'random', 'img': pygame.transform.scale(pineapple, (64, 64))},
            {'name': 'Banana!', 'type': 'random', 'img': pygame.transform.scale(banana, (64, 64))}
        ]
        return obj

    def play_high_score(self):
        self.play_high_score_index += 1
        self.high_score_sound.play()

    def play_long_explosion(self):
        self.long_explosion.play()

    def stop_long_explosion(self):
        self.long_explosion.fadeout(100)

    def get_mine_frames(self, start, end):
        data = self.mine_sprite_json
        frames = [data['frames'][key]['frame'] for key in data['frames'].keys()]
        images = []
        sheet = self.sheet_mine
        for i in frames[start:end]:
            images.append(sheet.get_image(i['x'], i['y'], i['w'], i['h'], color_key=(27, 33, 45)))
        return images

    def read_mine_json_data(self, path):
        file = open(path)
        self.mine_sprite_json = json.load(file)
        file.close()

    def get_frames(self, start, end):
        frames = [self.sprite_json['frames'][key]['frame'] for key in self.sprite_json['frames'].keys()]
        images = []
        for i in frames[start:end]:
            images.append(self.sheet.get_image(i['x'], i['y'], i['w'], i['h'], color_key=(0, 0, 0)))
        return images

    def read_json_data(self, path):
        file = open(path)
        self.sprite_json = json.load(file)
        file.close()


class KeyboardAssets:
    def __init__(self):
        self.letters = [
            {'item': pygame.K_a, 'let': 'a'},
            {'item': pygame.K_b, 'let': 'b'},
            {'item': pygame.K_c, 'let': 'c'},
            {'item': pygame.K_d, 'let': 'd'},
            {'item': pygame.K_e, 'let': 'e'},
            {'item': pygame.K_f, 'let': 'f'},
            {'item': pygame.K_g, 'let': 'g'},
            {'item': pygame.K_h, 'let': 'h'},
            {'item': pygame.K_i, 'let': 'i'},
            {'item': pygame.K_j, 'let': 'j'},
            {'item': pygame.K_k, 'let': 'k'},
            {'item': pygame.K_l, 'let': 'l'},
            {'item': pygame.K_m, 'let': 'm'},
            {'item': pygame.K_n, 'let': 'n'},
            {'item': pygame.K_o, 'let': 'o'},
            {'item': pygame.K_p, 'let': 'p'},
            {'item': pygame.K_q, 'let': 'q'},
            {'item': pygame.K_r, 'let': 'r'},
            {'item': pygame.K_s, 'let': 's'},
            {'item': pygame.K_t, 'let': 't'},
            {'item': pygame.K_u, 'let': 'u'},
            {'item': pygame.K_v, 'let': 'v'},
            {'item': pygame.K_w, 'let': 'w'},
            {'item': pygame.K_x, 'let': 'x'},
            {'item': pygame.K_y, 'let': 'y'},
            {'item': pygame.K_z, 'let': 'z'},
            {'item': pygame.K_SPACE, 'let': ' '}
        ]


class PlanetAssets:
    def __init__(self):
        # fonts
        self.fonts = Font(size=25)
        self.bold_font = self.fonts.mago_bold

        # images
        self.planet_size = 250
        self.planets_array = []
        self.planets_array_append = self.planets_array.append
        # for i in range(1):
        rand_int = randint(0, 7)
        file = open(f'assets/background/planets/p{rand_int}/p{rand_int}.json')
        sheet = SpriteSheet(f'assets/background/planets/p{rand_int}/p{rand_int}.png')
        data = json.load(file)
        self.planets_array_append(
            {"name": "test",
             "images":
                 [pygame.transform.scale(i, (self.planet_size, self.planet_size)) for i in
                  self.get_frames(sheet, data, 0, 159)]
             }
        )
        file.close()

        self.planet = self.planets_array[0]

    def get_frames(self, sheet, sprite_json, start, end):
        frames = [sprite_json['frames'][key]['frame'] for key in sprite_json['frames'].keys()]
        images = []
        for i in frames[start:end]:
            images.append(sheet.get_image(i['x'], i['y'], i['w'], i['h'], color_key=(0, 0, 0)))
        return images


class PlayerAssets:
    def __init__(self):
        # sounds
        # player_zoom
        self.player_zoom = pygame.mixer.Sound("assets/sounds/zoom/1.wav")
        self.player_zoom2 = pygame.mixer.Sound("assets/sounds/zoom/1.wav")
        self.player_zoom.set_volume(.01)

        # player_laser
        self.player_laser = pygame.mixer.Sound("assets/sounds/weapon/laser.wav")
        self.player_laser.set_volume(.2)

        # explosion
        self.player_explosion = pygame.mixer.Sound("assets/sounds/explosion/1.wav")
        self.player_explosion.set_volume(.3)

        self.fonts = Font(size=25)
        self.bold_font = self.fonts.mago_bold
        self.sprite_json = {}
        self.sheet = SpriteSheet("assets/player/ship.png")
        self.read_json_data("assets/player/ship.json")
        self.north = self.get_frames(0, 1)
        self.north_boost = self.get_frames(0, 5)

        self.south = [pygame.transform.rotate(i, 180) for i in self.north]
        self.south_boost = [pygame.transform.rotate(i, 180) for i in self.get_frames(0, 5)]

        self.west = [pygame.transform.rotate(i, 90) for i in self.north]
        self.west_boost = [pygame.transform.rotate(i, 90) for i in self.get_frames(0, 5)]

        self.east = [pygame.transform.rotate(i, 270) for i in self.north]
        self.east_boost = [pygame.transform.rotate(i, 270) for i in self.get_frames(0, 5)]

        self.sheet_for_heart = SpriteSheet("assets/player/heart.png")
        self.heart_img = self.sheet_for_heart.get_image(0, 0, 30, 30, color_key=(0, 0, 0))

        self.sheet_for_bolt = SpriteSheet("assets/player/bolt.png")
        self.bolt_img = self.sheet_for_bolt.get_image(0, 0, 30, 30, color_key=(0, 0, 0))

    def get_frames(self, start, end):
        frames = [self.sprite_json['frames'][key]['frame'] for key in self.sprite_json['frames'].keys()]
        images = []
        for i in frames[start:end]:
            images.append(self.sheet.get_image(i['x'], i['y'], i['w'], i['h'], color_key=(0, 0, 0)))
        return images

    def read_json_data(self, path):
        file = open(path)
        self.sprite_json = json.load(file)
        file.close()

    def play_laser_sound(self):
        self.player_laser.play()

    def play_zoom_sound(self):
        self.player_zoom.play()

    def stop_zoom_sound(self, fade=0):
        self.player_zoom.stop()

    def play_explosion_sound(self):
        self.player_explosion.play()


class ScoreAssets:
    def __init__(self):
        self.negs = [pygame.mixer.Sound("assets/sounds/fart2.wav"), pygame.mixer.Sound("assets/sounds/fart.wav")]
        self.pos = pygame.mixer.Sound("assets/sounds/pos_score.wav")
        self.pos.set_volume(.3)
        self.font = Font(50)
        self.bold_font = self.font.mago_bold

    def play_negative(self):
        sound = choice(self.negs)
        sound.set_volume(2)
        sound.play()

    def play_positive(self):
        self.pos.play()


class SpaceManAssets:
    def __init__(self):
        self.font = Font(25)
        self.mago_bold = self.font.mago_bold
        self.sprite_json = {}
        self.sheet = SpriteSheet('assets/background/space_man/space_man.png')
        self.read_json_data('assets/background/space_man/space_man.json')
        self.images = self.get_frames(0, 10)

    def get_frames(self, start, end):
        frames = [self.sprite_json['frames'][key]['frame'] for key in self.sprite_json['frames'].keys()]
        images = []
        for i in frames[start:end]:
            img = pygame.transform.scale(
                self.sheet.get_image(i['x'], i['y'], i['w'], i['h'], color_key=(0, 0, 0)), (35, 35))
            images.append(img)
        return images

    def read_json_data(self, path):
        file = open(path)
        self.sprite_json = json.load(file)
        file.close()
