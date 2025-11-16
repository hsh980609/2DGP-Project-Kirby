from pico2d import *

class Stage:
    def __init__(self):
        self.image = load_image('Stage.png')

        self.clip_w = self.image.w // 3
        self.clip_h = self.image.h // 3

        self.clip_bottom = self.clip_h * 2
        self.x=400
        self.y=-30

    def update(self):
        pass

    def draw(self,offset_x = 0):
        screen_x = self.x - offset_x
        self.image.clip_draw(0, self.clip_bottom, self.clip_w, self.clip_h, screen_x, self.y, 1000, 700)