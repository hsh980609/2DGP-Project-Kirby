from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 100)
        self.image.draw(1200, 30)

