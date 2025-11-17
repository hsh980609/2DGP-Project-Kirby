from pico2d import *

import game_framework
import game_world
from kirby import Kirby
from background import Background


def init():
    print("보스룸 시작")
    global kirby

    background = Background()
    game_world.add_object(background, 0)

    kirby = Kirby()
    game_world.add_object(kirby, 2)


def finish():
    print("보스룸 종료")
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            kirby.handle_event(event)

def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

