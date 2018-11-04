import gui
import pygame
from quit import *
from game import *
from multiplayerscreen import *
from settingsscreen import *
from gui.dialog import *
from gui.image import *
from gui.checkbox import *
from gui.editfield import *

import select, socket

from players import *


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
		
		connection = self.connectHost()
		if connection == 'ABORTED':
			self.surface.blit(self.images['startscreen']['background'],(0,0))
			self.wm.paint(1,0)
			return
			
				
		player1 = Human(self.surface, self.images, self.locations, 2)
                player2 = MultiPlayer(self.surface, self.images, self.locations, connection, 1)
						
		#chat = Chat(self.surface, self.images, self.locations)
		chat = None
		
		from game import *
		
                game = Game(self.surface, self.images, self.locations, player1, player2)
                game.run()

                self.surface.blit(self.images['startscreen']['background'],(0,0))
                self.wm.paint(1,0)

	def join(self, trigger, event):
		self.surface.blit(self.images['multiplayerscreen']['connecting'],
			(int(self.locations['multiplayerscreen']['connecting_x']),
			int(self.locations['multiplayerscreen']['connecting_y'])))
		pygame.display.flip()

	 	connection = self.connectClient(self.host.getText())
                if connection == 'ABORTED':
                        self.surface.blit(self.images['startscreen']['background'],(0,0))
                        self.wm.paint(1,0)
                        return

		player1 = MultiPlayer(self.surface, self.images, self.locations, connection,0)
                player2 = Human(self.surface, self.images, self.locations, 2)

		#chat = Chat(self.surface, self.images, self.locations, self.host.getText())
		chat = None
		
		from game import *

                game = Game(self.surface, self.images, self.locations, player1, player2)
		game.run()

                self.surface.blit(self.images['startscreen']['background'],(0,0))
                self.wm.paint(1,0)

        def return_to_main(self, trigger, event):
		self.state = 1
		return widget.DONE
	
	def check_abort(self):
		while not self.abort:
			event = pygame.event.wait()
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				quit()
				return
				
	def connectHost(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('',50000))
		s.listen(1)
			
		result = 0
		while not result:
			(result, q, w) = select.select([s.fileno()],[],[],0.3)
			event = pygame.event.poll()
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				return 'ABORTED'
				
		connection, address = s.accept()
		connection.setblocking(0)

		return connection
	
	def connectClient(self, host):
		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		trytime = pygame.time.get_ticks()	
		while connection.connect_ex((host, 50000)):
			if pygame.time.get_ticks() > trytime + 10000:
				return 'ABORTED'
			pygame.time.wait(300)

		connection.setblocking(0)
		return connection
			
			
