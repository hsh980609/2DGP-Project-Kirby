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

    def __init__(self,x,y):
        if Monster.image == None:
            Monster.image = load_image('Monster.png')
        self.x, self.y = x, y
        self.y_velocity = 0.0
        self.gravity = 1000.0  # 중력
        self.frame = 0
        self.dir = -1

        self.knockback_timer = 0.0
        self.is_being_sucked = False
        self.target = None

        self.patrol_start_x = self.x - 100
        self.patrol_end_x = self.x + 100

    def update(self):
        if self.knockback_timer > 0: # 넉백 상태라면
            self.x += self.dir * KNOCKBACK_SPEED_PPS * game_framework.frame_time
            self.knockback_timer -= game_framework.frame_time

        elif self.is_being_sucked:
            if self.x < self.target.x:
                self.dir = 1
                self.x += MONSTER_SPEED_PPS * 2 *game_framework.frame_time
            elif self.x > self.target.x:
                self.dir = -1
                self.x -= MONSTER_SPEED_PPS * 2 * game_framework.frame_time
            self.is_being_sucked = False
            self.target = None

        else:# 순찰
            self.frame = ( self.frame + MONSTER_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % MONSTER_FRAMES_PER_ACTION
            self.x += self.dir * MONSTER_SPEED_PPS * game_framework.frame_time

            if self.dir == -1 and self.x < self.patrol_start_x:
                self.x = self.patrol_start_x  # 경계 안넘게
                self.dir = 1
            elif self.dir == 1 and self.x > self.patrol_end_x:
                self.x = self.patrol_end_x
                self.dir = -1
        self.y += self.y_velocity * game_framework.frame_time
        self.y_velocity -= self.gravity * game_framework.frame_time

    def draw(self,offset_x=0):
        frame_index = int(self.frame)
        frame_data = self.MONSTER_ANIMATION[frame_index]
        M_left = frame_data

        screen_x = self.x - offset_x

        if self.knockback_timer > 0:
            if int(self.knockback_timer * 10) % 2 == 1:
                if self.dir == 1:
                    self.image.clip_draw(M_left, 120, 30, 30, screen_x, self.y, 100, 100)
                else:
                    self.image.clip_composite_draw(M_left, 120, 30, 30, 0, 'h', screen_x, self.y, 100, 100)
        else:
            if self.dir == 1:
                self.image.clip_draw(M_left, 120, 30, 30, screen_x, self.y, 100, 100)
            else:
                self.image.clip_composite_draw(M_left, 120, 30, 30, 0, 'h', screen_x, self.y, 100, 100)

        l, b, r, t = self.get_bb()
        draw_rectangle(l - offset_x, b, r - offset_x, t)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 45, self.x + 30, self.y + 15

    def handle_collision(self, group, other):
        if group == 'star:monster':
            print('별과 몬스터 충돌!-몬스터쪽 알람')
            # 임시로 별과 충돌하면 밀려나게만 해놓음.
            if self.knockback_timer <= 0: # 넉백 중 아니라면
                print('충돌! - 몬스터쪽 알람')
                self.knockback_timer = 0.5 # 0.5초간 넉백
                # 커비와 반대 방향으로 튕겨나감
                if self.x <other.x:
                    self.dir = -1
                else:
                    self.dir = 1
        elif group == 'kirby:monster':
            # 석션 상태라면 몬스터 삼켜짐 처리
            if other.state_machine.cur_state == other.SUCTION:
                print('몬스터 삼켜짐(삭제)')
                game_world.remove_object(self)

            elif self.knockback_timer <= 0: # 넉백 중 아니라면
                print('충돌! - 몬스터쪽 알람')
                self.knockback_timer = 0.5 # 0.5초간 넉백
                # 커비와 반대 방향으로 튕겨나감
                if self.x <other.x:
                    self.dir = -1
                else:
                    self.dir = 1
        elif group == 'suction:monster':
            if other.Kirby.state_machine.cur_state == other:
                print('몬스터 끌려감')
                self.is_being_sucked = True
                self.target = other.Kirby
        elif group == 'monster:ground':
            kl, kb, kr, kt = self.get_bb()
            gl, gb, gr, gt = other.get_bb()

            # 충돌 깊이 계산
            collision_l = kr - gl
            collision_r = gr - kl
            collision_b = gt - kb

            min_collision = min(collision_l, collision_r, collision_b)

            # 바닥밟음
            if min_collision == collision_b:
                self.y += collision_b  # 뚫고 들어간 만큼 위로 밀어올림
                self.y_velocity = 0  # 낙하 속도 초기화 (안 멈추면 계속 떨어지려 함)
            pass