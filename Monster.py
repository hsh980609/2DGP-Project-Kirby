from pico2d import *
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
MONSTER_SPEED_KMPH = 10.0  # Km / Hour (커비 걷기 속도의 절반)
MONSTER_SPEED_MPM = (MONSTER_SPEED_KMPH * 1000.0 / 60.0)
MONSTER_SPEED_MPS = (MONSTER_SPEED_MPM / 60.0)
MONSTER_SPEED_PPS = (MONSTER_SPEED_MPS * PIXEL_PER_METER)

MONSTER_FRAMES_PER_ACTION = 5
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Monster:
    image = None

    def __init__(self):
        if Monster.image == None:
            Monster.image = load_image('Monster.png')

        self.x, self.y = 500, 110
        self.frame = 0
        self.dir = -1

        self.patrol_start_x = 400
        self.patrol_end_x = 600

    def update(self):
        self.frame = (self.frame + MONSTER_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % MONSTER_FRAMES_PER_ACTION

        self.x += self.dir * MONSTER_SPEED_PPS * game_framework.frame_time

        if self.dir == -1 and self.x < self.patrol_start_x:
            self.x =self.patrol_start_x # 경계 안넘게
            self.dir =1
        elif self.dir == 1 and self.x > self.patrol_end_x:
            self.x = self.patrol_end_x
            self.dir = -1

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw((int(self.frame) * 30), 120, 30, 30, self.x, self.y, 100, 100)
        else:
            self.image.clip_composite_draw((int(self.frame) * 30), 120, 30, 30, 0, 'h', self.x, self.y, 100, 100)
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass