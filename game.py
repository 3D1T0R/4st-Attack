from board import *
from players import *
from rules import *
from settings import *
from endscreen import *
import pygame, pygame.font, pygame.image, pygame.mixer, pygame.transform
from pygame.locals import *
import gui
from quit import *
from gamelog import *

class Game:
	def __init__(self, screen, images, settings):
		self.screen = screen
		self.images = images
		self.settings = settings
	
	def run(self):
		self.gameloop()	
	
	# Graphics methods
	def drawPiece(self, piece, x, y):
        	self.screen.blit( piece, (
			int(self.settings.getLocations()['board']['x']) + x * piece.get_width(),
			int(self.settings.getLocations()['board']['y']) + (5-y) * piece.get_height()))
	
	def drawPieces(self, board):
        	for x in range(7):
                	for y in range(len(board.state[x])):
                        	if   board.state[x][y] == 1:
					self.drawPiece(self.images['stone1'], x, y)
	                        elif board.state[x][y] == 2:
					self.drawPiece(self.images['stone2'], x, y)

	def drawBoard(self, board):
        	self.screen.blit(self.images['back'], (
			int(self.settings.getLocations()['board']['x']),
			int(self.settings.getLocations()['board']['y'])))

	        self.drawPieces(board)

        	self.drawGrid()
	        return self.screen

	def drawGrid(self):
        	self.screen.blit(self.images['grid'], (
        		int(self.settings.getLocations()['board']['x']),
                        int(self.settings.getLocations()['board']['y'])))

	def doMove(self, selector_pos, stone):
		board.state[selector_pos].append(stone)
	        return board
	
	# Display the winner screen
	def winner(self, player):
		endscreen = EndScreen(self.screen, self.images, self.settings, player)
	        endscreen.run()
	        return 

	def loadPlayer(self, name):
		difficulty = int(self.settings.getGlobal()['game'][name+'_level'])
		
		if self.settings.getGlobal()['game'][name+'_type'] == 'human':
			player = Human(self.screen, self.images, self.settings, difficulty)
		elif self.settings.getGlobal()['game'][name+'_type'] == 'strategic':
			player = StrategicMinMax(self.screen, self.images, self.settings, difficulty)
		elif self.settings.getGlobal()['game'][name+'_type'] == 'random':
                        player = RandomAI(self.screen, self.images, self.settings, difficulty)
		elif self.settings.getGlobal()['game'][name+'_type'] == 'minmax':
                        player = MinMax(self.screen, self.images, self.settings, difficulty)
		elif self.settings.getGlobal()['game'][name+'_type'] == 'weighted':
                        player = WeightedMinMax(self.screen, self.images, self.settings, difficulty)
		else:
			print "INI FILE CURRUPT: set a player type to a legal one"
			print "Legal players include:"
			print "human, strategic, random, minmax"
			quit()

		return player
		
	# The gameloop
	def gameloop(self):
		self.screen.blit(self.images['background'], (0,0))
	
		player1 = self.loadPlayer('player1')
		player2 = self.loadPlayer('player2')

        	# Board generating code
	        board = Board()
        	# Board generating code

	        self.drawBoard(board)
        	pygame.display.flip()

		#Can be used for logging a game
		#gamelogger = GameLogger()
		#gamelogger.newgame()

	        while 1:
        	        move = player1.doMove(board, 1)
                	if rules.isMoveLegal(board, move):
                                board.move(move, 1)
				
				# Used for game log's
				#gamelogger.logmove(move)
				
                               	self.drawBoard(board)
	                        pygame.display.flip()
			else:
				print "BIG FAT ERROR!!!"
				quit()

        	        if rules.isWinner(board, 1):
				return self.winner(1)
			elif rules.isBoardFull(board):
				return self.winner(0)
	
			move = player2.doMove(board, 2)
			if rules.isMoveLegal(board, move):
                                board.move(move, 2)
				
				# Used for game log's
				#gamelogger.logmove(move)
                               	
				self.drawBoard(board)
	                        pygame.display.flip()
			else:
				print "BIG FAT ERROR!!!"
				quit()
        	        
			if rules.isWinner(board, 2):
				return self.winner(2)
			elif rules.isBoardFull(board):
				return self.winner(0)
