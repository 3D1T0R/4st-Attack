#import gui
import pygame
from quit import *
from game import *
from gui.dialog import *
from gui.image import *
from gui.checkbox import *

class SettingsScreen(Dialog):
        def __init__(self, surface, images, locations, ini_settings):
                self.images = images
                self.locations = locations
		self.player = player
		self.ini_settings = ini_settings
		Dialog.__init__(self, surface)
		
	def createWidgets(self):
		self.surface.blit(self.images['startscreen']['background'],(0,0))
	
		self.wm.register(Image(self.images['settingsscreen']['fullscreen'],
			(int(self.locations['settingsscreen']['fullscreen_x']),
			int(self.locations['settingsscreen']['fullscreen_y']))
		))
		
		self.wm.register(CheckBox(self.images['gui']['checkbox_checked'], self.images['gui']['checkbox_unchecked'],
                        (int(self.locations['settingsscreen']['fullscreen_toggle_x']),
                        int(self.locations['settingsscreen']['fullscreen_toggle_y'])),
			checked = self.ini_settings.settings['video']['fullscreen'] == 'yes',
			callbacks={widget.MOUSEBUTTONUP : self.fullscreen }
                ))

		# If sound system is available
		if pygame.mixer.get_init():
			self.wm.register(Image(self.images['settingsscreen']['music'],
				(int(self.locations['settingsscreen']['music_x']),
				int(self.locations['settingsscreen']['music_y']))
			))
			
			self.wm.register(CheckBox(self.images['gui']['checkbox_checked'], self.images['gui']['checkbox_unchecked'],
				(int(self.locations['settingsscreen']['music_toggle_x']),
				int(self.locations['settingsscreen']['music_toggle_y'])),
				checked = self.ini_settings.settings['sound']['music'] == 'yes',
				callbacks={widget.MOUSEBUTTONUP : self.music }
			))

		self.wm.register(Button(self.images['settingsscreen']['return'], self.images['settingsscreen']['return'],
			(int(self.locations['settingsscreen']['return_x']),
			int(self.locations['settingsscreen']['return_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.return_to_main }
                ))

        def return_to_main(self, trigger, event):
		self.state = 1
		return widget.DONE
		
	def fullscreen(self, trigger, event):
		if not (self.ini_settings.settings['video']['fullscreen'] == 'yes'):
			self.ini_settings.settings['video']['fullscreen'] = 'yes'
			pygame.display.toggle_fullscreen()
		else:
			self.ini_settings.settings['video']['fullscreen'] = 'no'
			pygame.display.toggle_fullscreen()
		self.ini_settings.save()
		
		self.wm.paint(1,0)
		
	def music(self, trigger, event):
		
		if not (self.ini_settings.settings['sound']['music'] == 'yes'):
			self.ini_settings.settings['sound']['music'] = 'yes'
			pygame.mixer.music.load( os.path.join(self.ini_settings.settings['path']['data'], 'music', 'definition.xm') )
			pygame.mixer.music.play(-1)
		else:
			self.ini_settings.settings['sound']['music'] = 'no'
			pygame.mixer.music.stop()
			
		self.ini_settings.save()
		
		self.wm.paint(1,0)
