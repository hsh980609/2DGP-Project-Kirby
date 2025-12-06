from pico2d import *

import game_framework
import game_world
from kirby import Kirby
from background import Boss_Background
from stage import Ground
from Boss import Boss

bgm = None
victory_bgm = None
victory_played = False
victory_timer = 0
boss = None

def init():
    print("보스룸 시작")
    global bgm, victory_bgm,victory_played, boss, victory_timer, kirby

    bgm = load_music('08 vs. Boss 1.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

    victory_bgm = load_music('17 Kirby Clear Dance 1.mp3')
    victory_bgm.set_volume(64)
    victory_played = False
    victory_timer = 0

    background = Boss_Background()
    game_world.add_object(background, 0)

    kirby = Kirby()
    kirby.x, kirby.y = 100, 100
    game_world.add_object(kirby, 3)

    boss = Boss()
    game_world.add_object(boss, 2)
    boss.target = kirby

    game_world.add_collision_pair('kirby:boss', kirby, boss)
    game_world.add_collision_pair('star:boss', boss, None)

    game_world.add_collision_pair('star:monster', None, None)
    game_world.add_collision_pair('kirby:monster', kirby, None)
    game_world.add_collision_pair('suction:monster', kirby.SUCTION, None)

    grounds = [
        Ground(700, 35, 1400, 70),
    ]
    game_world.add_objects(grounds, 1)
    for ground in grounds:
        game_world.add_collision_pair('kirby:ground', kirby, ground)
        game_world.add_collision_pair('boss:ground', boss, ground)
        game_world.add_collision_pair('monster:ground', None, ground) # 몬스터는 보스쪽에서


def finish():
    print("보스룸 종료")
    global bgm, victory_bgm
    bgm = None
    victory_bgm = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            kirby.handle_event(event)

def update():
    global victory_played, victory_timer

    game_world.update()
    game_world.handle_collision()

    if boss.state == 'Death':
        if not victory_played:
            bgm.stop()
            victory_bgm.play()
            victory_played = True

            kirby.victory()
        if victory_played:
            victory_timer +=game_framework.frame_time
            if victory_timer >5.0:
                game_framework.quit()

    if kirby.x < 100:
        kirby.x = 100
    elif kirby.x >1050:
        kirby.x = 1050

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

