from event_to_string import event_to_string

class StateMachine:
    def __init__(self, start_state):
        self.cur_state = start_state
        pass
    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()


    def handle_state_event(self):
        pass