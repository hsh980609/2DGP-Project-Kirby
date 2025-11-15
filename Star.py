from pico2d import *

class Star:
    image = None

    def __init__(self, x,y):
        if Star.image == None:
            Star.image = load_image('Star.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        pass
