from pico2d import *





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
    pass


def render_world():
    pass

def reset_world():
    pass


open_canvas()
reset_world()

while True:
    handle_events()
    update_world()
    render_world()

close_canvas()