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

	def score(self, node, player, opponent):
		current_score    = 0

		scoremap = ScoreMap()
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
