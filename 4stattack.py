#########################################################################
#                            4st Attack                                 #
#########################################################################
# Created by:                                                           #
# Main programming     - "slm" - Jeroen Vloothuis                       #
#                      - Tjerk Nan                                      #
# Graphics             - "The Corruptor" -- g@spank-the-monkey.org.uk   #
# Music                - Tjerk Nan                                      #
#########################################################################
# Specail thanks:                                                       #
# "CrashChaos" - Frank Raiser           for letting us nick his gui lib #
# Everyone in #pygame and the opensource community in general           #
#########################################################################
# This software is licensed under the GPL - General Public License      #
#########################################################################

import os
import pygame, pygame.font, pygame.image, pygame.mixer, pygame.transform
from pygame.locals import *
from startscreen import *
import settings
import profile

settings = Settings()

BACKGROUND_COLOR= (255,255,255,255)

pygame.init()

if settings.getGlobal()['sound']['music']=='yes':
	pygame.mixer.music.load(os.path.join('data', 'audio', settings.getTheme()['sound']['music']))
	pygame.mixer.music.play(-1)

# Declaration of the variables
images	= None
screen	= None
file_names_images = {
	'grid'		:'grid.png',	
	'back'		:'back.png',
	'stone1'	:'stone_1.png',
	'stone2'	:'stone_2.png',
	'selector'	:'selector.png',
	'splash'	:'splash.png',
	'won_1'		:'won_1.png',
	'won_2'		:'won_2.png',
	'background'	:'background.png'
}

def setDisplay():
	mode = DOUBLEBUF

	if(settings.getGlobal()['video']['fullscreen']=='yes'):
		mode = FULLSCREEN
	
	screen = pygame.display.set_mode( (int(settings.getGlobal()['video']['resolution_x']), 
		int(settings.getGlobal()['video']['resolution_y'])), mode )
	
	pygame.display.set_caption('4st Attack')
	pygame.mouse.set_visible(1)
	pygame.display.init()
	
	pygame.display.Info()
	return screen

def loadGraphic(image_name, resolution):
	image_path = os.path.join('data', 'graphics', settings.getGlobal()['theme']['name'],
		resolution, image_name)
	image = pygame.image.load(image_path).convert_alpha()
	return image

def loadGraphics(file_names, resolution):
	images = {}
	for key in file_names.keys():
		images[key] = loadGraphic(file_names[key], resolution)
	return images

def quit():
	pygame.quit()
	os._exit(0)

def main():
	startscreen = StartScreen(screen, images, settings)
	startscreen.run()

screen = setDisplay()
images = loadGraphics(settings.getTheme()['images'],
		settings.getGlobal()['video']['resolution_x'] + 'x' +
                settings.getGlobal()['video']['resolution_y'])

if __name__ == '__main__':
	main()
