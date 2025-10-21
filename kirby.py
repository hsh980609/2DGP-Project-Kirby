from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

from state_machine import StateMachine

class Idle:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self):
        self.Kirby.dir=0

    def do(self):
        self.Kirby.frame =(self.Kirby.frame +1) % 7

    def exit(self):
        pass
    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(self.Kirby.frame * 25, 0, 25, 25, self.Kirby.x, self.Kirby.y)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_draw(self.Kirby.frame * 25, 0, 100, 100, self.Kirby.x, self.Kirby.y)


class Run:
    def __init__(self):
        pass

    def enter(self):
        pass

    def do(self):
        pass

    def exit(self):
        pass


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
        self.image = load_image('idle_sheet.png')

        self.IDLE = Idle(self)
        # self.WALK = Walk(self)
        # self.RUN = Run(self)
        # self.FLY = Fly(self)
        # self.SUCTION = Suction(self)

        self.state_machine = StateMachine(
            self.IDLE,
        )


    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()
        pass

    def handle_event(self):
        pass