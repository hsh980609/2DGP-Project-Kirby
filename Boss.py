from pico2d import *
import game_framework
import game_world

class Boss:
    image = None
    def __init__(self):
        if Boss.image == None:
            Boss.image = load_image('Boss.png')

        self.x, self.y = 400, 100
        self.frame = 0
        self.dir = 1
        self.target = None

        pass

    def update(self):
       pass

    def draw(self, offset_x=0):  # offset_x 추가
        screen_x = self.x - offset_x

        if self.dir == 1:
            self.image.clip_draw(0, 700, 100, 100, screen_x, self.y, 100, 100)
        else:
            self.image.clip_composite_draw(0, 700, 100, 100, 0, 'h', screen_x, self.y, 100, 100)

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass
