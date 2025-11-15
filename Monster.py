from pico2d import *
import game_framework
import game_world

class Monster:
    image = None

    def __init__(self):
        if Monster.image == None:
            Monster.image = load_image('Monster.png')

        self.x, self.y = 500, 100
        pass

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(110, 120, 30, 30, self.x, self.y, 100, 100)
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass