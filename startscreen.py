import gui
import pygame
from quit import *
from game import *

class StartScreen:
	def __init__(self, screen, images, settings):
		self.screen = screen
		self.images = images
		self.settings = settings
	
	def run(self):
		self.display()
		while 1:
			list=[]
			list.append(pygame.event.wait())
			self.handler.update(list)
		
	def display(self):
		self.handler = gui.Handler()
		self.image = self.screen
		self.image.blit(self.images['background'], (0,0))
		pygame.display.flip()

		self.handler.add(gui.Label( self.image, '',
			(int(self.settings.getLocations()['startscreen']['title_x']),
			int(self.settings.getLocations()['startscreen']['title_y']),
			self.images['l_title'].get_width(), self.images['l_title'].get_height()), 
			background=self.images['l_title'],
			align='center',	valign='center'))

		self.handler.add(gui.Button( self.image, '',
			(int(self.settings.getLocations()['startscreen']['newgame_x']),
                        int(self.settings.getLocations()['startscreen']['newgame_y']),
                        self.images['b_newgame'].get_width(), self.images['b_newgame'].get_height()),
                        background=self.images['b_newgame'],
			align='center', valign='center',
			onClick=self.newgame))
		
		self.handler.add(gui.Button( self.image, '',
			(int(self.settings.getLocations()['startscreen']['quit_x']),
                        int(self.settings.getLocations()['startscreen']['quit_y']),
                        self.images['b_quit'].get_width(), self.images['b_quit'].get_height()),
                        background=self.images['b_quit'],
                        align='center', valign='center',
                        onClick=self.quit))

	def newgame(self, event):
		game = Game(self.screen, self.images, self.settings)
		game.run()
		#self.image.blit(self.images['background'], (0,0))
		#self.handler.repaint()
		self.handler = 0
		self.display()

	def quit(self, event):
		quit()
