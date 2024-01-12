import pygame, sys
from settings import *
from level import level

class RPG:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((width,height))
		pygame.display.set_caption('Meep')
		self.clock = pygame.time.Clock()

		self.level = level()

		# sound 
		m_sound = pygame.mixer.Sound('../audio/main.ogg')
		m_sound.set_volume(0.5)
		m_sound.play(loops = -1)
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(fps)

if __name__ == '__main__':
	game = RPG()
	game.run()