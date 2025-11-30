from pico2d import *

import game_framework
import game_world
from kirby import Kirby
from background import Boss_Background
from stage import Ground
from Boss import Boss

def init():
    print("보스룸 시작")
    global kirby

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
        Ground(400, 35, 800, 70),
    ]
    game_world.add_objects(grounds, 1)
    for ground in grounds:
        game_world.add_collision_pair('kirby:ground', kirby, ground)
        game_world.add_collision_pair('boss:ground', boss, ground)
        game_world.add_collision_pair('monster:ground', None, ground) # 몬스터는 보스쪽에서


def finish():
    print("보스룸 종료")
    pass

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
    game_world.update()
    game_world.handle_collision()

    if kirby.x < 20:
        kirby.x = 20
    elif kirby.x >800:
        kirby.x = 800

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

