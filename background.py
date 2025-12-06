from pico2d import *
import common

class Background:
    def __init__(self):
        self.image = load_image('resources/map/Backgrounds.png')

        self.clip_w = self.image.w // 3
        self.clip_h = self.image.h // 3
        self.clip_bottom = self.clip_h * 2

    def update(self):
        pass

    def draw(self,offset_x = 0):

        center_x = common.SCREEN_WIDTH // 2
        center_y = common.SCREEN_HEIGHT // 2
        self.image.clip_draw(0, self.clip_bottom, self.clip_w, self.clip_h, center_x, center_y, common.SCREEN_WIDTH * 1.2, common.SCREEN_HEIGHT * 1.2)

class Boss_Background:
    def __init__(self):
        self.image = load_image('resources/map/boss_stage.png')

    def update(self):
        pass

    def draw(self,offset_x = 0):
        center_x = common.SCREEN_WIDTH // 2
        center_y = common.SCREEN_HEIGHT // 2

        self.image.draw(center_x, center_y, common.SCREEN_WIDTH * 1.2, common.SCREEN_HEIGHT * 1.2)