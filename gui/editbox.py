import pygame
from pygame.locals import *

import string

from object import Object

class Editbox(Object):
    """
    Editbox class for user input
    """

    def __init__(self,surface,rect,**kwargs):
        self.text     = ''
        self.bgcolor  = 255,255,255
        self.color    = 0,0,0
        self.maxchars = 0 # infinite
        # parse editbox specific arguments
        for key in kwargs.keys():
            if key == 'text':
                self.text = kwargs[key]
            elif key == 'maxchars':
                self.maxchars = kwargs[key]
            elif key == 'onChange':
                self.onChange = kwargs[key]
            elif key == 'onNewText':
                self.onNewText = kwargs[key]

        Object.__init__(self,surface,rect,**kwargs)

    def draw(self):
        """
        draw the widget!
        """
        self.surface.set_clip(self.rect)

        if hasattr(self,'background'):
            self.surface.blit(self.background,(self.rect[0],self.rect[1]))
        else:
            self.surface.subsurface(self.rect).fill(self.bgcolor)
        if hasattr(self,'rectcolor'):
            pygame.draw.rect(self.surface,self.rectcolor,
                             (self.rect[0],self.rect[1],self.rect[2]-1,self.rect[3]-1),1)

        if len(self.text) > 0:
            tmp = self.font.render(self.text,0,self.color)
            self.surface.blit(tmp,(self.rect[0]+2,self.rect[1]+2))

        pygame.display.update(self.rect)
        self.surface.set_clip()

    def keyDown(self,self2,key,unicode,mod):
        """
        key handler to add new text
        """
        if unicode >= '!' or unicode == ' ':
            self.text = self.text + unicode
            if self.maxchars:
                self.text = self.text[:self.maxchars]
            self.draw()
            self.change()
        elif key == K_BACKSPACE:
            if len(self.text) > 0:
                self.text = self.text[:-1]
                self.draw()
                self.change()
        elif key in [K_RETURN,K_KP_ENTER]:
            self.newText()

    def setText(self,text):
        self.text = text
        if self.maxchars:
            self.text = self.text[:self.maxchars]
        self.newText()

    def change(self):
        """
        handler forwarding to callback method
        """
        if hasattr(self,'onChange'):
            self.onChange(self,self.text)

    def newText(self):
        """
        handler forwarding to callback method
        """
        if hasattr(self,'onNewText'):
            # convert from unicode to normal strings
            self.onNewText(self,str(self.text))
