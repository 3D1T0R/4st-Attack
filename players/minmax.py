import rules
from player import *
from random import *
import copy
from board import *

class Node:
	def __init__(self, board, move, player):
		self.board = board
		#self.parent = parent
		self.value = 0 
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

class MinMax(Player):
	type = 'AI'

	def __init__(self, screen, images, settings, difficulty):
                self.screen = screen
                self.images = images
                self.settings = settings
		self.search_depth = difficulty

	def evaluate(self, node, player, opponent, depth):
		if len(node.childs) > 0:
			list = []
			for child in node.childs:
				list.append(child.value)
			if node.player == player:
				node.value = min(list)
			else:
				node.value = max(list)
	
                else:
			node.value = self.score(node, player, opponent)  / (depth + 1)

	def score(self, node, player, opponent):
		return int(random() * 100) - 50
	
	
	def makeBoard(self, move, board, player):
		temp_board = copy.deepcopy(board)
		temp_board.move(move, player)
	        return temp_board

	def listMoves(self, board, player):
		checkmove = rules.isMoveLegal
		
		options = []
		for move in range(7):
                        if checkmove(board, move):
                                options.append(move)
		return options

	def statespace(self, node, depth, current_player, player, opponent):
		if rules.isWinner(node.board, opponent):
			print "a lose up ahead"
                        node.value = -10000 + depth
                        return node
                elif rules.isWinner(node.board, player):
			node.value = 10000 - depth 
                        return node
		
		elif self.listMoves(node.board, 0) < 1:
			self.evaluate(node, player, opponent, depth)
			return node
		elif depth < self.search_depth:
			if current_player==2:
				next_player = 1
			else:
				next_player = 2
			for move in self.listMoves(node.board, current_player):
				node.board.move(move, current_player)
				
				node.childs.append(self.statespace(Node( node.board, move, player), depth+1, next_player, player, opponent))
				node.board.undomove(move)
				
		self.evaluate(node, player, opponent, depth)
		return node
		

	def doMove(self, current_board, player):
		board = copy.deepcopy(current_board)

		if player == 1: opponent = 2
		else: opponent = 1
		
		node = Node(board, 0, player)
			
		node =  self.statespace( node, 0, player, player, opponent);

		bestscore = -100000 
		best_moves = []
		print "New Round"
		for child in node.childs:
			print "Child value=", child.value, "move=", child.board.last_move
			if child.value >= bestscore:
				#if rules.isMoveLegal(board, child.board.last_move):
				if bestscore == child.value:
					#print "Move added"
					best_moves.append(child.move)
				else:
					#print "New best move"
					bestscore = child.value
					best_moves = [child.move]
		return best_moves[int(random()*len(best_moves))]
