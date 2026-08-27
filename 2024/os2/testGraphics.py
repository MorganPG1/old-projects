import pygame
pygame.init()

x = 400
y = 300

surface = pygame.display.set_mode((x,y))
running = True
line = 0
size = 18
objectList = []
textList = []
def ClearText():
    global textList
    global surface
    textList = []
    surface.fill((0,0,0))
def PrintText(textStr):
    global line
    global size
    global textList
    global x
    global y
    if (len(textList) * size > y - (size*2)):
        textList.pop(0)
    
    textList.append(textStr)

while running:
    line = 0
    for object in textList:
        line += 1
        font = pygame.font.Font("textModeFont.ttf", size)
        text = font.render(object, True, (255,255,255), (0,0,0))
        rect = text.get_rect()
        rect.center = (10, line*size)
        surface.blit(text, rect)
        #print(surface, pos)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                PrintText("A")
            elif event.key == pygame.K_b:
                PrintText("B")
            elif event.key == pygame.K_DELETE:
                print("clear")
                ClearText()
    pygame.display.update()