import pygame
from settings import *
from floor import floor
from player import player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import ui

class level:
    def __init__(self):

        #get display surface
        self.display_surface = pygame.display.get_surface()

        #group
        self.one_sprites= CameraYAxis()
        self.two_sprites= pygame.sprite.Group()
    
        self.current_attack = None
    #setup
        self.map()

        self.ui = ui()
    def map(self):
        layouts = {
			'boundary': import_csv_layout('../map/map_constraints.csv'),
			'grass': import_csv_layout('../map/map_grass.csv'),
			'object': import_csv_layout('../map/map_objects.csv'),
		}
        graphics = {
			'grass': import_folder('../graphics/grass'),
			'objects': import_folder('../graphics/object')
		}
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * floorsize
                        y = row_index * floorsize
                        if style == 'boundary':
                            floor((x,y),[self.two_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            floor((x,y),[self.one_sprites,self.two_sprites],'grass',random_grass_image)
                        if style == 'object':
                            surface = graphics['objects'][int(col)]
                            floor((x,y),[self.one_sprites,self.two_sprites],'object',surface)
        
        self.player = player((200,140),[self.one_sprites],self.two_sprites)

    def create(self):
        self.current_attack = Weapon(self.player,[self.one_sprites],self.two_sprites,self.create,self.destroy)
    def destroy(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None



    def run(self):
        self.one_sprites.new_draw(self.player)
        self.one_sprites.update()
        debug(self.player.status)

class CameraYAxis(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.field = pygame.math.Vector2()
        self.width_divide2 = self.display_surface.get_size()[0] // 2
        self.height_divide2 = self.display_surface.get_size()[1] // 2

        self.floor_surface = pygame.image.load('game/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

    def new_draw(self,player):
        self.field.x = player.rect.centerx - self.width_divide2
        self.field.y = player.rect.centery - self.height_divide2
    
        floor_fieldset_position = self.field.topleft - self.field
        self.display_surface.blit(self.floor_surface,floor_fieldset_position)

        for sprite in sorted(self.sprites(),key= lambda sprite: sprite.rect.centery):
            field_position= sprite.rect.topleft - self.field
            self.display_surface.blit(sprite.image,field_position)