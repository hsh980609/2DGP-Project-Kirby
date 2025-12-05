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
        screen_w = get_canvas_width()
        screen_h = get_canvas_height()

        center_x = screen_w // 2
        center_y = screen_h // 2
        self.image.clip_draw(0, self.clip_bottom, self.clip_w, self.clip_h, center_x, center_y, screen_w * 1.2, screen_h * 1.2)

class Boss_Background:
    def __init__(self):
        self.image = load_image('boss_stage.png')

    def update(self):
        pass

    def draw(self,offset_x = 0):
        screen_w = get_canvas_width()
        screen_h = get_canvas_height()

        center_x = screen_w // 2
        center_y = screen_h // 2

        self.image.draw(center_x, center_y, screen_w * 1.2, screen_h*1.2)