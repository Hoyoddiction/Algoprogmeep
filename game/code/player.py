import pygame
from settings import *
from support import import_folder

class player (pygame.sprite.Sprite):
    def __init__(self,position,group,two_sprites,create,destroy):
        super().__init__(group)
        self.image= pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect =self.image.get_rect(topleft =position)
        self.oof= self.rect.inflate(0,-26)
        
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15



        self.movement = pygame.math.Vector2()
        self.fast = 6
        self.two_sprites = two_sprites
        self.attack = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = two_sprites

        self.create_attack = create
        self.destroy_attack = destroy
        self.weapon_index = 0
        self.weapon = list(weapons.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 100

        self.statistics = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
        self.healthbar = self.statistics['health'] * 0.5
        self.energybar = self.statistics['energy'] * 0.8
        self.exp = 200
        self.speedy = self.statistics['speed']


    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
			    'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			    'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    #clickky click
    def click(self):
        if not self.attack:
            movkey= pygame.key.get_pressed()
        
            if movkey[pygame.K_UP]:
                self.movement.y = -1
                self.status ='up'
            elif movkey[pygame.K_DOWN]:
                self.movement.y = 1
                self.status ='dowm'
            else:
                self.movement.y = 0

            if movkey[pygame.K_RIGHT]:
                self.movement.x = 1
                self.status ='right'
            elif movkey[pygame.K_LEFT]:
                self.movement.x = -1
                self.status = 'left'
            else:
                self.movement.x = 0

        if movkey[pygame.K_SPACE]:
            self.attack = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')


            if movkey[pygame.K_LCTRL]:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')

            if movkey[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapons.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                    self.weapon = list(weapons.keys())[self.weapon_index]


    def get_status(self):
        if self.movement.x == 0 and self.movement.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
            
            if self.attack:
                self.movement.x = 0
                self.movement.y = 0
                if not 'attack' in self.status:
                    if 'idle' in self.status:
                        self.status = self.status.replace('_idle','_attack')
                    else:
                        self.status = self.status + '_attack'
            else:
                if 'attack' in self.status:
                    self.status = self.status.replace('_attack','')

    def mov(self,fast):
        #magnitude length of vector
        if self.movement.magnitude()!=0:
            self.movement = self.movement.normalize()
        
        self.oof.x += self.movement.x * fast
        self.RTA('horizontal')
        self.oof.y += self.movement.y * fast
        self.RTA('vertical')
        self.rect.center= self.oof.center


    def RTA(self,movement):
        if movement == 'horizontal':
            for sprite in self.two_sprites:
                if sprite.oof.colliderect(self.oof):
                    if self.movement.x > 0: 
                        self.oof.right = self.oof.left
                    if self.movement.x <0:
                        self.oof.left = self.oof.right
        if movement == 'vertical':
             for sprite in self.two_sprites:
                if sprite.oof.colliderect(self.oof):
                    if self.movement.y > 0: 
                        self.oof.bottom = self.oof.top
                    if self.movement.y <0:
                        self.oof.top = self.oof.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attack = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]

		# loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

		# set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.oof.center)

    def update(self):
        self.click()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.mov(self.fast)