from gui.dialog import *
from gui.image import *
from gui.checkbox import *
from gui.editfield import *
import socket

# The chat class, id implements all the chat crap i need
class Chat(Dialog):
	def __init__(self, surface, images, locations, host=None):
		self.images = images
                self.locations = locations

		if host is None:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(('',50001))
			s.listen(1)
			self.connection, self.address = s.accept()
		else:
			self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection.connect((host, 50001))

		self.connection.setblocking(0)

		surface.blit(self.images['startscreen']['background'],(0,0))

		Dialog.__init__(self, surface)
		# we want timer events
		self.enableTimer ( 3000 )
		#Dialog.run(self)


	def createWidgets(self):
		# Set the background
		#self.surface.blit(self.images['chat']['background'],(0,0))

		self.wm.register(Button(self.images['chat']['send'], self.images['chat']['send'],
			(int(self.locations['chat']['send_x']),
                        int(self.locations['chat']['send_y'])),
			callbacks={widget.MOUSEBUTTONUP : self.send }
		))

		self.r_message = Label(pygame.font.Font('fonts/lucida.ttf', 14),"appeltaart",
			(int(self.locations['chat']['message_x']),
                        int(self.locations['chat']['message_y']))
		)

		self.wm.register(self.r_message)

		self.s_message = EditField( pygame.font.Font("fonts/lucida.ttf", 14), text = "slm.ath.cx", width = 200, position = (10,20),
			cursor = self.images['gui']['cursor'], frameicons = self.images['frame'])
		self.wm.register(self.s_message)
 
	def receive(self):
		try:
			text = self.connection.recv(1024)
		except:
			text = self.r_message.getText()

		self.r_message.setText(text)
		#print text

	def send(self, trigger, event):
		text = self.s_message.getText()
		self.connection.send(str(text))
		self.s_message.setText(" ")

	def timer (self):
		self.receive()
