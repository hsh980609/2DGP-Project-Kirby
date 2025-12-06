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

class Ground:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y # 발판의 중심
        self.w, self.h = w, h # 발판의 w, h

    def get_bb(self):
        return self.x - self.w // 2, self.y - self.h // 2, self.x + self.w // 2, self.y + self.h // 2

    def update(self):
        pass

    def draw(self, offset_x=0):
        # l, b, r, t = self.get_bb()
        # draw_rectangle(l - offset_x, b, r - offset_x, t)
        pass

    # 발판은 충돌 당해도 아무것도 하지 않음
    def handle_collision(self, group, other):
        pass
