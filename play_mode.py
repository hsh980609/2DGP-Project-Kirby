from pico2d import *

import game_world
from kirby import Kirby
from background import Background
from stage import Stage
from Monster import Monster

kirby = None
running = True

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            kirby.handle_event(event)

def init():
    global kirby
    global running

    running = True

    background = Background()
    game_world.add_object(background, 0)

    stage = Stage()
    game_world.add_object(stage, 1)

    kirby = Kirby()
    game_world.add_object(kirby, 2)

    monster = Monster()
    game_world.add_object(monster, 2)

    game_world.add_collision_pair('star:monster', monster, None)
    game_world.add_collision_pair('kirby:monster', kirby, monster)


def update():
    game_world.update()
    game_world.handle_collision()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass