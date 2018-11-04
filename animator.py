import os, math, sys
import pygame, pygame.font, pygame.image, pygame.mixer, pygame.transform
from pygame.locals import *

class AnimatedObject:
	def getFrame(time):
		return
	def getSurface(time):
		return
	def getPosition(time):
		return

class AnimatedMoveObject:
	def __init__(self, image, startpos, endpos, playtime, delay=0):
		self.image = image
		self.startpos = startpos
		self.endpos = endpos
		self.playtime = playtime
		self.delta = (endpos[0]-startpos[0])/float(playtime), (endpos[1]-startpos[1])/float(playtime)
		self.delay = delay

	def getPosition(self, time):
		offset = (time-self.delay)

		x = self.startpos[0]+int(self.delta[0]*offset)
		y = self.startpos[1]+int(self.delta[1]*offset)
		return x,y

	def getSurface(self, time):
		return self.image

	def visable(self, time):
		if time < self.delay or time-self.delay > self.playtime: return None
		return 1

class AnimatedAlphaObject:
	def __init__(self, image, position, startalpha, endalpha, playtime, delay=0):
		#self.image = pygame.Surface( (image.get_width(),image.get_height()),pygame.locals.SRCALPHA)
		#self.image.blit(image,(0,0))
		self.image = image.convert()

		self.startalpha = startalpha
		self.endalpha = endalpha
		self.playtime = playtime
		if startalpha < endalpha:
			self.delta = (endalpha - startalpha)/float(playtime)
		else:
			self.delta = (startalpha - endalpha)/float(playtime)
		self.delay = delay
		self.position = position

	def getPosition(self, time):
		return self.position

	def getSurface(self, time):
		offset = (time-self.delay)
		alpha = int((self.delta*offset))
#		print self.image.get_alpha()
		self.image.set_alpha(alpha)
		return self.image


	def visable(self, time):
		if time < self.delay or time-self.delay > self.playtime: return None
		return 1

class AnimatedTurnObject:
	def __init__(self, image, position, number_of_turns, playtime, delay=0):
		self.image = image
		self.playtime = playtime
		self.delta = (number_of_turns*3.14)/float(playtime)
		self.delay = delay
		self.position = position

	def getPosition(self, time):
		offset = (time-self.delay)
		position = (self.position[0]-(math.sin(self.delta*offset)*self.image.get_width())/2, self.position[1])
		return position

	def getSurface(self, time):
		offset = (time-self.delay)

		return pygame.transform.scale(self.image, (math.sin(self.delta*offset)*self.image.get_width(), self.image.get_height()))


	def visable(self, time):
		if time < self.delay or time-self.delay > self.playtime: return None
		return 1

class AnimatedRotateObject:
	def __init__(self, image, position, number_of_turns, playtime, delay=0):
		self.image = image
		self.playtime = playtime
		self.delta = (number_of_turns*360)/float(playtime)
		self.delay = delay
		self.position = position

		self.cache={}
		for angle in range(360):
			self.cache[angle]=pygame.transform.rotozoom(self.image, angle, 1)

	def getPosition(self, time):
		offset = (time-self.delay)
		angle = int(self.delta*offset)%360
		return self.position[0]-self.cache[angle].get_width()/2, self.position[1]-self.cache[angle].get_height()/2

	def getSurface(self, time):
		offset = (time-self.delay)
		#return pygame.transform.rotozoom(self.image, self.delta*offset, 1)
		return self.cache[int(self.delta*offset)%360]


	def visable(self, time):
		if time < self.delay or time-self.delay > self.playtime: return None
		return 1


# Based on wavey by Pete Shinners
class AnimatedWaveObject:
	def __init__(self, x, y, font, message, fontcolor, offset=0.0, speed=0.001, amount=10):
		self.x = x
		self.y = y
		self.base = font.render(message, 0, fontcolor)
		self.steps = range(0, self.base.get_width(), 2)
		self.amount = amount
		self.size = self.base.get_rect().inflate(0, amount).size
		self.offset = offset
		self.speed = speed

	def getSurface(self, time):
		s = pygame.Surface(self.size)
		height = self.size[1]
		self.offset += self.speed * time
		for step in self.steps:
			src = Rect(step, 0, 2, height)
			dst = src.move(0, math.cos(self.offset + step*.02)*self.amount)
			s.blit(self.base, dst, src)
		return s

	def getPosition(self, time):
		return (self.x, self.y)

	def visable(self, time):
		return 1

class AnimatedFPSTimerObject:
	def __init__(self, x, y, font, fontcolor, background, average=0):
		self.x = x
		self.y = y
		self.average = average
		self.background = pygame.Surface((200,50))
		self.background.blit(background,(0,0))
		self.oldtime = 0
		self.font = font
		self.fontcolor = fontcolor

	def getSurface(self, time):
		if (time-self.oldtime):
			fps=1000/(time-self.oldtime)
		else:
			fps = 0
		message = "FPS: "+str(fps)
		surface = pygame.Surface((200,50))
		tekst = self.font.render(message, 0, self.fontcolor)
		surface.blit(self.background,(0,0))
		surface.blit(tekst,(0,0))
		self.oldtime = time
		return surface

	def getPosition(self, time):
		return (self.x, self.y)

	def visable(self, time):
		return 1

class Animator:
	def __init__(self, screen, background, playtime, objects = None):
		self.screen = screen
		self.background = background
		self.playtime = playtime
		self.objects = []
		self.starttime = -1
		self.oldrects = {}

	def addObject(self, object):
		self.objects.append(object)

	def drawFrame(self, time):
		for rect in self.oldrects.values():
			self.screen.blit(self.background.subsurface(rect), rect.topleft)

		rects_to_update = []
		newrects={}

		for object in self.objects:
			if(object.visable(time)):
				image = object.getSurface(time)
				position = object.getPosition(time)
				rect = self.screen.blit(image, position)
				newrects[object]=rect
				if self.oldrects.has_key(object):
					rects_to_update.append(rect.union(self.oldrects[object]))
				else:
					rects_to_update.append(rect)

		for key in (filter(lambda x,l=newrects.keys(): x not in l,self.oldrects.keys())):
			rects_to_update.append(self.oldrects[key])

		pygame.display.update(rects_to_update)
		self.oldrects = newrects

	def play(self):
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()
		self.starttime = pygame.time.get_ticks()
		time = pygame.time.get_ticks() - self.starttime

		while time < self.playtime:
			time = pygame.time.get_ticks() - self.starttime
			self.drawFrame(time)
		# Reset the clippin
		self.screen.set_clip(((0,0), self.background.get_size()))
