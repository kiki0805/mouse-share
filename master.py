import pyautogui
from pynput import mouse
import socket

ip = input('ip: ')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, 9876))

resolution = (str(pyautogui.size()[0]), str(pyautogui.size()[1]))
resolution = ' '.join(resolution)

addr = None
while True:
    data, addr = sock.recvfrom(1024)
    if data.decode() == 'init':
        break

sock.sendto(resolution.encode(), addr)

class MouseAction:
    MOVE = 0
    CLICK = 1
    SCROLL = 2

def on_move(x, y):
    content = f'{MouseAction.MOVE} {x} {y}'
    sock.sendto(content.encode(), addr)
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    content = f'{MouseAction.CLICK} {x} {y} {button} {pressed}'
    sock.sendto(content.encode(), addr)

def on_scroll(x, y, dx, dy):
    content = f'{MouseAction.SCROLL} {x} {y} {dx} {dy}'
    sock.sendto(content.encode(), addr)
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

# Collect events until released
with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()
