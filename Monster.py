from pico2d import *
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
MONSTER_SPEED_KMPH = 5.0  # Km / Hour (커비 걷기 속도의 절반)
MONSTER_SPEED_MPM = (MONSTER_SPEED_KMPH * 1000.0 / 60.0)
MONSTER_SPEED_MPS = (MONSTER_SPEED_MPM / 60.0)
MONSTER_SPEED_PPS = (MONSTER_SPEED_MPS * PIXEL_PER_METER)

# 충돌시 넉백 속도
KNOCKBACK_SPEED_KMPH = 10.0  # 넉백 속도
KNOCKBACK_SPEED_MPM = (KNOCKBACK_SPEED_KMPH * 1000.0 / 60.0)
KNOCKBACK_SPEED_MPS = (KNOCKBACK_SPEED_MPM / 60.0)
KNOCKBACK_SPEED_PPS = (KNOCKBACK_SPEED_MPS * PIXEL_PER_METER)

MONSTER_FRAMES_PER_ACTION = 5
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Monster:
    image = None

    MONSTER_ANIMATION = [
        (0),
        (30),
        (55),
        (82),
        (110)
    ]

    def __init__(self):
        if Monster.image == None:
            Monster.image = load_image('Monster.png')
        self.x, self.y = 500, 120
        self.frame = 0
        self.dir = -1

        self.knockback_timer = 0.0

        self.patrol_start_x = 400
        self.patrol_end_x = 600

    def update(self):
        if self.knockback_timer > 0: # 넉백 상태라면
            self.x += self.dir * KNOCKBACK_SPEED_PPS * game_framework.frame_time
            self.knockback_timer -= game_framework.frame_time
        else:# 순찰
            self.frame = ( self.frame + MONSTER_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % MONSTER_FRAMES_PER_ACTION
            self.x += self.dir * MONSTER_SPEED_PPS * game_framework.frame_time

            if self.dir == -1 and self.x < self.patrol_start_x:
                self.x = self.patrol_start_x  # 경계 안넘게
                self.dir = 1
            elif self.dir == 1 and self.x > self.patrol_end_x:
                self.x = self.patrol_end_x
                self.dir = -1

    def draw(self):
        frame_index = int(self.frame)
        frame_data = self.MONSTER_ANIMATION[frame_index]
        M_left = frame_data

        if self.knockback_timer > 0:
            if int(self.knockback_timer * 10) % 2 == 1:
                if self.dir == 1:
                    self.image.clip_draw(M_left, 120, 30, 30, self.x, self.y, 100, 100)
                else:
                    self.image.clip_composite_draw(M_left, 120, 30, 30, 0, 'h', self.x, self.y, 100, 100)
        else:
            if self.dir == 1:
                self.image.clip_draw(M_left, 120, 30, 30, self.x, self.y, 100, 100)
            else:
                self.image.clip_composite_draw(M_left, 120, 30, 30, 0, 'h', self.x, self.y, 100, 100)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 45, self.x + 30, self.y + 15

    def handle_collision(self, group, other):
        if group == 'star:monster':
            print(f'별과 몬스터 충돌!-몬스터쪽 알람')
            # 임시로 별과 충돌하면 밀려나게만 해놓음.
            if self.knockback_timer <= 0: # 넉백 중 아니라면
                print(f'충돌! - 몬스터쪽 알람')
                self.knockback_timer = 0.5 # 0.5초간 넉백
                # 커비와 반 방향으로 튕겨나감
                if self.x <other.x:
                    self.dir = -1
                else:
                    self.dir = 1
        elif group == 'kirby:monster':
            if self.knockback_timer <= 0: # 넉백 중 아니라면
                print(f'충돌! - 몬스터쪽 알람')
                self.knockback_timer = 0.5 # 0.5초간 넉백
                # 커비와 반 방향으로 튕겨나감
                if self.x <other.x:
                    self.dir = -1
                else:
                    self.dir = 1
        elif group == 'suction:monster':
            print(f'몬스터 끌려감')