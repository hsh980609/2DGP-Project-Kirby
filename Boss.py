from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

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

        self.y_velocity = 0.0
        self.gravity = 1000.0 # 중력
        self.x, self.y = 700, 200
        self.frame = 0
        self.dir = 1
        self.attack_timer = 0
        self.pattern =0
        self.pattern_timer=0
        self.target = None
        self.state = 'Idle'

        self.state_animation = {
            'Idle':{'y':700,'frames':4,'w':66,'h':100},
            'Walk':{'y':535,'frames':4,'w':66,'h':90},
            'Attack':{'frames': 2,
                      'sprite':[(160,435,75,100),(225,400,90,100)]
                      },
            'Jump':{'frames': 3,
                      'sprite':[(0,400,80,100),(80,400,80,100),(160,435,75,100)]
                      },
        }

        self.build_behavior_tree()

    def update(self):
        total_frames = self.state_animation[self.state]['frames']
        if self.state == 'Jump':
            if self.y_velocity > 0:
                self.frame = 1  # 올라갈 때 (2번째 프레임)
            else:
                self.frame = 2  # 내려갈 때 (3번째 프레임)

        self.frame = (self.frame + total_frames * ACTION_PER_TIME * game_framework.frame_time) % total_frames
        self.bt.run()

        self.pattern_timer +=game_framework.frame_time
        if self.pattern_timer >3.0:# 3초 마다 패턴 변경
            self.pattern = random.randint(0,2)
            self.pattern_timer = 0
            print("패턴 변경: {self.pattern}")

        # 중력을 적용
        self.y += self.y_velocity * game_framework.frame_time
        self.y_velocity -= self.gravity * game_framework.frame_time

    def draw(self, offset_x=0):  # offset_x 추가
        screen_x = self.x - offset_x

        state_animation = self.state_animation[self.state]
        idx = int(self.frame)
        if self.state == 'Attack':
            if idx >= len(state_animation['sprite']):
                idx = len(state_animation['sprite']) - 1
            sprite_x,sprite_y,sprite_w,sprite_h = state_animation['sprite'][idx]
        elif self.state == 'Jump':
            if idx >= len(state_animation['sprite']):
                idx = len(state_animation['sprite']) - 1
            sprite_x,sprite_y,sprite_w,sprite_h = state_animation['sprite'][idx]
        else:
            sprite_x = idx * state_animation['w']
            sprite_y = state_animation['y']
            sprite_w = state_animation['w']
            sprite_h = state_animation['h']


        if self.dir == 1:
            self.image.clip_draw(sprite_x, sprite_y, sprite_w, sprite_h, screen_x, self.y, 300, 300)
        else:
            self.image.clip_composite_draw(sprite_x, sprite_y, sprite_w, sprite_h, 0, 'h', screen_x, self.y, 300, 300)

        draw_rectangle(*self.get_bb())
        draw_circle(screen_x, self.y, 200,255,255,255)

    def get_bb(self):
        return self.x -100, self.y - 130, self.x + 100, self.y + 100

    def handle_collision(self, group, other):
        if group == 'boss:ground':
            kl, kb, kr, kt = self.get_bb()
            gl, gb, gr, gt = other.get_bb()

            # 충돌 깊이 계산
            collision_l = kr - gl
            collision_r = gr - kl
            collision_b = gt - kb

            min_collision = min(collision_l, collision_r, collision_b)

            # 바닥밟음 - 보스룸에서는 바닥과의 충돌 처리만 계산해도 됌.
            if min_collision == collision_b:
                self.y += collision_b  # 뚫고 들어간 만큼 위로 밀어올림
                self.y_velocity = 0  # 낙하 속도 초기화 (안 멈추면 계속 떨어지려 함)


    def set_target_location(self, x=None, y=None):
        pass

    def distance_less_than(self, x1, y1, x2, y2, r): # r은 미터단위.
        pass

    def move_little_to(self, tx, ty):
        pass
    def kirby_in_atk_range(self, r):
        if self.target is None:
            return BehaviorTree.FAIL

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = dx ** 2 + dy ** 2

        if dist < r**2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def atk_kirby(self):
        self.state = 'Attack'
        self.attack_timer += game_framework.frame_time

        if self.attack_timer > 1.0:
            self.attack_timer = 0  # 타이머 초기화
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def pattern_walk(self):
        if self.pattern == 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def pattern_jump(self):
        if self.pattern == 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def pattern_shout(self):
        if self.pattern == 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def walk_to_kirby(self,r=0.5):
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
        #self.y += (dy / dist) * RUN_SPEED_PPS * game_framework.frame_time
        return BehaviorTree.RUNNING

    def jump_to_kirby(self,r =0.5):
        if self.target is None:
            return BehaviorTree.FAIL

        self.state ='Jump'
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dx > 0:
            self.dir = 1
        else:
            self.dir = -1

        if self.y_velocity == 0:
            self.y_velocity = 800  # 점프력 (원하는 높이만큼 조절)
        if dist < r:
            return BehaviorTree.SUCCESS

        self.x += self.dir*RUN_SPEED_PPS*game_framework.frame_time
        return BehaviorTree.RUNNING

    def shout_to_kirby(self):
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
        dist = dx ** 2 + dy ** 2

        if dist < distance**2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def get_patrol_location(self):
        pass


    def build_behavior_tree(self):
        # 커비가 공격범위에 있는가? -> 공격
        c1 = Condition('Kirby in atk range', self.kirby_in_atk_range, 200)
        a1 = Action('Attack', self.atk_kirby)
        seq_atk = Sequence('Attack Sequence', c1, a1)

        # walk
        c_pattern_0 = Condition('Pattern 0?',self.pattern_walk)
        a_walk = Action('Walk',self.walk_to_kirby)
        seq_walk = Sequence('Walk Sequence',c_pattern_0,a_walk)

        # Jump
        c_pattern_1 = Condition('Pattern 1?', self.pattern_jump)
        a_jump = Action('Jump', self.jump_to_kirby)
        seq_jump = Sequence('Jump Sequence', c_pattern_1, a_jump)

        # Shout
        c_pattern_2 = Condition('Pattern 2?', self.pattern_shout)
        a_shout = Action('Shout', self.shout_to_kirby)
        seq_shout = Sequence('Shout Sequence', c_pattern_2, a_shout)

        Pattern_Selector = Selector('Pattern Select',seq_walk,seq_jump,seq_shout)

        # Chase Sequence
        c_nearby = Condition('Is Kirby Nearby',self.is_kirby_nearby,1000)
        seq_chase =Sequence("Chase Sequence",c_nearby,Pattern_Selector)

        root = Selector('Root',seq_atk,seq_chase)
        self.bt = BehaviorTree(root)

