# Creditsscreen
from animator import *


class CreditsScreen:
	def __init__(self, surface, images, locations):
		self.images = images
		self.locations = locations

		background = self.images['credits']['background']
		programming =  self.images['credits']['programming']
		graphics =  self.images['credits']['graphics']
		thanks =  self.images['credits']['thanks']
		#pygame_image = pygame.image.load("credits/1024/pygame.png").convert_alpha()
		slm =  self.images['credits']['slm']
		chakie =  self.images['credits']['chakie']
		korruptor =  self.images['credits']['korruptor']

		bigfont = pygame.font.Font(None, 60)
		white = 255, 255, 255

		self.animator = Animator(surface, background, 13000)

		# Programming
		self.animator.addObject(AnimatedTurnObject(programming, ((1024-programming.get_width())/2+programming.get_width()/2,200), 0.5, 3000))
		self.animator.addObject(AnimatedMoveObject(programming, ((1024-programming.get_width())/2,200), (-programming.get_width(),200), 1000, 3000))

		# Jeroen
		self.animator.addObject(AnimatedTurnObject(slm, ((1024-slm.get_width())/2+slm.get_width()/2,400), 0.5, 3000, 500))
		self.animator.addObject(AnimatedMoveObject(slm, ((1024-slm.get_width())/2,400), (1024,400), 1000, 3500))

		# Graphics
		self.animator.addObject(AnimatedTurnObject(graphics, ((1024-graphics.get_width())/2+graphics.get_width()/2,200), 0.5, 3000, 4500))
		self.animator.addObject(AnimatedMoveObject(graphics, ((1024-graphics.get_width())/2,200), (-graphics.get_width(),200), 1000, 7500))

		# Gareth
		self.animator.addObject(AnimatedTurnObject(korruptor, ((1024-korruptor.get_width())/2+korruptor.get_width()/2,400), 0.5, 3000, 5000))
		self.animator.addObject(AnimatedMoveObject(korruptor, ((1024-korruptor.get_width())/2,400), (1024,400), 1000, 8000))

		# Thanks
		self.animator.addObject(AnimatedTurnObject(thanks, ((1024-thanks.get_width())/2+thanks.get_width()/2,200), 0.5, 3000, 8000))
		self.animator.addObject(AnimatedMoveObject(thanks, ((1024-thanks.get_width())/2,200), (-thanks.get_width(),200), 1000, 11000))

		# Chakie
		self.animator.addObject(AnimatedTurnObject(chakie, ((1024-chakie.get_width())/2+chakie.get_width()/2,400), 0.5, 3000, 8500))
		self.animator.addObject(AnimatedMoveObject(chakie, ((1024-chakie.get_width())/2,400), (1024,400), 1000, 11500))

		#self.animator.addObject(AnimatedFPSTimerObject(0, 0, bigfont, white, background.subsurface(0,0,200,50) ))

	def run(self):
		self.animator.play()
		return
