from pynput.keyboard import Key, Controller
import time
kb = Controller()
while True:
    kb.press(Key.space)
    time.sleep(0.25)
    kb.release(Key.space)
    time.sleep(2)