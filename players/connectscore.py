from minmax import *

# This class tries to add some strategic value to the min max algorithme
# this one does this by giving scores for stones based on their connections
class WeightedMinMax(MinMax):

	def score(self, node, player, opponent):
		player_score = 0
		opponent_score = 0

		for pos_x in range(7):
			for pos_y in range(len(node.board.state[pos_x])):
				player_score, opponent_score = self.stone_score(node, player, opponent, (pos_x, pos_y), 1, range(-1,1,1))
		
		return player_score #- opponent_score

	def stone_score(self, node, player, opponent, stone, score, stone_range):
		player_score = 0
		opponent_score = 0
		
		for x in stone_range:
			for y in stone_range:
				if (-1 < (stone[0] + x) < 7):
					if( -1 < (stone[1] + y) < len(node.board.state[stone[0] + x])):
						if node.board.state[stone[0] + x][stone[1] + y] == player:
							player_score +=	self.score_line(node, (stone[1] + y, stone[0] + x), (x,y), player)
						elif node.board.state[stone[0] + x][stone[1] + y] == opponent:
							opponent_score += score
		return player_score, opponent_score

	def score_line(self, node, stone, direction, player):
		score = 0
		for modifier in range(4):
			if(-1 < stone[0]+modifier*direction[0] < 7):
				if( -1 < (stone[1] + modifier*direction[1]) < len(node.board.state[stone[0] + modifier*direction[0]])):
					if node.board.state[stone[0]+modifier*direction[0]][stone[1]+modifier*direction[1]] == player:
						score += modifier
		return score
