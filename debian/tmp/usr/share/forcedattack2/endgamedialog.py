import gui
import pygame
from quit import *
from game import *
from multiplayerscreen import *
from settingsscreen import *
from gui.dialog import *
from gui.image import *
from players import *

class EndGameDialog(Dialog):
	def __init__(self, surface, images, locations):
		self.images = images
		self.locations = locations
		Dialog.__init__ (self, surface)

	def createWidgets(self):
		# Set the background
		#self.surface.blit(self.images['endgamedialog']['background'],(0,0))

		self.wm.register(Image(self.images['endgamedialog']['message'],
			(int(self.locations['endgamedialog']['message_x']),
                        int(self.locations['endgamedialog']['message_y'])),
		))
		self.wm.register(Button(self.images['endgamedialog']['quit'], self.images['endgamedialog']['quit'],
			(int(self.locations['endgamedialog']['quit_x']),
                        int(self.locations['endgamedialog']['quit_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.quit }
		))
		self.wm.register(Button(self.images['endgamedialog']['keepplaying'], self.images['endgamedialog']['keepplaying'],
                        (int(self.locations['endgamedialog']['keepplaying_x']),
                        int(self.locations['endgamedialog']['keepplaying_y'])),
                        callbacks={widget.MOUSEBUTTONUP : self.keepplaying }
                ))

	def quit(self, trigger, event):
		self.state = "quit"
		return widget.DONE

	def keepplaying(self, trigger, event):
		self.state = "keeplaying"
		return widget.DONE