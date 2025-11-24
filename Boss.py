from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

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

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION


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


    def is_boy_nearby(self, distance):
        pass


    def move_to_boy(self, r=0.5):
        pass


    def get_patrol_location(self):
        pass


    def build_behavior_tree(self):
        pass
