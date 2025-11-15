from pico2d import *
import game_framework
import game_world

class Monster:
    image = None

    def __init__(self):
        if Monster.image == None:
            Monster.image = load_image('Monster.png')

        self.x, self.y = 800, 90
        pass

    def update(self):
        pass

    def draw(self):
        # Placeholder for drawing the monster
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass