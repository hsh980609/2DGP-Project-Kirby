from pico2d import *
from kirby import Kirby




def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            exit()
        else:
            pass
    pass


def update_world():
    for i in world:
        i.update()
    pass


def render_world():
    clear_canvas()
    for i in world:
        i.draw()
    update_canvas()
    pass

def reset_world():
    global world
    global kirby

    world = []

    kirby = Kirby()
    world.append(kirby)
    pass


open_canvas()
reset_world()

while True:
    handle_events()
    update_world()
    render_world()
    delay(1)

close_canvas()