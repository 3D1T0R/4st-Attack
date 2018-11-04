import gui
import pygame
from quit import *
from game import *
from gamescreen import *
from settingsscreen import *
from gui.dialog import *
from gui.image import *
from players import *
from creditsscreen import *

class StartScreen(Dialog):
	def __init__(self, surface, images, locations, ini_settings):
		self.images = images
		self.locations = locations
		self.ini_settings = ini_settings	
		Dialog.__init__ (self, surface)
		
	def createWidgets(self):
		# Set the background
		self.surface.blit(self.images['startscreen']['background'],(0,0))

		self.wm.register(Image(self.images['startscreen']['title'],
			(int(self.locations['startscreen']['title_x']),
			int(self.locations['startscreen']['title_y']))
		))
		self.wm.register(Button(self.images['startscreen']['newgame'], self.images['startscreen']['newgame'],
			(int(self.locations['startscreen']['newgame_x']),
			int(self.locations['startscreen']['newgame_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.newgame }
		))

		
		self.wm.register(Button(self.images['startscreen']['credits'], self.images['startscreen']['credits'],
			(int(self.locations['startscreen']['credits_x']),
			int(self.locations['startscreen']['credits_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.credits }
		))
		
		
		self.wm.register(Button(self.images['startscreen']['settings'], self.images['startscreen']['settings'],
			(int(self.locations['startscreen']['settings_x']),
			int(self.locations['startscreen']['settings_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.settings }
		))

		self.wm.register(Button(self.images['startscreen']['quit'], self.images['startscreen']['quit'],
			(int(self.locations['startscreen']['quit_x']),
			int(self.locations['startscreen']['quit_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.quit }
		))

	def newgame(self, trigger, event):
		gamescreen = GameScreen(self.surface, self.images, self.locations)
		gamescreen.run()
		self.surface.blit(self.images['startscreen']['background'],(0,0))
		self.wm.paint(1,0)

	def settings(self, trigger, event):
		settingsscreen = SettingsScreen(self.surface, self.images, self.locations, self.ini_settings)
		settingsscreen.run()
                self.surface.blit(self.images['startscreen']['background'],(0,0))
                self.wm.paint(1,0)

	def credits(self, trigger, event):
		creditsscreen = CreditsScreen(self.surface, self.images, self.locations)
		creditsscreen.run()
                self.surface.blit(self.images['startscreen']['background'],(0,0))
                self.wm.paint(1,0)

	def quit(self, trigger, event):
		quit()

	def loadPlayer(self, name):
                difficulty = 2 #int(self.settings.getGlobal()['game'][name+'_level'])

                if self.settings.getGlobal()['game'][name+'_type'] == 'human':
	                player = Human(self.screen, self.images, self.settings, difficulty)
                elif self.settings.getGlobal()['game'][name+'_type'] == 'strategic':
                        player = StrategicMinMax(self.screen, self.images, self.settings, difficulty)
		elif self.settings.getGlobal()['game'][name+'_type'] == 'random':
                        player = RandomAI(self.screen, self.images, self.settings, difficulty)
                elif self.settings.getGlobal()['game'][name+'_type'] == 'minmax':
			player = MinMax(self.screen, self.images, self.settings, difficulty)
                elif self.settings.getGlobal()['game'][name+'_type'] == 'weighted':
                        player = WeightedMinMax(self.screen, self.images, self.settings, difficulty)
                else:
			print "INI FILE CURRUPT: set a player type to a legal one"
		        print "Legal players include:"
		        print "human, strategic, random, minmax"
		        quit()

		return player
