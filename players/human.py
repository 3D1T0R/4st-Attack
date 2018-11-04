from player import *
import gui
import pygame, pygame.font, pygame.image, pygame.mixer, pygame.transform
from pygame.locals import *
import rules
from gui.dialog import *

class Human(Dialog):
	type = 'human'

	def __init__(self, surface, images, locations, difficulty):
		self.images = images
		self.locations = locations
		Dialog.__init__ (self, surface)

	def createWidgets(self):
		for number in range(7):
			self.wm.register(Button(self.images['human']['column'+ str(number)], self.images['human']['column'+ str(number)],
	                        (int(self.locations['game']['column'+ str(number) +'_x']),
	                        int(self.locations['game']['column'+ str(number) +'_y'])),
	                        callbacks={widget.MOUSEBUTTONUP : self.setmove }, args=number
	                ))

	# This method returns the move to be made
	def doMove(self, board, player, event):
		self.move = -1
		self.board = board
		# Reset the move to an illegal one
		self.move = -1
		self.handleEvent(event)
		if self.move >-1 and self.move < 7:
			return self.move
		return -1

	def setmove(self, trigger, event, number):
		if rules.isMoveLegal(self.board, number):
			self.move = number
			return widget.DONE
	def gameOver(self, move):
		return None
