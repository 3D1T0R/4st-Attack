import gui
import pygame
from quit import *
from game import *
                
class EndScreen:
        def __init__(self, screen, images, settings, player):
                self.screen = screen
                self.images = images
                self.settings = settings
		self.exit_screen = 0
		self.player = player
        
        def run(self):
                self.display()
                while 1:
                        list=[]
                        list.append(pygame.event.wait())
                        self.handler.update(list)
			if self.exit_screen:
				return
                
        def display(self):
                self.handler = gui.Handler()
                self.image = self.screen
		# Display the winner image
                self.image.blit(self.images['winner'+str(self.player)], (
			int(self.settings.getLocations()['endscreen']['winner_x']),
			int(self.settings.getLocations()['endscreen']['winner_y'])))
                pygame.display.flip()

                self.handler.add(gui.Button( self.image, '',
                        (int(self.settings.getLocations()['endscreen']['return_x']),
                        int(self.settings.getLocations()['endscreen']['return_y']),
                        self.images['b_return'].get_width(), self.images['b_return'].get_height()),
                        background=self.images['b_return'],
                        align='center', valign='center',
                        onClick=self.return_to_main))
                

        def return_to_main(self, event):
		self.exit_screen = 1
