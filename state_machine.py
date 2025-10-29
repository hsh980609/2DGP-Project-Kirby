from event_to_string import event_to_string

class StateMachine:
    def __init__(self, start_state, state_transitions):
        self.cur_state = start_state
        self.state_transitions = state_transitions
        self.cur_state.enter(('START', None))

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()


    def handle_state_event(self,event):
        for check_event in self.state_transitions[self.cur_state].keys():
            if check_event(event):
                pass
        pass