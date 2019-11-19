import socket
import pyautogui
from pynput.mouse import Controller, Button

TEST = False #True

master = input('master ip: ')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'init', (master, 9876))

mouse = Controller()

init, _ = sock.recvfrom(1024)
master_resolution = init.decode().split(' ')
master_resolution = list(map(lambda i: int(i), master_resolution))
print('master resolution: ', master_resolution)
self_resolution = (pyautogui.size()[0], pyautogui.size()[1])

class MouseAction:
    MOVE = 0
    CLICK = 1
    SCROLL = 2

def on_move(x, y):
    x_ = x * self_resolution[0] / master_resolution[0]
    y_ = y * self_resolution[1] / master_resolution[1]
    if not TEST:
        mouse.position = (x_, y_)
    else:
        print(x_, y_)

def on_click(x, y, button, pressed):
    if pressed:
        if not TEST:
            mouse.press(button)
        print('press', button)
    else:
        if not TEST:
            mouse.release(button)
        print('release', button)

def on_scroll(x, y, dx, dy):
    if not TEST:
        mouse.scroll(dx, dy)
    print('scroll', dx, dy)

def _eval(*args):
    evaled_args = []
    for i in args:
        evaled_args.append(eval(i))
    return evaled_args

while True:
    control, _ = sock.recvfrom(1024)
    args = control.decode().split(' ')
    action = int(args[0])
    if action == MouseAction.MOVE:
        on_move(*_eval(*args[1:]))
    if action == MouseAction.CLICK:
        on_click(*_eval(*args[1:]))
    if action == MouseAction.SCROLL:
        on_scroll(*_eval(*args[1:]))

