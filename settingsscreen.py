import gui
import pygame
from quit import *
from game import *
from gui.dialog import *
from gui.image import *
from gui.checkbox import *

class SettingsScreen(Dialog):
        def __init__(self, surface, images, locations):
                self.images = images
                self.locations = locations
		self.player = player
		Dialog.__init__(self, surface)
		
	def createWidgets(self):
		self.surface.blit(self.images['settingsscreen']['background'],(0,0))
	
		self.wm.register(Image(self.images['multiplayerscreen']['hostagame'],
			(int(self.locations['multiplayerscreen']['hostagame_x']),
			int(self.locations['multiplayerscreen']['hostagame_y']))
		))

		self.wm.register(CheckBox(self.images['gui']['checkbox_checked'], self.images['gui']['checkbox_unchecked'],
                        (int(self.locations['settingsscreen']['resolution1024_x']),
                        int(self.locations['settingsscreen']['resolution1024_y']))
			#callbacks={widget.MOUSEBUTTONUP : self.return_to_main }
                ))

		

		self.wm.register(Button(self.images['multiplayerscreen']['return'], self.images['multiplayerscreen']['return'],
			(int(self.locations['endscreen']['return_x']),
			int(self.locations['endscreen']['return_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.return_to_main }
                ))

        def return_to_main(self, trigger, event):
		self.state = 1
		return widget.DONE
