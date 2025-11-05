from pico2d import *

import game_world
from kirby import Kirby




def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            exit()
        else:
            kirby.handle_event(event)
    pass


def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

def reset_world():
    global kirby

    kirby = Kirby()
    game_world.add_object(kirby)


open_canvas()
reset_world()

while True:
    handle_events()
    update_world()
    render_world()
    delay(0.1)

close_canvas()