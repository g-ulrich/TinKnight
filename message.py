from init_fonts import Font
import pygame
from datetime import datetime


class Message:
    def __init__(self):
        self.screen_offset = 10
        self.message = ""
        self.big_message = ""
        self.secondary_font = Font(50)
        self.big_font = Font(100)
        self.message_timer = datetime.now()
        self.white = 255

    def init_message(self, message, big_message=""):
        if message != self.message or big_message != self.big_message:
            self.reset_message_variables()
        self.message = message
        self.big_message = big_message

    def iterate_message(self, surface):
        if (datetime.now() - self.message_timer).total_seconds() < 2:
            self.blit_message(surface)
        else:
            self.reset_message_variables()

    def reset_message_variables(self):
        self.message = ""
        self.big_message = ""
        self.white = 255
        self.message_timer = datetime.now()

    def blit_message(self, surface):
        half_w = surface.get_width() / 2
        half_h = surface.get_height() / 2
        self.white -= 2
        if self.message != "":
            # top middle message
            text = self.secondary_font.mago_bold.render(self.message, True, (self.white, self.white, self.white))
            text_rect = text.get_rect()
            half_text_w = text_rect.w / 2
            surface.blit(text, (half_w - half_text_w, self.screen_offset))
        if self.big_message != "":
            # middle screen
            text = self.big_font.mago_bold.render(self.big_message, True, (self.white, self.white, self.white))
            text_rect = text.get_rect()
            half_text_w = text_rect.w / 2
            surface.blit(text, (half_w - half_text_w, (half_h + self.screen_offset) - (text_rect.h / 2)))

