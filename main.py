from pico2d import *
import game_framework
import title_mode as start_mode
import common


open_canvas(common.SCREEN_WIDTH,common.SCREEN_HEIGHT)
game_framework.run(start_mode)
close_canvas()