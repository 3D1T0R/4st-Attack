import time

class GameLogger:
	def newgame(self):
		self.move_number = 0
		self.logfile = open( "gamelog-%s.txt" % time.clock(), 'w')

	def logmove(self, move):
		self.move_number += 1
		self.logfile.write("%s,	%s\n" % (self.move_number, move))
