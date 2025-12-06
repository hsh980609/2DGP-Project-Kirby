from pico2d import *
import game_framework
import play_mode
import common

def init():
    global image
    image = load_image('resources/Title.png')


def finish():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)

def update():
    pass

def draw():
    clear_canvas()
    image.draw(common.SCREEN_WIDTH // 2, common.SCREEN_HEIGHT // 2, common.SCREEN_WIDTH, common.SCREEN_HEIGHT)
    update_canvas()