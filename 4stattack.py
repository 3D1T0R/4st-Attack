#!/usr/bin/env python

#########################################################################
#                            4st Attack                                 #
#########################################################################
# Created by:                                                           #
# Main programming     - "slm" - Jeroen Vloothuis                       #
# Graphics             - "The Corruptor" -- g@spank-the-monkey.org.uk   #
#########################################################################
# Specail thanks:                                                       #
# Everyone in #pygame and the opensource community in general           #
#########################################################################
# This software is licensed under the GPL - General Public License      #
#########################################################################

import os, sys
import pygame, pygame.font, pygame.image, pygame.mixer, pygame.transform
from pygame.locals import *
from startscreen import *
from inisettings import *
import profile
import string

pygame.init()


# Declaration of the variables
images	= None
screen	= None


def playMusic(datadir):
	if pygame.mixer.get_init():
		pygame.mixer.music.load( os.path.join(datadir, 'music', '4stattack.ogg') )
		pygame.mixer.music.play(-1)

def getOptions(argv):
	opts= {}
	while argv:
		if argv[0][0] == '-':
			opts[argv[0]] = argv[1]
			argv = argv[2:]
		else:
			argv = argv[1:]
	return opts

def setDisplay(resolution, fullscreen):
	if fullscreen == 'yes':
		screen = pygame.display.set_mode(resolution, FULLSCREEN)
	else:
		screen = pygame.display.set_mode(resolution)
	
	pygame.display.set_caption('4st Attack 2')
	pygame.mouse.set_visible(1)
	pygame.display.init()
	
	pygame.display.Info()
	return screen

def loadGraphic(image_name, resolution, themename, datadir):
	image_path = os.path.join(datadir, 'themes', themename, resolution, image_name)
	image = pygame.image.load(image_path).convert_alpha()
	return image

def loadGraphics(file_names, resolution, themename, datadir):
	images = {}
	for key in file_names.keys():
		images[key] = loadGraphic(file_names[key], resolution, themename, datadir)
	return images

def quit():
	pygame.quit()
	os._exit(0)

def main():                    
	options = getOptions(sys.argv)
	
	if options.has_key('-ini'):
		ini_settings = IniSettings(options['-ini'])
	else:
		ini_settings = IniSettings('settings.ini')
	
	settings = ini_settings.settings
	
	datadir = settings['path']['data']
	
	if settings['sound']['music'] == 'yes':
		playMusic(datadir)
	
	resolution = settings['video']['resolution']
	res = string.split(resolution, 'x')
	screen = setDisplay((int(res[0]), int(res[1])), settings['video']['fullscreen'])

	# load all images
	images = {}
	img_files = IniSettings(datadir + '/themes/clean/graphics.ini')
	for key in img_files.settings.keys():
		images[key] = loadGraphics(img_files.settings[key], resolution, "clean", datadir)
		#print "Loading:	", key

	locations = IniSettings(datadir + '/themes/clean/'+resolution+'/locations.ini').settings

	startscreen = StartScreen(screen, images, locations, ini_settings)
	startscreen.run()

if __name__ == '__main__':
	main()
