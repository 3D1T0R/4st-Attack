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

import os
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

def setDisplay(resolution):
	screen = pygame.display.set_mode(resolution, FULLSCREEN)
	
	pygame.display.set_caption('4st Attack')
	pygame.mouse.set_visible(1)
	pygame.display.init()
	
	pygame.display.Info()
	return screen

def loadGraphic(image_name, resolution, themename):
	image_path = os.path.join('themes', themename, resolution, image_name)
	image = pygame.image.load(image_path).convert_alpha()
	return image

def loadGraphics(file_names, resolution, themename):
	images = {}
	for key in file_names.keys():
		images[key] = loadGraphic(file_names[key], resolution, themename)
	return images

def quit():
	pygame.quit()
	os._exit(0)

def main():                    
	settings = IniSettings('settings.ini').settings
	resolution = settings['video']['resolution']
	res = string.split(resolution, 'x')
	screen = setDisplay((int(res[0]), int(res[1])))

	# load all images
	images = {}
	img_files = IniSettings('themes/clean/graphics.ini')
	for key in img_files.settings.keys():
		images[key] = loadGraphics(img_files.settings[key], resolution, "clean")
		print "Loading:	", key

	locations = IniSettings('themes/clean/'+resolution+'/locations.ini').settings

	startscreen = StartScreen(screen, images, locations)
	startscreen.run()

if __name__ == '__main__':
	main()
