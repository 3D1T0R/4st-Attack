import ConfigParser
import string
import os

class Settings:
	def __init__(self):
		self.loadGlobal()
		self.loadTheme()
		self.loadLocations()
	
	# Load the ini files into dictionaries
	def LoadConfig(self, file):
    		config = {}
		cp = ConfigParser.ConfigParser()
		cp.read(file)
		for sec in cp.sections():
			settings={}
			name = string.lower(sec)
			for opt in cp.options(sec):
				settings[string.lower(opt)] = string.strip(cp.get(sec, opt))
			config[name] = settings
		return config

	def loadGlobal(self):
		self.common = self.LoadConfig(os.path.join('settings','global.ini'))

	def loadTheme(self):
		self.theme = self.LoadConfig(os.path.join('settings', 'themes',
			self.common['theme']['name'] + '.ini'))

	def loadLocations(self):
		self.locations = self.LoadConfig(os.path.join('data', 'graphics',
		                        self.common['theme']['name'],
					self.common['video']['resolution_x'] + 'x' +
					self.common['video']['resolution_y'],
					'locations' + '.ini'))
	
	def getGlobal(self):
		return self.common

	def getTheme(self):
		return self.theme

	def getLocations(self):
	        return self.locations
