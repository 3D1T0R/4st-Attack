from board import *
from players import *
from rules import *
from endscreen import *
import pygame, pygame.font, pygame.image, pygame.mixer, pygame.transform
from pygame.locals import *
import gui
from quit import *
from gamelog import *
import types
from endgamedialog import *

class Game:
	def __init__(self, screen, images, locations, player1, player2):
		self.screen = screen
		self.images = images
		self.locations = locations
		self.player1 = player1
		self.player2 = player2
			
	def run(self):
		self.gameloop()	
	
	# Graphics methods
	def drawPiece(self, piece, x, y):
        	self.screen.blit( piece, (
			int(self.locations['board']['x']) + x * piece.get_width(),
			int(self.locations['board']['y']) + (5-y) * piece.get_height()))
	
	def drawPieces(self, board):
        	for x in range(7):
                	for y in range(len(board.state[x])):
                        	if   board.state[x][y] == 1:
					self.drawPiece(self.images['game']['stone1'], x, y)
	                        elif board.state[x][y] == 2:
					self.drawPiece(self.images['game']['stone2'], x, y)

	def drawBoard(self, board):
        	self.screen.blit(self.images['game']['back'], (
			int(self.locations['board']['x']),
			int(self.locations['board']['y'])))

	        self.drawPieces(board)

        	self.drawGrid()
	        return self.screen

	def drawGrid(self):
        	self.screen.blit(self.images['game']['grid'], (
        		int(self.locations['board']['x']),
                        int(self.locations['board']['y'])))

	def doMove(self, selector_pos, stone):
		board.state[selector_pos].append(stone)
	        return board
	
	# Display the winner screen
	def winner(self, player):
		endscreen = EndScreen(self.screen, self.images, self.locations, player)
	        endscreen.run()
	        return


	# The gameloop
	def gameloop(self):
		self.screen.blit(self.images['game']['background'], (0,0))

		player1 = self.player1
		player2 = self.player2

        	# Board generating code
	        board = Board()
        	# Board generating code

	        self.drawBoard(board)
        	pygame.display.flip()

		#Can be used for logging a game
		#gamelogger = GameLogger()
		#gamelogger.newgame()

	        while 1:
			while 1:
    				event = pygame.event.poll()

				#self.chat.handleEvent(event)

				if event.type is KEYDOWN and event.key is K_ESCAPE:
					quitdialog = EndGameDialog(self.screen, self.images, self.locations)
					if quitdialog.run() is "quit":
						quit()
					else:
						self.drawBoard(board)
						pygame.display.flip()


        	        	move = player1.doMove(board, 1, event)
				if type(move) is types.IntType and rules.isMoveLegal(board, move):
					board.move(move, 1)
					break

			self.drawBoard(board)
			pygame.display.flip()

        	        if rules.isWinner(board, 1):
				player2.gameOver(move)
				player1.gameOver(move)
				return self.winner(1)
			elif rules.isBoardFull(board):
				player2.gameOver(move)
				player1.gameOver(move)
				return self.winner(0)

			while 1:
				event = pygame.event.poll()
				#self.chat.handleEvent(event)

        			if event.type is KEYDOWN and event.key is K_ESCAPE:
					quitdialog = EndGameDialog(self.screen, self.images, self.locations)
					if quitdialog.run() is "quit":
						quit()
					else:
						self.drawBoard(board)
						pygame.display.flip()


				move = player2.doMove(board, 2, event)
				if type(move) is types.IntType and rules.isMoveLegal(board, move):
                                	board.move(move, 2)
					break

			self.drawBoard(board)
	                pygame.display.flip()

			if rules.isWinner(board, 2):
				player1.gameOver(move)
				player2.gameOver(move)
				return self.winner(2)
			elif rules.isBoardFull(board):
				player1.gameOver(move)
				player2.gameOver(move)
				return self.winner(0)
