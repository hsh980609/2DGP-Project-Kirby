from pico2d import *

import game_framework
import game_world
import boss_mode
from kirby import Kirby
from background import Background
from stage import Stage
from stage import Ground
from Monster import Monster
import common

kirby = None
running = True
camera_offset_x = 0
camera_offset_y = 0 # 임시

stage = None
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
MAP_LEFT_LIMIT = -950
MAP_RIGHT_LIMIT = 1950

PORTAL_X_MIN = 1830
PORTAL_X_MAX = 1870

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type ==SDL_KEYDOWN and event.key == SDLK_UP:
            if PORTAL_X_MIN < kirby.x <PORTAL_X_MAX:
                game_framework.change_mode(boss_mode)
            else:
                kirby.handle_event(event)
        else:
            kirby.handle_event(event)

def init():
    global kirby
    global running
    global stage

    running = True

    background = Background()
    game_world.add_object(background, 0)

    stage = Stage()
    game_world.add_object(stage, 1)

    grounds = [
        Ground(-550, 35, 800, 70),
        Ground(-100,35,80,180 ),
        Ground(280, 35, 650, 70),
        Ground(730, 35, 255, 180),
        Ground(950, 35, 200, 70),
        Ground(1200, 35, 255, 180),
        Ground(1370, 35, 80, 630),
        Ground(1440, 35, 45, 400),
        Ground(1700, 35, 500, 180),
    ]
    game_world.add_objects(grounds, 1)

    kirby = Kirby()
    game_world.add_object(kirby, 2)

    monsters=[
        Monster(-300, 120),
        Monster(100, 120),
        Monster(250, 120),
        Monster(1000, 120),
    ]
    game_world.add_objects(monsters, 2)

    for monster in monsters:
        game_world.add_collision_pair('star:monster', monster, None)
        game_world.add_collision_pair('kirby:monster', kirby, monster)
        game_world.add_collision_pair('suction:monster', kirby.SUCTION, monster)
        game_world.add_collision_pair('monster:ground', monster, None)

    for ground in grounds:
        game_world.add_collision_pair('kirby:ground', kirby, ground)
        game_world.add_collision_pair('monster:ground', None, ground)


def update():
    global camera_offset_x

    game_world.update()
    game_world.handle_collision()

    camera_offset_x = kirby.x - (common.SCREEN_WIDTH // 2)

    if camera_offset_x < MAP_LEFT_LIMIT:
        camera_offset_x = MAP_LEFT_LIMIT
    elif camera_offset_x > MAP_RIGHT_LIMIT - common.SCREEN_WIDTH:
        camera_offset_x = MAP_RIGHT_LIMIT - common.SCREEN_WIDTH



def draw():
    clear_canvas()
    game_world.render(camera_offset_x)
    update_canvas()

def finish():
    global kirby
    game_world.clear()
    kirby = None

def pause():
    pass

def resume():
    pass