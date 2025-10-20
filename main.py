from pico2d import *


open_canvas()
reset_world()

while True:
    handle_events()
    update_world()
    render_world()

close_canvas()