from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from Monster import Monster

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
            Boss.image = load_image('resources/KingDedede/Boss.png')
        self.Boss_2_image =load_image('resources/KingDedede/Boss_2.png')

        self.Shout_sound = load_wav('resources/Sounds/Boss_Shout.wav')
        self.Shout_sound.set_volume(32)
        self.land_sound = load_wav('resources/Sounds/Boss_land.wav')
        self.land_sound.set_volume(32)

        self.y_velocity = 0.0
        self.gravity = 1000.0 # 중력
        self.x, self.y = 700, 200
        self.hp = 3
        self.frame = 0
        self.dir = 1
        self.font = load_font('resources/ENCR10B.TTF', 16)

        self.pattern =0
        self.is_thinking = False  # 생각 중인지 체크하는 플래그
        self.attack_timer = 0
        self.walk_timer = 0
        self.think_timer = 0
        self.shout_timer=0
        self.hit_timer=0
        self.target = None
        self.state = 'Idle'

        self.state_animation = {
            'Idle':{'y':700,'frames':4,'w':66,'h':100},
            'Walk':{'y':535,'frames':4,'w':66,'h':90},
            'Attack':{'frames': 2,
                      'sprite':[(160,435,70,100),(225,400,90,120)]
                      },
            'Jump':{'frames': 3,
                      'sprite':[(0,400,80,100),(80,400,80,100),(160,435,75,100)]
                      },
            'Shout':{'frames': 2,
                      'sprite':[(245,110,55,90),(300,110,55,90)]
                      },
            'Hit':{'y':622,'frames':1,'w':66,'h':80},
            'Death':{'frames': 2,
                      'sprite':[(743,110,65,90),(810,110,65,90)]
                      },
        }

        self.build_behavior_tree()

    def update(self):
        if self.hp <= 0:
            print("보스 체력 0. 보스 사망")
            self.state = 'Death'

        if self.state == 'Hit':
            self.hit_timer += game_framework.frame_time

            if self.hit_timer > 0.5:
                self.hit_timer = 0
                self.state = 'Idle'
                self.is_thinking = True  # 맞았으니 잠깐 생각
        elif self.state == 'Death':
            pass
        else:
            # Hit가 아닐 때만 행동 트리 실행
            self.bt.run()

        total_frames = self.state_animation[self.state]['frames']
        if self.state == 'Jump':
            if self.y_velocity > 0:
                self.frame = 1  # 올라갈 때 (2번째 프레임)
            else:
                self.frame = 2  # 내려갈 때 (3번째 프레임)
        self.frame = (self.frame + total_frames * ACTION_PER_TIME * game_framework.frame_time) % total_frames

        # 중력을 적용
        self.y += self.y_velocity * game_framework.frame_time
        self.y_velocity -= self.gravity * game_framework.frame_time

    def draw(self, offset_x=0):  # offset_x 추가
        screen_x = self.x - offset_x

        state_animation = self.state_animation[self.state]
        idx = int(self.frame)

        if self.state in['Shout','Death'] :
            target_image = self.Boss_2_image
        else:
            target_image = self.image

        if self.state in['Attack','Jump','Shout','Death'] :
            if idx >= len(state_animation['sprite']):
                idx = len(state_animation['sprite']) - 1
            sprite_x,sprite_y,sprite_w,sprite_h = state_animation['sprite'][idx]
        else:
            sprite_x = idx * state_animation['w']
            sprite_y = state_animation['y']
            sprite_w = state_animation['w']
            sprite_h = state_animation['h']


        if self.dir == 1:
            target_image.clip_draw(sprite_x, sprite_y, sprite_w, sprite_h, screen_x, self.y, 300, 300)
        else:
            target_image.clip_composite_draw(sprite_x, sprite_y, sprite_w, sprite_h, 0, 'h', screen_x, self.y, 300, 300)

        self.font.draw(screen_x - 40, self.y + 80, f'HP: {self.hp:.0f}', (255, 255, 0))
        # draw_rectangle(*self.get_bb())
        # draw_circle(screen_x, self.y, 200,255,255,255)

    def get_bb(self):
        l = self.x - 100
        b = self.y - 130
        r = self.x + 100
        t = self.y + 100

        # 공격상태라면 바운딩박스 범위를 늘려서 망치도 충격판정나게.
        if self.state == 'Attack':
            if self.dir == 1:
                r += 100
            else:
                l -= 100

        return l, b, r, t

    def handle_collision(self, group, other):
        if group == 'boss:ground':
            kl, kb, kr, kt = self.get_bb()
            gl, gb, gr, gt = other.get_bb()

            # 충돌 깊이 계산
            collision_l = kr - gl
            collision_r = gr - kl
            collision_b = gt - kb

            min_collision = min(collision_l, collision_r, collision_b)

            # 바닥밟음 - 보스룸에서는 바닥과의 충돌 처리만 계산해도 됨.
            if min_collision == collision_b:
                if self.y_velocity < -100: # 공중에서 착지하는 순간에만 재생 - 떨어지는 속도가 있을 경우
                    self.land_sound.play()

                self.y += collision_b  # 뚫고 들어간 만큼 위로 밀어올림
                self.y_velocity = 0  # 낙하 속도 초기화 (안 멈추면 계속 떨어지려 함)

        if self.state == 'Death': # 사망시 다른 객체와의 충돌처리 X
            return
        elif group == 'star:boss':
            print('별과 보스 충돌!-보스쪽 알람')
            self.hp -= 1
            self.state = 'Hit'

    def kirby_in_atk_range(self, r):
        if self.state == 'Attack':
            return BehaviorTree.SUCCESS

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
            self.is_thinking = True
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def Check_pattern(self,pattern):
        if self.pattern == pattern:
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

        self.walk_timer +=game_framework.frame_time
        if self.walk_timer>2.0:
            self.walk_timer = 0
            self.is_thinking = True
            return BehaviorTree.SUCCESS

        self.x += (dx / dist)*RUN_SPEED_PPS*game_framework.frame_time
        return BehaviorTree.RUNNING

    def jump_to_kirby(self,r =0.5):
        if self.target is None:
            return BehaviorTree.FAIL

        if self.state !='Jump':
            self.state = 'Jump'
            # 점프 뛸때 한번만 방향 설정
            dx = self.target.x - self.x
            if dx > 0:
                self.dir = 1
            else:
                self.dir = -1
            if self.y_velocity == 0: # 땅에 있을떄만
                self.y_velocity = 800
            return BehaviorTree.RUNNING
        else: # 이미 점프 상태라면
            if self.y_velocity == 0: # 착지 체크
                self.is_thinking = True
                return BehaviorTree.SUCCESS

        self.x += self.dir*RUN_SPEED_PPS*game_framework.frame_time # 공중 이동 착지전까지 계속된다.
        return BehaviorTree.RUNNING

    def shout_to_kirby(self):
        self.state = 'Shout'
        self.shout_timer += game_framework.frame_time

        if self.shout_timer < game_framework.frame_time * 1.5:
            print("몬스터 소환")
            self.Shout_sound.play()
            new_monster = Monster(random.randint(100,1000),800)
            game_world.add_object(new_monster,3)
            game_world.add_collision_pair('monster:ground', new_monster,None)# 땅은 모드에서 등록해놓음
            game_world.add_collision_pair('star:monster', new_monster, None)
            game_world.add_collision_pair('kirby:monster', None, new_monster)
            game_world.add_collision_pair('suction:monster', None, new_monster)

        # (몬스터 소환 로직)
        if self.shout_timer > 1.5:
            self.shout_timer = 0
            self.is_thinking = True
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

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

    def check_thinking(self):
        if self.is_thinking:
            return BehaviorTree.SUCCESS
        else:
            return  BehaviorTree.FAIL

    def do_think(self):
        self.state = 'Idle'
        self.think_timer +=game_framework.frame_time
        if self.think_timer >1.0:
            self.think_timer=0
            self.pattern=random.randint(0,2)
            print(f"생각 끝. 다음패턴: {self.pattern}")
            self.is_thinking=False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        # 커비가 공격범위에 있는가? -> 공격
        c1 = Condition('Kirby in atk range', self.kirby_in_atk_range, 200)
        a1 = Action('Attack', self.atk_kirby)
        seq_atk = Sequence('Attack Sequence', c1, a1)

        # walk
        c_pattern_0 = Condition('Pattern 0?',self.Check_pattern,0)
        a_walk = Action('Walk',self.walk_to_kirby)
        seq_walk = Sequence('Walk Sequence',c_pattern_0,a_walk)

        # Jump
        c_pattern_1 = Condition('Pattern 1?', self.Check_pattern,1)
        a_jump = Action('Jump', self.jump_to_kirby)
        seq_jump = Sequence('Jump Sequence', c_pattern_1, a_jump)

        # Shout
        c_pattern_2 = Condition('Pattern 2?', self.Check_pattern,2)
        a_shout = Action('Shout', self.shout_to_kirby)
        seq_shout = Sequence('Shout Sequence', c_pattern_2, a_shout)

        Pattern_Selector = Selector('Pattern Select',seq_walk,seq_jump,seq_shout)

        # Think Sequence
        c_think = Condition('Think?',self.check_thinking)
        a_think = Action('Think & Reset',self.do_think)
        seq_think = Sequence('Think Seq',c_think,a_think)

        # Chase Sequence
        c_nearby = Condition('Is Kirby Nearby',self.is_kirby_nearby,1000)
        seq_chase =Sequence("Chase Sequence",c_nearby,Pattern_Selector)

        root = Selector('Root',seq_think, seq_atk,seq_chase)
        self.bt = BehaviorTree(root)

