from asset_classes import ScoreAssets
from datetime import datetime


class Score:
    def __init__(self, screen, message):
        self.assets = ScoreAssets()
        self.message = message
        self.start_time = datetime.now()
        # self.screen = screen
        self.score = 0
        self.screen_offset = 10

    def update_score(self, num):
        if num < 0:
            self.message.init_message(f"{num}")
            self.assets.play_negative()
        elif num > 0:
            self.message.init_message(f"+{num}")
            self.assets.play_positive()
        self.score += num

    def add_time(self):
        secs = (datetime.now() - self.start_time).total_seconds()
        text = f"TIME: {round(secs, 2)}s"
        if secs > 60.0:
            text = f"TIME: {round(secs / 60, 2)}m"
        return text

    def blit_score(self, surface):
        self.message.iterate_message(surface)
        text = self.assets.bold_font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        x, y = self.screen_offset, self.screen_offset + 60
        surface.blit(text, (x, y))
        text = self.assets.bold_font.render(self.add_time(), True, (255, 255, 255))
        surface.blit(text, (x, y + 60))
