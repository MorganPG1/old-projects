from pyboy import PyBoy

game = PyBoy("rom.gb")
while game.tick():
    pass
game.stop()