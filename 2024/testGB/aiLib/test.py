from gbAiLib import AIBoy, Variable

game = AIBoy(state="rom.gb.state", speedLimiter=True)
numItems = Variable(0xd31d, game)
while game.tick():
    if numItems.getVal() > 0:
        game.reset()
    pass