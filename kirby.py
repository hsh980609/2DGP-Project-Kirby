import time
from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_DOWN, SDLK_UP, SDLK_c, SDLK_x, SDLK_z

import game_world
import game_framework
from state_machine import StateMachine
from Star import Star

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN
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
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
# Kirby Run Speed
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Kirby Fly Speed
FLY_SPEED_KMPH = 20.0  # Km / Hour
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

# Kirby Walk Speed
WALK_SPEED_KMPH = 20.0  # Km / Hour
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

# 충돌시 넉백 속도
KNOCKBACK_SPEED_KMPH = 10.0  # 넉백 속도
KNOCKBACK_SPEED_MPM = (KNOCKBACK_SPEED_KMPH * 1000.0 / 60.0)
KNOCKBACK_SPEED_MPS = (KNOCKBACK_SPEED_MPM / 60.0)
KNOCKBACK_SPEED_PPS = (KNOCKBACK_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5 # 한번의 액션재생에 0.5초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 1초에 2번 액션 수행
SLEEP_FRAMES_PER_ACTION = 3
IDLE_FRAMES_PER_ACTION = 2
WALK_FRAMES_PER_ACTION = 8
RUN_FRAMES_PER_ACTION = 8
RUN_STOP_FRAMES_PER_ACTION = 1
JUMP_FRAMES_PER_ACTION = 10
FLY_FRAMES_PER_ACTION = 6
SUCTION_FRAMES_PER_ACTION = 5

MAP_CEILING_Y = 600.0 # 맵 천장
MAP_FLOOR_Y = 100.0 # 맵 바닥.

class Sleep:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self,e):
        pass

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + SLEEP_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    def exit(self,e):
        pass
    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(140 + int(self.Kirby.frame) * 25, 922, 25, 25, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(140 + int(self.Kirby.frame) * 25, 922, 25, 25, 0,'h', self.Kirby.x, self.Kirby.y,100,100)

class Idle:
    def __init__(self, Kirby):
        self.Kirby = Kirby

        # 더블탭 위한 변수
        self.entry_time = 0
        self.double_tap_time = 0.1
        self.can_double_tap = False

    def enter(self, e):
        self.Kirby.dir=0

        # 상태 진입할때 타이머 켜기
        self.entry_time = time.time()
        self.can_double_tap = True

        # sleep 타이머 변수
        self.Kirby.wait_time = get_time()

    def do(self):
        # 0.3초 지나면 더블탭flag 끄기
        if self.can_double_tap and time.time() - self.entry_time > self.double_tap_time:
            self.can_double_tap = False

        self.Kirby.frame = (self.Kirby.frame + IDLE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        if get_time() - self.Kirby.wait_time > 5:
            self.Kirby.state_machine.handle_state_event(('TIMEOUT', None))

    def exit(self,e):
        self.can_double_tap = False # 상태끝날때 초기화
        self.Kirby.last_state = 0


    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(int(self.Kirby.frame) * 25, 3360, 25, 25, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(int(self.Kirby.frame) * 25, 3360, 25, 25, 0,'h', self.Kirby.x, self.Kirby.y,100,100)

class Walk:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self,e):
        if e:
            if right_down(e):
                self.Kirby.dir = self.Kirby.face_dir = 1
            elif left_down(e):
                self.Kirby.dir = self.Kirby.face_dir = -1
        # e가 없으면 Jump에서 쓰던 dir 유지

    def do(self):

        self.Kirby.frame = (self.Kirby.frame + WALK_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.Kirby.x += self.Kirby.dir * WALK_SPEED_PPS * game_framework.frame_time

    def exit(self,e):
        self.Kirby.last_state = 0 # walk
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(4 + int(self.Kirby.frame) * 24, 3266, 23, 23, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(4 + int(self.Kirby.frame) * 24, 3266, 23, 23, 0, 'h', self.Kirby.x, self.Kirby.y,100,100)

class Run:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self,e):
        if e:
            if right_down(e):
                self.Kirby.dir = self.Kirby.face_dir = 1
            elif left_down(e):
                self.Kirby.dir = self.Kirby.face_dir = -1
        # e가 없으면 Jump에서 쓰던 dir 유지

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + RUN_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.Kirby.x += self.Kirby.dir * RUN_SPEED_PPS * game_framework.frame_time

    def exit(self,e):
        self.Kirby.last_state = 1 # run
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(5 + int(self.Kirby.frame) * 24, 3241, 23, 23, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(5 + int(self.Kirby.frame) * 24, 3241, 23, 23, 0, 'h', self.Kirby.x, self.Kirby.y,100,100)

class Run_Stop:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self,e):
        self.Kirby.frame = 0

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + RUN_STOP_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        self.Kirby.x += self.Kirby.dir * RUN_SPEED_PPS * 0.1 * game_framework.frame_time

        if self.Kirby.frame >= 1:
            self.Kirby.frame = 1

            self.Kirby.state_machine.handle_state_event(('TIMEOUT', None))

    def exit(self,e):
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(200 + int(self.Kirby.frame) * 23, 3241, 23, 24, self.Kirby.x, self.Kirby.y,100,100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(200 + int(self.Kirby.frame) * 23, 3241, 23, 24, 0, 'h', self.Kirby.x, self.Kirby.y,100,100)

class Jump:
    def __init__(self, Kirby):
        self.Kirby = Kirby
        self.jump_velocity = 500 # 초당 500픽셀 점프
        self.gravity = 1000 # 초당 1000픽셀씩 속도 감소

    def enter(self,e):
        self.Kirby.frame = 0
        self.Kirby.y_velocity = self.jump_velocity
        if self.Kirby.last_state == 3:
            self.Kirby.y_velocity = 0

    def do(self):
        if self.Kirby.last_state == 0:  # walk
            self.Kirby.y += self.Kirby.y_velocity * game_framework.frame_time
            self.Kirby.y_velocity -= self.gravity * game_framework.frame_time
            self.Kirby.x += self.Kirby.dir * WALK_SPEED_PPS * game_framework.frame_time

        elif self.Kirby.last_state == 1:  # run
            self.Kirby.y += self.Kirby.y_velocity * 1.3 * game_framework.frame_time
            self.Kirby.y_velocity -= self.gravity * game_framework.frame_time
            self.Kirby.x += self.Kirby.dir * RUN_SPEED_PPS * game_framework.frame_time

        elif self.Kirby.last_state == 3:  # fly
            self.Kirby.y += self.Kirby.y_velocity * game_framework.frame_time
            self.Kirby.y_velocity -= self.gravity * game_framework.frame_time
            self.Kirby.x += self.Kirby.dir * WALK_SPEED_PPS * game_framework.frame_time

        if self.Kirby.y_velocity > 0:
            self.Kirby.frame = 0
        else:
            self.Kirby.frame = ( self.Kirby.frame + JUMP_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10

        # 땅에 닿았는지 확인
        if self.Kirby.y <= MAP_FLOOR_Y:
            self.Kirby.y = MAP_FLOOR_Y
            self.Kirby.y_velocity = 0

            if self.Kirby.dir == 0:
                self.Kirby.state_machine.change_state(self.Kirby.IDLE)
            elif self.Kirby.dir == 1 or self.Kirby.dir == -1:
                if self.Kirby.last_state == 0: # walk
                    self.Kirby.state_machine.change_state(self.Kirby.WALK)
                elif self.Kirby.last_state == 1: # run
                    self.Kirby.state_machine.change_state(self.Kirby.RUN)


    def exit(self,e):
        self.Kirby.y_start = 0
        # self.Kirby.dir = 0

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
        self.Kirby.frame = (self.Kirby.frame + FLY_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        self.Kirby.x += self.Kirby.dir * FLY_SPEED_PPS * game_framework.frame_time
        self.Kirby.y += self.Kirby.dir_y * FLY_SPEED_PPS * game_framework.frame_time

        (kirby_left, kirby_bottom, kirby_right, kirby_top) = self.Kirby.get_bb()
        # 맵 최대 높이 충돌처리
        if kirby_top >= MAP_CEILING_Y:
            self.Kirby.y = MAP_CEILING_Y - 40
            self.Kirby.y_velocity = 0  # 상승 중이었다면 속도를 0으로

        # 땅에 닿았는지 확인
        if self.Kirby.y <= MAP_FLOOR_Y:
            self.Kirby.y = MAP_FLOOR_Y
            self.Kirby.y_velocity = 0

    def exit(self, e):
        self.Kirby.dir = 0
        self.Kirby.last_state = 3
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(int(self.Kirby.frame) * 30, 3158, 30, 29, self.Kirby.x, self.Kirby.y, 100, 100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(int(self.Kirby.frame) * 30, 3158, 30, 29, 0, 'h', self.Kirby.x,self.Kirby.y, 100, 100)

class Suction:
    def __init__(self, Kirby):
        self.Kirby = Kirby

    def enter(self, e):
        self.Kirby.dir=0
        self.Kirby.frame = 0

    def do(self):
        self.Kirby.frame = (self.Kirby.frame + SUCTION_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

        if self.Kirby.frame >=4: # 4프레임에서 멈춤
            self.Kirby.frame = 4

    def exit(self, e):
        self.Kirby.fire_star()
        pass

    def draw(self):
        if self.Kirby.face_dir == 1:  # right
            self.Kirby.image.clip_draw(int(self.Kirby.frame) * 27, 3213, 25, 27, self.Kirby.x, self.Kirby.y, 100, 100)
        else:  # face_dir == -1: # left
            self.Kirby.image.clip_composite_draw(int(self.Kirby.frame) * 27, 3213, 25, 27, 0, 'h', self.Kirby.x,
                                                 self.Kirby.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.Kirby.x + 10, self.Kirby.y - 20, self.Kirby.x + 150, self.Kirby.y + 30

    def handle_collision(self, group, other):
        if group == 'suction:monster':
            print("커비가 빨아들이는 중")

class Kirby:
    def __init__(self):
        self.x, self.y =400, 100
        self.y_start = 0

        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.dir_y = 0 # 위 1 아래 -1
        self.image = load_image('Kirby_sheet.png')

        self.last_state = 0 # 0이면 walk, 1이면 run 3이면 Fly
        self.knockback_timer = 0.0

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.WALK = Walk(self)
        self.RUN = Run(self)
        self.RUN_STOP = Run_Stop(self)
        self.FLY = Fly(self)
        self.SUCTION = Suction(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP : {space_down: self.IDLE},
                self.IDLE :{time_out: self.SLEEP, z_down: self.SUCTION, x_down: self.JUMP, right_down: self.WALK, left_down: self.WALK,},
                self.WALK :{x_down: self.JUMP, right_up: self.IDLE, left_up: self.IDLE,},
                self.RUN :{x_down: self.JUMP, right_up: self.RUN_STOP, left_up: self.RUN_STOP,},
                self.RUN_STOP :{time_out: self.IDLE},
                self.JUMP:{c_down: self.FLY},
                self.SUCTION:{z_up: self.IDLE},
                self.FLY:{c_up: self.JUMP}

             }
        )

    def update(self):
        if self.knockback_timer > 0:
            self.knockback_timer -= game_framework.frame_time
            self.x += self.dir * KNOCKBACK_SPEED_PPS * game_framework.frame_time
            return

        self.state_machine.update()

    def draw(self):
        if self.knockback_timer > 0:
            # 홀수 일때만 출력하여 깜빡거리는 모션 연출
            if int(self.knockback_timer * 10) % 2 == 1:
                self.state_machine.draw()
        else:
            self.state_machine.draw()

        draw_rectangle(*self.get_bb())

    def fire_star(self):
        print("Fire Star!")
        star = Star(self.x, self.y,self.face_dir)

        game_world.add_collision_pair('star:monster',None, star)

    def get_bb(self):
        return self.x -35, self.y - 30, self.x + 40, self.y + 40

    def handle_collision(self, group, other):
        if group == 'kirby:monster':
            print("Kirby Hit Monster!")

            self.knockback_timer = 0.5
            if self.x < other.x:
                self.dir = -1
            else:
                self.dir = 1


    def handle_event(self, event):
        e = ('INPUT', event)
        # 더블탭 Run 처리
        if self.state_machine.cur_state == self.IDLE and self.IDLE.can_double_tap:
            if right_down(e) or left_down(e):
                self.state_machine.change_state(self.RUN, (e))
                return

        elif self.state_machine.cur_state == self.WALK or self.state_machine.cur_state == self.RUN:
            if left_down(e) and self.dir == 1:
                self.state_machine.change_state(self.WALK, e)  # 즉시 왼쪽 WALK로
                return
            elif right_down(e) and self.dir == -1:
                self.state_machine.change_state(self.WALK, e)  # 즉시 오른쪽 WALK로
                return

        # Jump와 Fly에서의 방향키 처리
        elif self.state_machine.cur_state == self.JUMP:
            if right_down(e):
                self.dir = 1
                self.face_dir = 1
            elif left_down(e):
                self.dir = -1
                self.face_dir = -1
            # 키 떼면 공중에서 멈춤
            elif right_up(e) and self.dir == 1:
                self.dir = 0
            elif left_up(e) and self.dir == -1:
                self.dir = 0

            # fly로 가는 c_down 아니면 이벤트 안넘기고 종료
            if not c_down(e):
                return

        elif self.state_machine.cur_state == self.FLY:
            if right_down(e):
                self.dir = 1
                self.face_dir = 1
            elif left_down(e):
                self.dir = -1
                self.face_dir = -1
            # 키를 떼도 C키를 누르고 있다면 멈추기만 함
            elif right_up(e) and self.dir == 1:
                self.dir = 0
            elif left_up(e) and self.dir == -1:
                self.dir = 0

            if up_down(e):
                self.dir_y = 1
            elif down_down(e):
                self.dir_y = -1
            elif up_up(e) and self.dir_y == 1:
                self.dir_y = 0
            elif down_up(e) and self.dir_y == -1:
                self.dir_y = 0

            if not c_up(e):
                return

        self.state_machine.handle_state_event(e)
