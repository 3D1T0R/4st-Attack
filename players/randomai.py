import rules
from player import *
from random import *

class RandomAI(Player):
	type = 'AI'

	def __init__(self, screen, images, settings, difficulty):
		type = 'AI'

	def doMove(self, board, player):
		while 1:
			move = int(random() * 7)
			if rules.isMoveLegal(board, move):
				return move
