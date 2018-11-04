# Created by Jeroen Vloothuis, 2002
import ConfigParser
import string


# The IniSettings class, handles loading and saving of inifiles
# These files should have the following structure:
# [group0]
# key0 = value0
# key1 = value1
#
# [group1]
# key0 = value0
# key1 = value1
class IniSettings:
	def __init__(self, filename):
		self.filename = filename
		self.settings = self.__loadConfig()
	
	# Load the ini file into a dictionarie
	def __loadConfig(self):
    		config = {}
		cp = ConfigParser.ConfigParser()
		cp.read(self.filename)
		for sec in cp.sections():
			settings={}
			name = string.lower(sec)
			for opt in cp.options(sec):
				settings[string.lower(opt)] = string.strip(cp.get(sec, opt))
			config[name] = settings
		return config

	# Reload the config file
	def reload(self):
		self.__loadConfig()

	# Save all settings in the ini format
	def save(self):
		inifile = open(self.filename, 'w')
		for group in self.settings.keys():
			inifile.write("\n["+group+"]\n")
			for key in self.settings[group].keys():
				inifile.write(str(key)+"="+str(self.settings[group][key])+"\n")
	
	# Set a single value, requires a valid group and key
	def set(self, group, key, value):
		self.settings[group][key] = value
	
	# Set a complete dict of values, it doesnt delete groups, keys and values which are not
	# specified in the passed in dict. It only overides or makes additions. Structure of the
	# dict should be [group][key] = value
	def set_dict(dict):
		for group in dict.keys():
			for key in dict[group].keys():
				self.settings[group][key] = dict[group][key]
