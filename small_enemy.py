import pygame
from asset_classes import EnemyAssets
from random import choice, randint
from explosion import Explosion


class SmallEnemy:
    def __init__(self, settings):
        self.planet_center_pos = (125, 125)
        self.settings = settings
        self.level_rect = settings.level_rect
        self.screen = settings.screen
        self.assets = EnemyAssets()
        self.init_health_points_small = 10
        self.init_health_points_large = 30
        self.screen_offset = 10
        self.explosion = Explosion(settings, color=(255, 50, 50))
        self.kills = 0
        self.enemies = []
        self.enemies_append = self.enemies.append
        for index in range(5):
            pos = pygame.math.Vector2((randint(self.level_rect.topleft[0], self.level_rect.bottomright[0]),
                                       randint(self.level_rect.topleft[1], self.level_rect.bottomright[1])))
            if choice([True, False, False, False, False]):
                self.enemies_append({'img': pygame.transform.scale(choice(self.assets.enemy_ships), (100, 100)),
                                     'hp': self.init_health_points_large,
                                     'speed': randint(1, 2),
                                     'rect': pygame.Rect(pos.x, pos.y, 100, 100),
                                     'rotation': randint(0, 360),
                                     'damage': .2,
                                     'score': 250,
                                     'hit': False,
                                     'track': choice(['player', 'planet']),
                                     'side': choice(['right', 'top', 'bottom', 'left'])})
            else:
                self.enemies_append({'img': pygame.transform.scale(choice(self.assets.enemy_ships), (64, 64)),
                                 'hp': self.init_health_points_small,
                                 'speed': randint(1, 3),
                                 'rect': pygame.Rect(pos.x, pos.y, 64, 64),
                                 'rotation': randint(0, 360),
                                 'damage': .1,
                                 'score': 10,
                                  'hit': False,
                                 'track': choice(['player', 'planet']),
                                 'side': choice(['right', 'top', 'bottom', 'left'])})

    def add_new_enemy(self):
        pos = pygame.math.Vector2((randint(self.level_rect.topleft[0], self.level_rect.bottomright[0]),
                                   randint(self.level_rect.topleft[1], self.level_rect.bottomright[1])))
        if choice([True, False, False, False, False]):
            self.enemies_append({'img': pygame.transform.scale(choice(self.assets.enemy_ships), (100, 100)),
                                 'hp': self.init_health_points_large,
                                 'speed': randint(1, 2),
                                 'rect': pygame.Rect(pos.x, pos.y, 100, 100),
                                 'rotation': randint(0, 360),
                                 'track': choice(['player', 'planet']),
                                 'score': 250,
                                 'hit': False,
                                 'damage': .2,
                                 'side': choice(['right', 'top', 'bottom', 'left'])})
        else:
            self.enemies_append({'img': pygame.transform.scale(choice(self.assets.enemy_ships), (64, 64)),
                                 'hp': self.init_health_points_small,
                                 'speed': randint(2, 5),
                                 'rect': pygame.Rect(pos.x, pos.y, 64, 64),
                                 'rotation': randint(0, 360),
                                 'track': choice(['player', 'planet']),
                                 'damage': .1,
                                 'score': 10,
                                 'hit': False,
                                 'side': choice(['right', 'top', 'bottom', 'left'])})

    def enemy_movement(self, surface, index, enemy, player, player_r, planet, planet_r, offset, internal_offset, controls):
        num_enemies = len(self.enemies)
        if enemy['track'] == 'player':
            e = enemy['rect'].topleft - offset + internal_offset
            speed = enemy['speed']
            if player_r.collidepoint(e):
                if choice([True, False, False, False]):
                    pygame.draw.line(surface, (randint(230, 255), 200, 200),
                                     enemy['rect'].center - offset + internal_offset,
                                     player_r.center, 10 if enemy['score'] == 10 else 30)
                    pygame.draw.line(surface, (randint(200, 255), 0, 0),
                                     enemy['rect'].center - offset + internal_offset,
                                     player_r.center, 4 if enemy['score'] == 10 else 12)
                pygame.draw.circle(surface, choice([(randint(150, 255), 0, 0), (255, 200, 200)]), player.rect.center - offset + internal_offset, randint(5, 10))
                player.current_health_points -= .5
                controls.start_rumble()
                speed = 0

            if enemy['side'] == "right":
                px, py = player_r.midright
                enemy['rect'].x = enemy['rect'].x + speed if e.x <= px - 16 else enemy['rect'].x - speed
                enemy['rect'].y = enemy['rect'].y + speed if e.y <= py - 16 else enemy['rect'].y - speed
            elif enemy['side'] == "left":
                px, py = player_r.midleft
                enemy['rect'].x = enemy['rect'].x + speed if e.x <= px - 16 else enemy['rect'].x - speed
                enemy['rect'].y = enemy['rect'].y + speed if e.y <= py - 16 else enemy['rect'].y - speed
            elif enemy['side'] == "bottom":
                px, py = player_r.midbottom
                enemy['rect'].x = enemy['rect'].x + speed if e.x <= px - 16 else enemy['rect'].x - speed
                enemy['rect'].y = enemy['rect'].y + speed if e.y <= py - 16 else enemy['rect'].y - speed
            elif enemy['side'] == "top":
                px, py = player_r.midtop
                enemy['rect'].x = enemy['rect'].x + speed if e.x <= px - 16 else enemy['rect'].x - speed
                enemy['rect'].y = enemy['rect'].y + speed if e.y <= py - 16 else enemy['rect'].y - speed
        if enemy['track'] == 'planet':
            e = enemy['rect'].topleft - offset + internal_offset
            speed = enemy['speed']
            if planet_r.collidepoint(e):
                if choice([True, False, False, False]):
                    pygame.draw.line(surface, (randint(240, 255), 200, 200),
                                     enemy['rect'].center - offset + internal_offset,
                                     planet_r.center,  10 if enemy['score'] == 10 else 30)
                    pygame.draw.line(surface, (randint(200, 255), 0, 0),
                                     enemy['rect'].center - offset + internal_offset,
                                     planet_r.center, 4 if enemy['score'] == 10 else 12)
                pygame.draw.circle(surface, choice([(randint(150, 255), 0, 0), (255, 200, 200)]), planet.rect.center - offset + internal_offset, randint(31 + num_enemies, 48 + num_enemies))
                planet.current_health_points -= .05
                speed = 0

            if enemy['side'] == "right":
                px, py = planet_r.midright
                enemy['rect'].x = enemy['rect'].x + speed if e.x <= px - 16 else enemy['rect'].x - speed
                enemy['rect'].y = enemy['rect'].y + speed if e.y <= py - 16 else enemy['rect'].y - speed
            elif enemy['side'] == "left":
                px, py = planet_r.midleft
                enemy['rect'].x = enemy['rect'].x + speed if e.x <= px - 16 else enemy['rect'].x - speed
                enemy['rect'].y = enemy['rect'].y + speed if e.y <= py - 16 else enemy['rect'].y - speed
            elif enemy['side'] == "bottom":
                px, py = planet_r.midbottom
                enemy['rect'].x = enemy['rect'].x + speed if e.x <= px - 16 else enemy['rect'].x - speed
                enemy['rect'].y = enemy['rect'].y + speed if e.y <= py - 16 else enemy['rect'].y - speed
            elif enemy['side'] == "top":
                px, py = planet_r.midtop
                enemy['rect'].x = enemy['rect'].x + speed if e.x <= px - 16 else enemy['rect'].x - speed
                enemy['rect'].y = enemy['rect'].y + speed if e.y <= py - 16 else enemy['rect'].y - speed

    def blit_enemy_count(self, surface):
        text = self.assets.bold_font.render(f"ENEMIES: {len(self.enemies)}", True, (255, 255, 255))
        x, y = self.screen_offset, self.screen_offset + 90
        surface.blit(text, (x, y))

    def blit_enemy(self, surface, planet, player, score, offset, internal_offset, controls):
        self.blit_enemy_count(surface)
        self.explosion.iterate(surface, offset + internal_offset)
        planet_rect_peri = pygame.Rect(planet.pos.x - 50, planet.pos.y - 50, planet.assets.planet_size + 100,
                                       planet.assets.planet_size + 100)
        ppos = player.rect.topleft - offset + internal_offset
        player_rect_peri = pygame.Rect(ppos[0] - 10, ppos[1] - 10, player.rect.w + 20, player.rect.h + 20)
        for index, enemy in enumerate(self.enemies, 0):
            self.enemies[index]['rotation'] += .5
            rotated_img = pygame.transform.rotate(enemy['img'], self.enemies[index]['rotation'])

            self.enemy_movement(surface, index, enemy, player, player_rect_peri, planet, planet_rect_peri, offset,
                                internal_offset, controls)
            x, y = enemy['rect'].topleft - offset + internal_offset
            if enemy['hit']:
                pygame.draw.rect(surface, (127, 127, 127), pygame.Rect(x + (enemy['rect'].w / 3), y - 10,
                    (self.init_health_points_small if enemy['score'] == self.init_health_points_small else self.init_health_points_large) * 4, 3))
                pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(x + (enemy['rect'].w / 3), y - 10, enemy['hp'] * 4, 3))

            surface.blit(rotated_img, (x, y))

    def enemy_hit(self, surface, player, score, offset, internal_offset):
        enemies_killed = []
        for b_index, pb in enumerate(player.boom, 0):
            for e_index, enemy in enumerate(self.enemies, 0):
                if enemy['rect'].colliderect(pb['rect']):
                    try:
                        del player.boom[b_index]
                    except:
                        pass
                    self.enemies[e_index]['hit'] = True
                    e_rotate = pygame.transform.rotate(self.assets.white_quare_sheet.get_image(0, 0, enemy['rect'].w, enemy['rect'].h), enemy['rotation'])
                    surface.blit(e_rotate, enemy['rect'].topleft - offset + internal_offset)
                    self.enemies[e_index]['hp'] -= player.bullet_width * 2
                    if self.enemies[e_index]['hp'] <= 0:
                        self.kills += 1
                        del self.enemies[e_index]
                        self.explosion.initiate(enemy['rect'].center)
                        self.assets.play_explosion()
                        # only add enemy if big guy is killed
                        if enemy['score'] > 10 or randint(0, 5) == 1:
                            enemies_killed.append(enemy['score'])
        if enemies_killed:
            score.update_score(sum(enemies_killed))
            for i in range(len(enemies_killed)):
                for index in range(5):
                    self.add_new_enemy()

    def kill_half(self):
        """
        if called
        """
        for index in range(len(self.enemies)):
            try:
                del self.enemies[index]
            except:
                pass