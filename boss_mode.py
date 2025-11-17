from pico2d import *
import game_framework

def init():
    print("보스룸 시작")
    pass

def finish():
    print("보스룸 종료")
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            pass
    pass

def update():
    pass

def draw():
    pass
