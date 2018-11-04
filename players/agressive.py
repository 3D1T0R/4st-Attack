import rules
from player import *
from random import *
import copy
from board import *

class Node:
	def __init__(self, board, parent, move, player):
		self.board = board
		self.parent = parent
		self.value = 1
		self.childs = []
		self.move = move
		self.player = player

		self.wins_score = 0
		self.lose_score = 0

	def __repr__(self):
		if self.childs > 1:
			number=0
			for child in self.childs:
				number=number+1
			return "Has %s child(s)" % number
		return "STATE"	

class Agressive(Player):
	type = 'AI'

	def __init__(self, screen, images, settings):
                self.screen = screen
                self.images = images
                self.settings = settings
		self.search_depth = int(settings.getGlobal()['game']['ailevel'])

	def evaluate(self, node, player, opponent, depth):
		if rules.isWinner(node.board, opponent):
	                node.value = -100 / (depth + 1) 
	        elif rules.isWinner(node.board, player):
	                node.value = 100 / (depth + 1)
		
		elif len(node.childs) > 0:
			list = []
			for child in node.childs:
				list.append(child.value)
			if node.player == player:
				node.value = min(list)
			else:
				node.value = max(list)
                else:
			node.value = self.score(node, player, opponent)  / (depth + 1)

		# The "argessive" way of evaluation
		if len(node.childs) > 0:
			for child in node.childs:
				node.wins_score = node.wins_score + child.wins_score
				node.lose_score += child.lose_score
				# Check if it is a win
				if child.value > 0:
					node.wins_score = node.wins_score + 1
				elif child.value < 0:
					node.lose_score += 1

	def score(self, node, player, opponent):
		# Not relevant for this function
		return 0
	
	
	def makeBoard(self, move, board, player):
		temp_board = copy.deepcopy(board)
		temp_board.move(move, player)
	        return temp_board

	def listMoves(self, board, player):
		options = []
		for move in range(7):
                        if rules.isMoveLegal(board, move):
                                options.append(self.makeBoard(move, board, player))
		return options

	def statespace(self, node, depth, current_player, player, opponent):
		if self.listMoves(node.board, 0) < 1:
			self.evaluate(node, player, opponent, depth)
			return node
		elif depth < self.search_depth:
			if current_player==2:
				next_player = 1
			else:
				next_player = 2
			for move in self.listMoves(node.board, current_player):
				node.childs.append(self.statespace(Node( move, node, 0, player), depth+1, next_player, player, opponent))
		self.evaluate(node, player, opponent, depth)
		return node
		

	def doMove(self, current_board, player):
		board = copy.deepcopy(current_board)

		if player == 1: opponent = 2
		else: opponent = 1
		
		node = Node(board, "", 0, player)
			
		node =  self.statespace( node, 0, player, player, opponent);

		bestscore = -100
		wins_score = -1 
		move = 0
		print "New Round"

		for child in node.childs:
			print "Child value=", child.value, "score=", child.wins_score
			if child.value > bestscore:
				if rules.isMoveLegal(board, child.board.last_move):
					bestscore = child.value
					move = child.board.last_move
			elif child.value == bestscore:
				if child.wins_score > wins_score:
					wins_score = child.wins_score
					move = child.board.last_move

		
		
		return move
