# Created by Jeroen Vloothuis, 2002
import sys
from inisettings import *

def getOptions(argv):
	opts= {}
	while argv:
		if argv[0][0] == '-':
			opts[argv[0]] = argv[1]
			argv = argv[2:]
		else:
			argv = argv[1:]
	return opts


options = getOptions(sys.argv)

settings = IniSettings(options['-ini'])
for key in settings.settings.keys():
	for item in settings.settings[key].keys():
		settings.set(key,item, int(int(settings.settings[key][item])*float(options['-size'])))
settings.save()
