from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from kirby import Kirby

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Boss:
    image = None
    def __init__(self):
        if Boss.image == None:
            Boss.image = load_image('Boss.png')


        self.x, self.y = 400, 200
        self.frame = 0
        self.dir = 1
        self.target = None
        self.state = 'Idle'

        self.build_behavior_tree()

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()


    def draw(self, offset_x=0):  # offset_x 추가
        screen_x = self.x - offset_x

        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 66, 700, 68, 100, screen_x, self.y, 300, 300)
        else:
            self.image.clip_composite_draw(int(self.frame) * 66, 700, 68, 100, 0, 'h', screen_x, self.y, 300, 300)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x -100, self.y - 130, self.x + 100, self.y + 100

    def handle_collision(self, group, other):
        pass


    def set_target_location(self, x=None, y=None):
        pass

    def distance_less_than(self, x1, y1, x2, y2, r): # r은 미터단위.
        pass

    def move_little_to(self, tx, ty):
        pass


    def move_to(self, r=0.5):
        pass

    def set_random_location(self):
        pass


    def is_kirby_nearby(self, distance):
        if self.target is None:
            return BehaviorTree.FAIL

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist < distance:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def move_to_kirby(self, r=0.5):
        if self.target is None:
            return BehaviorTree.FAIL

        self.state ='Walk'
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dx > 0:
            self.dir = 1
        else:
            self.dir = -1

        if dist < r:
            return BehaviorTree.SUCCESS

        self.x += (dx / dist)*RUN_SPEED_PPS*game_framework.frame_time
        self.y += (dy / dist) * RUN_SPEED_PPS * game_framework.frame_time
        return BehaviorTree.RUNNING


    def get_patrol_location(self):
        pass


    def build_behavior_tree(self):
        # 커비가 1000픽셀 화면안에 있는가?
        c1 = Condition('Is Kirby Nearby',self.is_kirby_nearby,1000)
        # 액션: 커비 추격
        a1 =Action('Move to Kirby',self.move_to_kirby)

        root = Sequence("Chase kirby",c1,a1)
        self.bt = BehaviorTree(root)
        pass
