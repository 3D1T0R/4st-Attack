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

	def __repr__(self):
		if self.childs > 1:
			number=0
			for child in self.childs:
				number=number+1
			return "Has %s child(s)" % number
		return "STATE"	

class TreeAI(Player):
	type = 'AI'

	def __init__(self, screen, images, settings):
	        self.screen = screen
	        self.images = images
	        self.settings = settings
		self.search_depth = int(settings.getGlobal()['game']['ailevel'])


	def evaluate(self, node, player, opponent):
		if len(node.childs) > 0:
			list = []
			for child in node.childs:
				list.append(child.value)
			if node.player == player:
				node.value = min(list)
			else:
				node.value = max(list)

		else:
			if rules.isWinner(node.board, opponent):
				node.value = -10
			elif rules.isWinner(node.board, player):
				node.value = 10
			else:
				node.value = int(random() * 10) - 5 
	
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

	def statespace(self, node, depth, player):
		if self.listMoves(node.board, 0) < 1:
			node.value = 9
			return node
		elif depth < self.search_depth:
			if player==2:
				next_player = 1
			else:
				next_player = 2
			for move in self.listMoves(node.board, player):
				node.childs.append(self.statespace(Node( move, node, 0, player), depth+1, next_player))
		self.evaluate(node, 2, 1)
		return node
		

	def doMove(self, current_board, player):
		board = copy.deepcopy(current_board)
		# Build tree
		searchtree=[]

		node = Node(board, "", 0, player)
			
		node =  self.statespace( node, 0, player );

		print node
		print node.value

		bestscore = -10 
		move = 0
		for child in node.childs:
			print "Child value=", child.value
			if child.value > bestscore:
				if rules.isMoveLegal(board, child.board.last_move):
					bestscore = child.value
					move = child.board.last_move

		return move
		
		#while 1:
#		for move in range(7):
			#print "move", move
#			if rules.isMoveLegal(board, move):
#				searchtree.append(self.makeBoard(move, board, player))
		
#		for state in searchtree:
#			for move in range(7):
#				if rules.isMoveLegal(board, move):
#	                               state.append(self.makeBoard(move, board, player))
#		print searchtree

		return 0
