from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_c, SDLK_x, SDLK_z

import game_framework

from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x
def x_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_x
def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z
def z_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_z
def c_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def c_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

TIME_PER_ACTION = 0.5 # 한번의 액션재생에 0.5초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 1초에 2번 액션 수행
IDLE_FRAMES_PER_ACTION = 10
RUN_FRAMES_PER_ACTION = 8
JUMP_FRAMES_PER_ACTION = 10

class Idle:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self, e):
        self.Kirby.dir=0

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + IDLE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10

    def exit(self,e):
        pass
    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(int(self.Kirby.frame) * 25, 3360, 25, 25, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(int(self.Kirby.frame) * 25, 3360, 25, 25, 0,'h', self.Kirby.x, self.Kirby.y,100,100)


class Run:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self,e):
        if right_down(e) or left_up(e):
            self.Kirby.dir = self.Kirby.face_dir = 1
        elif left_down(e) or right_up(e):
            self.Kirby.dir = self.Kirby.face_dir = -1

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + RUN_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.Kirby.x += self.Kirby.dir * 1

    def exit(self,e):
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(5 + int(self.Kirby.frame) * 24, 3245, 23, 23, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(5 + int(self.Kirby.frame) * 24, 3245, 23, 23, 0, 'h', self.Kirby.x, self.Kirby.y,100,100)

class Jump:
    def __init__(self, Kirby):
        self.Kirby = Kirby
        self.jump_height = 10
        self.gravity = 1

    def enter(self,e):
        self.Kirby.dir = 0
        self.Kirby.frame = 0
        self.Kirby.y_start = self.jump_height

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + JUMP_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        self.Kirby.y += self.Kirby.y_start
        self.Kirby.y_start -=self.gravity

        # 땅에 닿았는지 확인
        if self.Kirby.y <=90:
            self.Kirby.y = 90
            self.Kirby.y_start = 0

            self.Kirby.state_machine.change_state(self.Kirby.IDLE)


    def exit(self,e):
        self.Kirby.y_start = 0

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(int(self.Kirby.frame) * 26, 3290, 26, 26, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(int(self.Kirby.frame) * 26, 3290, 26, 26, 0,'h', self.Kirby.x, self.Kirby.y,100,100)


class Fly:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self, e):
        pass


    def do(self):
        self.Kirby.frame = (self.Kirby.frame + 1) % 6
        self.Kirby.x += self.Kirby.dir * 15

    def exit(self, e):
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(self.Kirby.frame * 30, 3158, 30, 29, self.Kirby.x, self.Kirby.y, 100, 100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(self.Kirby.frame * 25, 3158, 23, 25, 0, 'h', self.Kirby.x,
                                                 self.Kirby.y, 100, 100)


class Suction:
    def __init__(self, Kirby):
        self.Kirby = Kirby
        self.wait_time = 0

    def enter(self, e):
        self.Kirby.dir=0
        self.Kirby.frame = 0
        self.wait_time = 0

    def do(self):
        self. wait_time += 1

        if self.wait_time >= 2:
            self.wait_time = 0

            if self.Kirby.frame < 4:
                self.Kirby.frame += 1
            self.Kirby.frame = (self.Kirby.frame) % 5


    def exit(self, e):
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(self.Kirby.frame * 27, 3217, 27, 27, self.Kirby.x, self.Kirby.y, 100, 100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(self.Kirby.frame * 27, 3217, 27, 27, 0, 'h', self.Kirby.x,
                                                 self.Kirby.y, 100, 100)


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
        self.x, self.y =400, 90
        self.y_start = 0

        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('Kirby_sheet.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.FLY = Fly(self)
        self.SUCTION = Suction(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE :{z_down: self.SUCTION,x_down: self.JUMP, right_up: self.RUN, right_down: self.RUN, left_up: self.RUN, left_down: self.RUN,},
                self.RUN :{right_down: self.IDLE, right_up: self.IDLE,left_down: self.IDLE, left_up: self.IDLE,},
                self.JUMP:{c_down:self.FLY},
                self.SUCTION:{z_up:self.IDLE},
                self.FLY:{c_up:self.IDLE}

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