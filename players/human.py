from player import * 
import gui
import pygame, pygame.font, pygame.image, pygame.mixer, pygame.transform
from pygame.locals import *
import rules

class Human(Player):
	type = 'human'

	def __init__(self, screen, images, settings, difficulty):
		self.screen = screen
		self.images = images
		self.settings = settings
	
	# This method returns the move to be made
	def doMove(self, board, player):
		# Reset the move to an illegal one
		self.move = -1
		self.display()

		while 1:
                        list=[]
                        list.append(pygame.event.wait())
                        self.handler.update(list)
			if rules.isMoveLegal(board, self.move):
				return self.move
		
	def display(self):
	        self.handler = gui.Handler()
	        self.image = self.screen
                # The game buttons, for selecting a column
                for number in range(7):
	                self.dropButton(self.handler, self.image, number)



	def dropButton(self, handler, image, number):
                # The game button, for selecting a column
		button = gui.IndexedButton( image, '',
        		(int(self.settings.getLocations()['gamescreen']['column'+ str(number) +'_x']),
                	int(self.settings.getLocations()['gamescreen']['column'+ str(number) +'_y']),
	                self.images['b_column'+str(number)].get_width(), self.images['b_column'+str(number)].get_height()),
        	        background=self.images['b_column'+str(number)],
                	align='center', valign='center',
			onClick=self.setmove)
		button.index = number
		self.handler.add(button)
	
	def setmove(self,  event):
		self.move = event.index
		print self.move
