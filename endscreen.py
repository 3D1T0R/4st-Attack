import gui
import pygame
from quit import *
from game import *
from gui.dialog import *
from gui.image import *

class EndScreen(Dialog):
        def __init__(self, surface, images, locations, player):
                self.images = images
                self.locations = locations
		self.player = player
		Dialog.__init__(self, surface)
		
	def createWidgets(self):

		self.wm.register(Image(self.images['endscreen']['winner'+str(self.player)],
			(int(self.locations['endscreen']['winner_x']),
			int(self.locations['endscreen']['winner_y']))
		))

		self.wm.register(Button(self.images['endscreen']['return'], self.images['endscreen']['return'],
			(int(self.locations['endscreen']['return_x']),
			int(self.locations['endscreen']['return_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.return_to_main }
                ))

        def return_to_main(self, trigger, event):
		self.state = 1
		return widget.DONE
