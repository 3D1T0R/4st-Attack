import pygame,pygame.draw

import string

from object import Object

class Label(Object):
    """
    General GUI label class
    """

    def __init__(self,surface,text,rect,**kwargs):
        self.text   = text
        self.align  = 'left'
        self.valign = 'top'
        self.can_focus = 0
        # parse label specific arguments
        for key in kwargs.keys():
            if key == 'align':
                self.align = kwargs[key]
            elif key == 'valign':
                self.valign = kwargs[key]

        Object.__init__(self,surface,rect,**kwargs)

    def setText(self,text):
        """ Sets new text and updates label """
        self.text = text
        self.draw()

    def showText(self):
        """
        Display label text (multiline support)
        """
        if len(self.text.split()) == 0: return

        bw,bh = self.rect.size
        text = self.text
        lines = []

        # some magic to divide the text into several lines
        while text:
            words = text.split(' ')
            for i in range(len(words)):
                str = string.join(words[:i])
                if '\n' in str:
                    str = str[:str.index('\n')]
                    if self.font.size(str)[0] > bw:
                        i = i -1
                    else:
                        # enforce newline
                        index = text.index('\n')
                        i = len( text[:index].split(' ') )
                        text = text[:index]+' '+text[index+1:]
                        words = text.split(' ')
                    break
                    
                if self.font.size(str)[0] > bw:
                    i = i-1
                    break
            if i == len(words)-1 or i == 0:
                lines.append(string.join(words))
                text = []
            elif i != 0:
                lines.append(string.join(words[:i]))
                text = string.join(words[i:])                

        count = 0
        if self.valign == 'bottom':
            lines.reverse()

        # now draw lines according to alignment options
        for line in lines:
            if line == '':
                count += 1
                continue
            tmp = self.font.render(line,0,self.color)
            x = self.rect[0]
            if self.align == 'right':
                x = self.rect[0] + self.rect[2] - tmp.get_width()
            elif self.align == 'center':
                x = self.rect[0] + (self.rect[2]-tmp.get_width())/2

            y = self.rect[1] + count*self.font.get_height()
            if self.valign == 'bottom':
                y = self.rect[1]+self.rect[3] - (count+1)*self.font.get_height()
            elif self.valign == 'center':
                y = self.rect[1] + self.rect[3]/2 - self.font.get_height() \
                    * ( len(lines)/2. - count)

            self.surface.blit(tmp,(x,y))
            count += 1
                
        
    def draw(self):
        """
        draw the widget!
        """
        self.surface.set_clip(self.rect)
        if hasattr(self,'background'):
            self.surface.blit(self.background,(self.rect[0],self.rect[1]))

	""" Commented out by Jeroen Vloothuis, so that there wont be a black box
	else:
            self.surface.subsurface(self.rect).fill(self.bgcolor)
        if hasattr(self,'rectcolor'):
            pygame.draw.rect(self.surface,self.rectcolor,
                             (self.rect[0],self.rect[1],self.rect[2]-1,self.rect[3]-1),1)
        self.showText()
	"""
        pygame.display.update(self.rect)
        self.surface.set_clip()
