from board import *

# Checks if the move is legal
def isMoveLegal(board, selector_pos):
	return len(board.state[selector_pos]) < 6 and selector_pos >= 0

def isBoardFull(board):
	for pos in range(7):
		if len(board.state[pos]) < 6:
			return 0 
	return 1

def isWinner(board, player):
        if _isVerticalWin(board, player):
                return 4
        if _isHorizontalWin(board, player):
                return 4
        if _isDiagonalWin(board, player):
                return 4
        return 0


def _isVerticalWin(board, player):
        x = board.last_move
        four_in_a_row = [player, player, player, player]
        return board.state[x][-4:] == four_in_a_row


def _isHorizontalWin(board, player):
        x = board.last_move
        y = len(board.state[x]) - 1
        four_in_a_row = str(player) * 4
        row = []
        for i in range(-3, 4):
                try:
                        if x+i < 0: continue
                        row.append(str(board.state[x+i][y]))
                except IndexError:
                        row.append('s')  # 's' stands for sentinel
        return ''.join(row).find(four_in_a_row) >= 0


def _isDiagonalWin(board, player):
        x = board.last_move
        y = len(board.state[x]) - 1
        four_in_a_row = str(player) * 4
        row = []
        for i in range(-3, 4):
                try:
                        if x+i < 0: continue
                        if y+i < 0: continue
                        row.append(str(board.state[x+i][y+i]))
                except IndexError:
                        row.append('s')  # 's' stands for sentinel
        if ''.join(row).find(four_in_a_row) >= 0:
                return 1
        row = []
        for i in range(-3, 4):
                try:
                        if x+i < 0: continue
                        if y-i < 0: continue
                        row.append(str(board.state[x+i][y-i]))
                except IndexError:
                        row.append('s')  # 's' stands for sentinel
        if ''.join(row).find(four_in_a_row) >= 0:
                return 1
        return 0

"""

# Checks if theres a winner
def isWinner(board, player):

	# Check vertical wins
	for x in range(7):
		sequence = 0
		for y in range(len(board.state[x])):
			if board.state[x][y] == player:
				sequence += 1
				if sequence == 4:
					# Whe've got a winner!!
					return sequence
			else: sequence = 0
	# Check horizontal wins
	for y in range(6):
		sequence = 0
		for x in range(7):
			# Make sure we wont go out of bounds
			if len(board.state[x]) > y:
				if board.state[x][y] == player:
					sequence += 1
                	                if sequence == 4:
                        	               # Whe've got a winner!!
                                	       return sequence
				else: sequence = 0
			else: sequence = 0

	# Check diagonally - bottom to top
	for height in range(6+1-4):
		for start in range(7+1-4):
			sequence = 0
			for pos in range(7 - start):
				# Make sure we wont go out of bounds
	                        if len(board.state[pos+start]) > (pos + height):
				 	if board.state[pos+start][pos+ height] == player:
						sequence += 1
						if sequence == 4:
							# Whe've got a winner!!
							return sequence
					else: sequence = 0
				else: sequence = 0

	# Check diagonally - top to bottom
	for height in range(6+2-4):
		for start in range(7+1-4):
			sequence = 0
			for pos in range(7-start):
				# Make sure we wont go out of bounds
	                        if (len(board.state[pos+start]) > (6 - pos - height) )  and (6 - pos - height) >=0 :
				 	if board.state[pos+start][6 - pos - height] == player:
						sequence += 1
						if sequence == 4:
							# Whe've got a winner!!
							return sequence
					else: sequence = 0
				else: sequence = 0
	# No win for player
	return 0
"""