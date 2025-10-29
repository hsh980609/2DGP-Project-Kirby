from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Idle:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self, e):
        self.Kirby.dir=0

    def do(self):
        self.Kirby.frame =(self.Kirby.frame +1) % 10

    def exit(self,e):
        pass
    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(self.Kirby.frame * 25, 3360, 25, 25, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(self.Kirby.frame * 25, 3360, 25, 25, 0,'h', self.Kirby.x, self.Kirby.y,100,100)


class Run:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self,e):
        if right_down(e) or left_up(e):
            self.Kirby.dir = self.Kirby.face_dir = 1
        elif left_down(e) or right_up(e):
            self.Kirby.dir = self.Kirby.face_dir = -1

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + 1) % 8
        self.Kirby.x += self.Kirby.dir * 15

    def exit(self,e):
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(5 + self.Kirby.frame * 24, 3245, 23, 23, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(5 + self.Kirby.frame * 24, 3245, 23, 23, 0, 'h', self.Kirby.x, self.Kirby.y,100,100)

class Jump:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self,e):
        self.Kirby.dir = 0

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + 1) % 10

    def exit(self,e):
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(self.Kirby.frame * 26, 3290, 25, 25, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_draw(self.Kirby.frame * 25, 0, 25, 25, self.Kirby.x, self.Kirby.y,100,100)




class Fly:
    def __init__(self):
        pass

    def enter(self):
        pass

    def do(self):
        pass

    def exit(self):
        pass


class Suction:
    def __init__(self):
        pass

    def enter(self):
        pass

    def do(self):
        pass

    def exit(self):
        pass


class Walk:
    def __init__(self):
        pass

    def enter(self):
        pass

    def do(self):
        pass

    def exit(self):
        pass
    def draw(self):
        pass


class Kirby:
    def __init__(self):
        self.x, self.y =400, 100
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('Kirby_sheet.png')

        self.IDLE = Idle(self)
        # self.WALK = Walk(self)
        self.RUN = Run(self)
        # self.FLY = Fly(self)
        # self.SUCTION = Suction(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE :{right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN :{right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},

             }

        )


    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()
        pass

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass