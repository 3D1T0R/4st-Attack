import os
import pygame, pygame.font, pygame.image, pygame.mixer, pygame.transform
from pygame.locals import *
from gui.dialog import *

pygame.init()

mode = DOUBLEBUF

mode = FULLSCREEN
	
screen = pygame.display.set_mode( (1024,768) )
	
pygame.display.set_caption('4st Attack')
pygame.mouse.set_visible(1)
pygame.display.init()
	
pygame.display.Info()

def quit():
	pygame.quit()
	os._exit(0)

	


class TestDialog(Dialog):
	def __init__ (self, surface):
		Dialog.__init__ (self, surface)
	
	def createWidgets (self):
		self.wm.register ( Label (pygame.font.Font("lucida.ttf", 20), "Setup network information", (10, 10), color=(255, 0, 0)))

def main():
	testd = TestDialog(screen)
	testd.run()

if __name__ == '__main__':
	main()
