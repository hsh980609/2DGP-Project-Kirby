from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
STAR_SPEED_KMPH = 60.0  # Km / Hour
STAR_SPEED_MPM = (STAR_SPEED_KMPH * 1000.0 / 60.0)
STAR_SPEED_MPS = (STAR_SPEED_MPM / 60.0)
STAR_SPEED_PPS = (STAR_SPEED_MPS * PIXEL_PER_METER)

class Star:
    image = None

    def __init__(self, x =400,y=300, dir = 1):
        if Star.image == None:
            Star.image = load_image('Star.png')
        self.x, self.y = x, y
        self.dir = dir

        game_world.add_object(self, 2)

    def draw(self):

        if self.dir ==1:
            self.image.clip_draw(593,410,30,50,self.x,self.y,100,100)
        else:
            self.image.clip_draw(593,410,30,50,self.x,self.y,100,100)

        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.dir * STAR_SPEED_PPS * game_framework.frame_time

        if self.x <0 or self.x >800:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        if group == 'star:monster':
            print(f'충돌!')
            game_world.remove_object(self)
        elif group == 1:
            pass
        pass
