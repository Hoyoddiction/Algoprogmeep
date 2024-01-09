import pygame
from settings import *

class floor(pygame.sprite.Sprite):
    def __init__(self,position,group,type,land=pygame.Surface((floorsize,floorsize))):
        super().__init__(group)
        self.image= land
        if type == 'object':
            self.rect = self.image.get_rect(topleft = (position[0],position[1] - floorsize))
        else:
            self.rect = self.image.get_rect(topleft = position)
        self.oof = self.rect.inflate(0,-10)
        self.type = type