import pygame
import kernelClasses
class GPU(kernelClasses.GPUClass):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        pass
    def init(self, textSize):
        pygame.init()        
        self.surface = pygame.display.set_mode((self.x,self.y))
        self.running = True
        self.size = textSize
        self.objectList = []
        self.textList = []
    
    def ClearText(self):
        self.textList = []
        self.surface.fill((0,0,0))
    def PrintText(self,textStr):

        if (len(self.textList) * self.size > self.y - (self.size*2)):
            self.textList.pop(0)
        
        self.textList.append(textStr)

    def mainloop(self):
        line = 0
        for object in self.textList:
            line += 1
            font = pygame.font.Font("textModeFont.ttf", self.size)
            text = font.render(object, True, (255,255,255), (0,0,0))
            rect = text.get_rect()
            rect.topleft = (0, (line*self.size)-self.size)
            self.surface.blit(text, rect)
            #print(surface, pos)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
            
        pygame.display.update()