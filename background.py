from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('Backgrounds.png')
        full_w = self.image.w
        full_h = self.image.h

        self.clip_w = full_w // 3
        self.clip_h = full_h // 3

        self.clip_bottom = self.clip_h * 2
    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, self.clip_bottom, self.clip_w, self.clip_h, 400, 300, 1000, 900)
        #self.image.clip_draw(0,self.clip_bottom, self.clip_w, self.clip_h, 1200, 30)

