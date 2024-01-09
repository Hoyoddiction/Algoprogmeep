import pygame, sys
from settings import *
from level import level

class RPG:
    def __init__(self):
        
        #general setup for pygames
        pygame.init()
        self.screen= pygame.display.set_mode((width,height))
        pygame.display.set_caption('Meep')
        self.clock= pygame.time.Clock()
        self.level= level()
    #event loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    rpg = RPG()
    rpg.run()