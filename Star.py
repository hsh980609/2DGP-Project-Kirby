from pico2d import *

class Star:
    image = None

    def __init__(self, x =400,y=300):
        if Star.image == None:
            Star.image = load_image('Star.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.clip_draw(593,410,30,50,self.x,self.y,100,100)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        pass
