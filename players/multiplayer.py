# Echo server program
import socket
import rules

class MultiPlayer:
	def __init__(self, surface, images, locations, host = None):
		if host is None:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(('',50000))
			s.listen(1)
			self.connection, self.address = s.accept()

			self.myturn = 1
		else:
			self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection.connect((host, 50000))

			self.myturn = 0

		self.connection.setblocking(0)

	def doMove(self, board, player, event):
		# Transmit the last move first
		if self.myturn:
			# Add one to the last move before sending to make sure it
			# get's send: str(0) = ""
			self.connection.send(str(board.last_move+1))
			self.myturn = 0
		else:
			# Wait for a move to return
			try:
				# Convert the string to an int and substract the 1
				move = int(self.connection.recv(1024))-1
				self.myturn = 1
				return move
			except:
				return -1

	def gameOver(self, last_move):
		self.connection.send(str(last_move+1))