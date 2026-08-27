import pygame
import test

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("System Information")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)



# Keep the GUI running until the user closes it
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
   # Get system information
    screen.fill(white)

    # Display system information on the screen
    font = pygame.font.Font(None, 24)
    text = font.render("System Information:", True, black)
    screen.blit(text, (20, 20))

    systemInfo = test.getSystemInfo()
    kernelInfo = test.getKernelInfo()

    # CPU information
    text = font.render("CPU Name:", True, black)
    screen.blit(text, (20, 50))
    text = font.render(systemInfo["cpuName"], True, black)
    screen.blit(text, (150, 50))

    text = font.render("CPU Cores:", True, black)
    screen.blit(text, (20, 80))
    text = font.render(str(systemInfo["cpuCores"]), True, black)
    screen.blit(text, (150, 80))

    text = font.render("CPU Max Frequency:", True, black)
    screen.blit(text, (20, 110))
    text = font.render(str(round(systemInfo["cpuFreq"] / 1000, 1)) + " GHz", True, black)
    screen.blit(text, (200, 110))

    text = font.render("CPU Current Frequency:", True, black)
    screen.blit(text, (20, 140))
    text = font.render(str(round(systemInfo["cpuFreqCurrent"] / 1000, 1)) + " GHz", True, black)
    screen.blit(text, (220, 140))

    # Memory information
    text = font.render("Total Memory:", True, black)
    screen.blit(text, (20, 180))
    text = font.render(str(round(systemInfo["memoryTotal"] / 1024 / 1024 / 1024, 1)) + " GB", True, black)
    screen.blit(text, (150, 180))

    text = font.render("Free Memory:", True, black)
    screen.blit(text, (20, 210))
    text = font.render(str(round(systemInfo["memoryFree"] / 1024 / 1024 / 1024, 1)) + " GB", True, black)
    screen.blit(text, (150, 210))

    # Kernel information
    text = font.render("Kernel Name:", True, black)
    screen.blit(text, (20, 250))
    text = font.render(kernelInfo["kernelName"], True, black)
    screen.blit(text, (150, 250))

    text = font.render("Kernel Version:", True, black)
    screen.blit(text, (20, 280))
    text = font.render(kernelInfo["kernelVer"], True, black)
    screen.blit(text, (150, 280))

    # Update the display
    pygame.display.update()
pygame.quit()