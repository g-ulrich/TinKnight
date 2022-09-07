import pygame, sys
from settings import Settings
from player import Player
from camera import CameraGroup
from background import Background
from planet import Planet, PlanetTitle
from explosion import Explosion
from sounds import Sounds
from init_fonts import Font
from small_enemy import SmallEnemy
from score import Score
from message import Message
from controls import Controls
from asset_classes import PlanetAssets
from keyboard import Keyboard


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.font = Font(15)
        self.controls = Controls()
        self.sounds = Sounds()
        self.settings = Settings()
        self.message = Message()
        self.screen = self.settings.get_screen()
        self.clock = self.settings.get_clock()
        self.camera_group = CameraGroup(self.settings, self.sounds, self.message)
        self.score = Score(self.screen, self.message)
        self.player = Player(self.settings, self.camera_group)
        self.small_enemy = SmallEnemy(self.settings)
        self.explosion = Explosion(self.settings,
                                   width=self.screen.get_width(),
                                   radius=self.screen.get_width(),
                                   color=(95, 101, 115),
                                   iterate_by=4)
        self.planet_assets = PlanetAssets()
        self.planet = Planet(self.camera_group, self.settings, self.planet_assets)
        self.planet_title = PlanetTitle(self.settings, self.planet_assets)
        # place the stars and insert into camera group
        self.keyboard = Keyboard(self.sounds)
        self.background = Background(self.settings, self.camera_group, self.planet_title, self.sounds, self.score, self.keyboard)
        self.show_title_screen = True
        self.left_click = False
        self.game_over = False
        self.player_name = ""

    def run(self):
        run = True
        self.sounds.play_music()
        while run:
            pressed = pygame.key.get_pressed()
            self.controls.activated_pressed(pressed)
            for event in pygame.event.get():
                self.controls.activated_controler(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.sounds.skip_song()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.left_click = True
                self.controls.update_joysticks(event)

            if self.show_title_screen:
                self.show_title_screen, quit_game = self.background.blit_title_screen(self.controls, self.left_click)
                self.sounds.blit_song_name(self.screen)
                self.controls.blit_controller_type(self.screen)
                if quit_game:
                    quit()
                if not self.show_title_screen:
                    self.explosion.initiate((self.screen.get_width() / 2, self.screen.get_height() / 2))
            else:
                if self.controls.obj['esc'] and not self.game_over:
                    run = self.background.blit_pause_game(self.controls)
                elif self.player.current_health_points > 0:
                    self.camera_group.update(self.controls.obj)  # update player sprite
                    self.camera_group.custom_draw(pressed, self.clock, self.player, self.background, self.score, self.small_enemy, self.planet,
                                                  self.explosion, self.controls, self.keyboard.user_text)
                else:
                    self.sounds.stop_music()
                    run = self.background.blit_game_over(self.controls, self.score)

                if not run:
                    self.sounds.stop_music()
                    self.game_over = True

            pygame.display.update()
            self.clock.tick(self.settings.get_fps())
        game = Game()
        game.run()


if __name__ == '__main__':
    game = Game()
    game.run()
