import gui
import pygame
from quit import *
from game import *
from gui.dialog import *
from gui.image import *
from gui.checkbox import *
from gui.editfield import *

class MultiplayerScreen(Dialog):
        def __init__(self, surface, images, locations):
                self.images = images
                self.locations = locations
		self.player = player
		Dialog.__init__(self, surface)

	def createWidgets(self):
		self.surface.blit(self.images['multiplayerscreen']['background'],(0,0))
	
		self.wm.register(Button(self.images['multiplayerscreen']['hostagame'], self.images['multiplayerscreen']['hostagame'],
			(int(self.locations['multiplayerscreen']['hostagame_x']),
			int(self.locations['multiplayerscreen']['hostagame_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.host }
		))

		"""
		self.wm.register(CheckBox(self.images['gui']['checkbox_checked'], self.images['gui']['checkbox_unchecked'],
                        (int(self.locations['multiplayerscreen']['test_x']),
                        int(self.locations['multiplayerscreen']['test_y']))
			#callbacks={widget.MOUSEBUTTONUP : self.return_to_main }
                ))
		"""

		self.host = EditField( pygame.font.Font(None, 24), text = "localhost", width = int(self.locations['multiplayerscreen']['textfield_size']), position = (
			int(self.locations['multiplayerscreen']['textfield_x']),
			int(self.locations['multiplayerscreen']['textfield_y'])
		),
			cursor = self.images['gui']['cursor'], frameicons = self.images['frame'])
		self.wm.register(self.host)

		self.wm.register(Button(self.images['multiplayerscreen']['joinagame'], self.images['multiplayerscreen']['joinagame'],
                        (int(self.locations['multiplayerscreen']['joinagame_x']),
                        int(self.locations['multiplayerscreen']['joinagame_y'])),
                        callbacks={widget.MOUSEBUTTONUP : self.join }
                ))


		self.wm.register(Button(self.images['multiplayerscreen']['return'], self.images['multiplayerscreen']['return'],
			(int(self.locations['endscreen']['return_x']),
			int(self.locations['endscreen']['return_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.return_to_main }
                ))

	def host(self, trigger, event):
                self.surface.blit(self.images['multiplayerscreen']['awaitingconnection'],
			(int(self.locations['multiplayerscreen']['awaitingconnection_x']),
			int(self.locations['multiplayerscreen']['awaitingconnection_y'])))
		pygame.display.flip()

		player1 = Human(self.surface, self.images, self.locations, 2)
                player2 = MultiPlayer(self.surface, self.images, self.locations)
		#chat = Chat(self.surface, self.images, self.locations)
		chat = None
		
                game = Game(self.surface, self.images, self.locations, player1, player2)
                game.run()

                self.surface.blit(self.images['startscreen']['background'],(0,0))
                self.wm.paint(1,0)

	def join(self, trigger, event):
		player1 = MultiPlayer(self.surface, self.images, self.locations, self.host.getText())
                player2 = Human(self.surface, self.images, self.locations, 2)

		#chat = Chat(self.surface, self.images, self.locations, self.host.getText())
		chat = None

                game = Game(self.surface, self.images, self.locations, player1, player2)
		game.run()

                self.surface.blit(self.images['startscreen']['background'],(0,0))
                self.wm.paint(1,0)

        def return_to_main(self, trigger, event):
		self.state = 1
		return widget.DONE
