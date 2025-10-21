from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a


class Idle:
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


class Kirby:
    def __init__(self):
        self.img = load_image('walk_sheet.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.FLY = Fly(self)
        self.SUCTION = Suction(self)
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self):
        pass