import pygame
from quit import *
from game import *
from multiplayerscreen import *
from settingsscreen import *
from gui.dialog import *
from gui.image import *
from players import *

class GameScreen(Dialog):
	def __init__(self, surface, images, locations):
		self.images = images
		self.locations = locations
		Dialog.__init__ (self, surface)
	
	def createWidgets(self):
		# Set the background
		self.surface.blit(self.images['gamescreen']['background'],(0,0))
		
		self.wm.register(Button(self.images['gamescreen']['humanvscpu'], self.images['gamescreen']['humanvscpu'],
			(int(self.locations['gamescreen']['humanvscpu_x']),
                        int(self.locations['gamescreen']['humanvscpu_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.humanvscpu }
		))
		self.wm.register(Button(self.images['gamescreen']['multiplayer'], self.images['gamescreen']['multiplayer'],
			(int(self.locations['gamescreen']['multiplayer_x']),
                        int(self.locations['gamescreen']['multiplayer_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.multiplayergame }
		))
		self.wm.register(Button(self.images['gamescreen']['back'], self.images['gamescreen']['back'],
                        (int(self.locations['gamescreen']['back_x']),
                        int(self.locations['gamescreen']['back_y'])),
                        callbacks={widget.MOUSEBUTTONUP : self.back }
                ))

	def humanvscpu(self, trigger, event):
		player1 = StrategicMinMax(self.surface, self.images, self.locations, 2)
		player2 = Human(self.surface, self.images, self.locations, 2)
		
		game = Game(self.surface, self.images, self.locations, player1, player2)
		game.run()
		
		self.surface.blit(self.images['startscreen']['background'],(0,0))
		self.wm.paint(1,0)

	def multiplayergame(self, trigger, event):
		multiplayerscreen = MultiplayerScreen(self.surface, self.images, self.locations)
		multiplayerscreen.run()
		self.surface.blit(self.images['startscreen']['background'],(0,0))
                self.wm.paint(1,0)

	def back(self, trigger, event):
		self.state = 1
		return widget.DONE

	def loadPlayer(self, name):
                difficulty = 4 #int(self.settings.getGlobal()['game'][name+'_level'])

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
