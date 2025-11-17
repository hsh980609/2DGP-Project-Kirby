from pico2d import *

class Stage:
    def __init__(self):
        self.image = load_image('Stage_1.png')

        self.clip_w = self.image.w
        self.clip_h = self.image.h

        self.x = self.clip_w // 2
        self.y= 150

    def update(self):
        pass

    def draw(self,offset_x = 0):
        screen_x = self.x - offset_x

        self.image.clip_draw(0, 0, 1040, 180, screen_x, self.y, 3000, 600)
