import pyautogui
from pynput import mouse
import socket

ip = input('ip: ')

resolution = (str(pyautogui.size()[0]), str(pyautogui.size()[1]))
resolution = ' '.join(resolution)

class MouseAction:
    MOVE = 0
    CLICK = 1
    SCROLL = 2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ip, 9876))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        conn.sendall(resolution.encode())
        def on_move(x, y):
            content = f'{MouseAction.MOVE} {x} {y}'
            conn.sendall(content.encode())
            print('Pointer moved to {0}'.format(
                (x, y)))

        def on_click(x, y, button, pressed):
            print('{0} at {1}'.format(
                'Pressed' if pressed else 'Released',
                (x, y)))
            content = f'{MouseAction.CLICK} {x} {y} {button} {pressed}'
            conn.sendall(content.encode())

        def on_scroll(x, y, dx, dy):
            content = f'{MouseAction.SCROLL} {x} {y} {dx} {dy}'
            conn.sendall(content.encode())
            print('Scrolled {0} at {1}'.format(
                'down' if dy < 0 else 'up',
                (x, y)))
        with mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll) as listener:
            listener.join()
