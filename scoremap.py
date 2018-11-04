from random import *

# This class is a score map used by some of the ai players
class ScoreMap:

	def __init__(self):
		""" New and `improved'"""
		self.scoremap = [
			[3,4,5,7,5,4,3],
			[4,6,8,10,8,6,4],
			[5,8,12,13,12,8,5],
			[5,8,12,13,12,8,5],
			[4,6,8,10,8,6,4],
			[3,4,5,7,5,4,3]
		]
	
	# Get the score for a single stone
	def getStoneScore(self, x, y):
		# Reverse the x and y because the map is in a human readable form:
		# 6 x 7 horizontal array's
		return self.scoremap[y][x] 

		# Get the score for a single stone
	def setStoneScore(self, x, y, value):
		# Reverse the x and y because the map is in a human readable form:
		# 6 x 7 horizontal array's
		self.scoremap[y][x] = value

	# These are not implemented, there was no need for them anymore...yet?
	def loadScoreMap(file_name):
		return 0

	def saveScoreMap(file_name):
		return 0
	
	def updateScoreMap(board, player, win):
		return 0

	def randomizeMap(self):
		x_center = int (random()*5)
		y_center = int (random()*4)
		for x in [-1,0,1]:
			for y in [-1,0,1]:
				self.scoremap[y+y_center][x+x_center] = + int(random()*2)

