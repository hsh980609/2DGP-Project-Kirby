import time
frame_time = 0.0

running = None
stack = None

def change_mode(mode): # 현재 모드 삭제하고 새로운 모드 추가하면서 init 호출
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()

def push_mode(mode): # 현재 모드 pause하고 새로운 모드를 스택에 추가 후 init 호출
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()

def pop_mode(): # 현재 모드 finish 호출 후 현재모드 제거. 이제 Top에는 이전모드가 존재하므로 resume 호출
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()

    if (len(stack) > 0):
        stack[-1].resume()



def quit():
    global running
    running = False

def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode] # 스택에 시작 모드 추가
    start_mode.init()

    global frame_time
    frame_time = 0.0
    current_time = time.time()

    while running: # 현재 모드에 대한 루프 실행
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        frame_time = time.time() - current_time
        current_time += frame_time
        frame_rate = 1.0 / frame_time

    while (len(stack) > 0): # 스택에 남은 모드들 차례대로 삭제
        stack[-1].finish()
        stack.pop()