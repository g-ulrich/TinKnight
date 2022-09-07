import pygame
from init_fonts import Font
from datetime import datetime
from random import choice
from bible_names import BIBLE_NAMES
from asset_classes import KeyboardAssets


class Keyboard:
    def __init__(self, sounds):
        self.sounds = sounds
        self.text = []
        self.start_dt = datetime.now()
        self.secondary_font = Font(50)
        self.user_text = ''
        self.input_rect = pygame.Rect(200, 200, 80, 3)
        self.color_active = pygame.Color((127, 127, 127))
        self.color_passive = pygame.Color((255, 255, 255))
        self.color = self.color_passive
        self.count = 0
        self.active = True
        self.assets = KeyboardAssets()
        self.search_noun = BIBLE_NAMES
        self.user_text += choice(self.search_noun)

    def blit_quit_btn(self, surface, title_rect, controls):
        btn_rect = pygame.Rect(0, 0, title_rect.w / 2, 50)
        btn_rect.x = title_rect.bottomright[0] - (btn_rect.w - 10)
        btn_rect.y = title_rect.bottomright[1] + 85
        rect = btn_rect
        text_quit = " QUIT (-)" if controls.joysticks else "   QUIT"
        text = self.secondary_font.mago_bold.render(text_quit, True, (255, 255, 255))
        pygame.draw.rect(surface, (71, 77, 91), rect)
        pygame.draw.rect(surface, (95, 101, 115), (rect.x, (rect.y + rect.h) - 5, rect.w, 5))
        pygame.draw.rect(surface, (120, 126, 141), ((rect.x + rect.w) - 5, rect.y, 5, rect.h))
        surface.blit(text, (rect.x + (rect.w / 6) + 10, rect.y))
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos):
            # for keyboard
            pygame.draw.rect(surface, (71, 77, 91), rect)
            pygame.draw.rect(surface, (120, 126, 141), (rect.x, rect.y, rect.w, 5))
            pygame.draw.rect(surface, (95, 101, 115), (rect.x, rect.y, 5, rect.h))
            surface.blit(text, (rect.x + (rect.w / 6) + 5, rect.y + 5))
            return True
        elif controls.joysticks and controls.obj['esc']:
            # for joysticks
            pygame.draw.rect(surface, (71, 77, 91), rect)
            pygame.draw.rect(surface, (120, 126, 141), (rect.x, rect.y, rect.w, 5))
            pygame.draw.rect(surface, (95, 101, 115), (rect.x, rect.y, 5, rect.h))
            surface.blit(text, (rect.x + (rect.w / 6) + 5, rect.y + 5))
            return True
        return False

    def blit_start_btn(self, surface, title_rect, controls):
        btn_rect = pygame.Rect(0, 0, title_rect.w / 2, 50)
        btn_rect.x = title_rect.bottomleft[0] - 10
        btn_rect.y = title_rect.bottomleft[1] + 85
        rect = btn_rect
        text_start = "    START (+)" if controls.joysticks else "      START"
        text = self.secondary_font.mago_bold.render(text_start, True, (255, 255, 255))
        pygame.draw.rect(surface, (71, 77, 91), rect)
        pygame.draw.rect(surface, (95, 101, 115), (rect.x, (rect.y + rect.h) - 5, rect.w, 5))
        pygame.draw.rect(surface, (120, 126, 141), ((rect.x + rect.w) - 5, rect.y, 5, rect.h))
        surface.blit(text, (rect.x, rect.y))
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos):
            # for keyboard
            pygame.draw.rect(surface, (71, 77, 91), rect)
            pygame.draw.rect(surface, (120, 126, 141), (rect.x, rect.y, rect.w, 5))
            pygame.draw.rect(surface, (95, 101, 115), (rect.x, rect.y, 5, rect.h))
            surface.blit(text, (rect.x + 5, rect.y + 5))
            return True
        elif controls.joysticks and controls.obj['restart']:
            # for joysticks
            pygame.draw.rect(surface, (71, 77, 91), rect)
            pygame.draw.rect(surface, (120, 126, 141), (rect.x, rect.y, rect.w, 5))
            pygame.draw.rect(surface, (95, 101, 115), (rect.x, rect.y, 5, rect.h))
            surface.blit(text, (rect.x + 5, rect.y + 5))
            return True
        return False

    def get_letter(self, pressed):
        text = ""
        for letter in self.assets.letters:
            code = letter['item']
            let = letter['let']
            if pressed[code]:
                self.sounds.play_menu_select()
                text += let
        return text.upper()

    def type_name(self, surface, controls, title_obj):
        self.count += .08
        if round(self.count) == 1:
            self.count = 0
            char = self.get_letter(controls.obj['pressed'])
            if controls.obj['pressed'][pygame.K_BACKSPACE]:
                self.color = self.color_passive
                # self.user_text = self.user_text[:-1]
                self.user_text = ""
            elif char != "" and self.active:
                self.color = self.color_active
                self.user_text = self.user_text + char if len(self.user_text) < 25 else self.user_text

        self.input_rect.w = title_obj.get_width() / 2
        self.input_rect.x = (surface.get_width() / 2) - 40
        self.input_rect.y = surface.get_height() / 2
        pygame.draw.rect(surface, self.color, self.input_rect)
        text = self.secondary_font.mago_bold.render(self.user_text, True, (255, 255, 255))
        surface.blit(text, (self.input_rect.x, self.input_rect.y - text.get_height()))
        text_bg = self.secondary_font.mago_bold.render("  ENTER NAME:", True, (0, 0, 0))
        text = self.secondary_font.mago_bold.render("  ENTER NAME:", True, (255, 255, 255))
        surface.blit(text_bg, (((surface.get_width() / 2) - title_obj.get_width() / 2) - 4,
                            (self.input_rect.y - text.get_height()) - 4))
        surface.blit(text, ((surface.get_width() / 2) - title_obj.get_width() / 2,
                            self.input_rect.y - text.get_height()))
        if text.get_width() >= self.input_rect.w - 50:
            self.active = False
        else:
            self.active = True