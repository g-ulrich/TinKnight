import pygame
from asset_classes import PlayerAssets
from random import randint, choice


class MiniMap:
    def __init__(self, settings):
        self.level_rect = settings.level_rect
        self.screen = settings.screen
        self.assets = PlayerAssets()
        # divide by = divide screen size by for minimap
        self.divide_by = 15
        self.map_offset = 10
        map_topleft = self.screen.get_width() - self.map_offset - self.level_rect.width / self.divide_by
        self.map_rect = pygame.Rect(map_topleft, self.map_offset,
                                    self.level_rect.width / self.divide_by,
                                    self.level_rect.height / self.divide_by)
        self.screen_offset = (self.screen.get_width() * .485, self.screen.get_height() * .48)
        self.player_pos = pygame.math.Vector2()

    def blit_player_pos(self, surface, offset, internal_offset, mines_pos, small_enemies):
        pos = (offset + internal_offset) + self.screen_offset
        self.player_pos = pygame.math.Vector2(pos)
        pos_text = self.assets.bold_font.render(f"Pos: ({round(self.player_pos.x)}, {round(self.player_pos.y)})", True, (255, 255, 255))
        surface.blit(pos_text,
                     (self.screen.get_width() - (pos_text.get_width() + self.map_offset),
                      self.map_offset + self.map_rect.height + 2))
        self.blit_mini_map(surface, (offset + internal_offset) + self.screen_offset, mines_pos, small_enemies)

    def blit_mini_map(self, surface, offset, mines_pos, small_enemies):
        # player map
        pygame.draw.rect(surface, (50, 50, 50), self.map_rect)
        # player map border
        pygame.draw.rect(surface, (255, 255, 255), self.map_rect, 2)
        # quadrants
        pygame.draw.rect(surface, (60, 60, 60), (self.map_rect.centerx, self.map_offset + 2, 1, self.map_rect.height - 4))
        pygame.draw.rect(surface, (60, 60, 60), (self.map_rect.x + 2, self.map_rect.centery, self.map_rect.width - 4, 1))
        # blit planet dot
        pygame.draw.circle(surface, (79, 164, 255), (self.map_rect.centerx, self.map_rect.centery), 5.5)
        # player dot
        px, py = offset[0] / self.divide_by, offset[1] / self.divide_by
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(px + self.map_rect.centerx, py + self.map_rect.centery, 5, 5))
        # # mines dot
        # for pos in mines_pos:
        #     mx, my = pos[0] / self.divide_by, pos[1] / self.divide_by
        #     pygame.draw.circle(surface, (168,169,173), (mx + self.map_rect.centerx, my + self.map_rect.centery), 3.0)

        enemy_color = choice([(200, 0, 0), (200, 0, 0), (150, 0, 0)])
        for enemy in small_enemies:
            try:
                ex, ey = enemy['rect'].x / self.divide_by, enemy['rect'].y / self.divide_by
                pygame.draw.circle(surface, enemy_color, (ex + self.map_rect.centerx, ey + self.map_rect.centery), 3.0)
            except:
                pass