import rules
from player import *
from random import *
import copy
from board import *
from minmax import *
from scoremap import *

class Node:
	def __init__(self, board, parent, move, player):
		self.board = board
		self.parent = parent
		self.value = 1
		self.childs = []
		self.move = move
		self.player = player

	def __repr__(self):
		if self.childs > 1:
			number=0
			for child in self.childs:
				number=number+1
			return "Has %s child(s)" % number
		return "STATE"

# This class tries to add some strategic value to the min max algorithme
class StrategicMinMax(MinMax):
	def __init__(self, screen, images, settings, difficulty):
		self.scoremap = ScoreMap()
		#self.scoremap.randomizeMap()
		MinMax.__init__(self, screen, images, settings, difficulty)

	def score(self, node, player, opponent):
		current_score    = 0

		scoremap = ScoreMap()

		for y in range( len(node.board.state[3]) ):
			if node.board.state[3][y] == opponent and y != 0:
				for x in range(7):
					scoremap.setStoneScore(x,y, scoremap.getStoneScore(x, y)+8)

			if node.board.state[3][0] == opponent:
				if ((len(node.board.state[2]) and node.board.state[2][0]==player) and (len(node.board.state[4]) and node.board.state[4][0]==opponent)):
					scoremap.setStoneScore(2,0, 80)
				if ((len(node.board.state[4]) and node.board.state[4][0]==player) and (len(node.board.state[2]) and node.board.state[2][0]==opponent)):
					scoremap.setStoneScore(4,0, 80)

		number_of_stones = 0

		for x in range(7):
			for y in range(len(node.board.state[x])):
				if node.board.state[x][y] == player:
					current_score += scoremap.getStoneScore(x, y)
					number_of_stones += 1
				"""
				else:
					current_score -= scoremap.getStoneScore(x, y)
					number_of_stones += 1
				"""
		return (current_score * 100) / number_of_stones