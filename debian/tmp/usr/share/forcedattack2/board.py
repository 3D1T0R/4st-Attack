import copy

class Board:
	# Setup an empty board
	def __init__(self):
		self.state = []
        	for x in range(7):
			self.state.append([])
		self.last_move = -1
	
	def move(self, move, player):
		self.state[move].append(player)
		self.last_move = move
	
	def domoves(self, moves):
		for (move, player) in moves:
			self.move(move, player)
			
	def undomove(self, move):
		if len(self.state[move]) > 0:
			del self.state[move][len(self.state[move])-1]
