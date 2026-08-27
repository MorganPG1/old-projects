from linkboy2 import LinkBoy, Link
import keyboard
import logging
logger = logging.getLogger()
gb1 = LinkBoy(logger,"pkr.gb")
gb2 = LinkBoy(logger,"pkb.gb")

keyMap1 = {
    "[":"a",
    "p":"b",
    "u":"start",
    "i":"select",
    "t":"up",
    "g":"down",
    "h":"right",
    "f":"left",
}
keyMap2 = {
    "d":"a",
    "f":"b",
    "'":"start",
    "#":"select",
    "o":"up",
    "l":"down",
    ";":"right",
    "k":"left",
}
link = Link(gb1, gb2)

while True:
    
    for key, button in keyMap1.items():
        if keyboard.is_pressed(key):
            gb1.button(button)
    for key, button in keyMap2.items():
        if keyboard.is_pressed(key):
            gb2.button(button)
    link.step()
    