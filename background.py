from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('Backgrounds.png')

        self.clip_w = self.image.w // 3
        self.clip_h = self.image.h // 3

        self.clip_bottom = self.clip_h * 2
    def update(self):
        pass

    def draw(self,offset_x = 0):
        self.image.clip_draw(0, self.clip_bottom, self.clip_w, self.clip_h, 400, 300, 1000, 900)

class Boss_Background:
    def __init__(self):
        self.image = load_image('boss_stage.png')

    def update(self):
        pass

    def draw(self,offset_x = 0):
        self.image.clip_draw(0, -100, self.image.w, self.image.h, 400, 300, 1200,1000)