import pygame.transform

from label import Label

class Button(Label):
    """
    Class for two-state buttons
    """

    def __init__(self,surface,text,rect,**kwargs):
        self.pushed_color = 0,0,0
        self.state = 0
        
        # parse button specific arguments
        for key in kwargs.keys():
            if key == 'pushed_color':
                self.pushed_color = kwargs[key]
            elif key == 'pushed_background':
                tmp = kwargs[key]
                if tmp.get_size() == (rect[2],rect[3]):
                    self.pushed_background = tmp
                else:
                    self.pushed_background = pygame.transform.scale(tmp,(rect[2],rect[3]))
        Label.__init__(self,surface,text,rect,**kwargs)
        if self.pushed_color == (0,0,0):
            self.pushed_color = self.bgcolor

        
    def mouseButtonDown(self):
        self.state = 1
        self.draw()

    def mouseButtonUp(self):
        self.state = 0
        self.draw()

    def draw(self):
        tmp_bg = None
        if self.state:
            tmp = self.bgcolor
            self.bgcolor = self.pushed_color
            if hasattr(self,'pushed_background'):
                if hasattr(self,'background'):
                    tmp_bg = self.background
                else:
                    tmp_bg = None
                self.background = self.pushed_background
        
        Label.draw(self)

        if self.state:
            self.bgcolor = tmp
            if tmp_bg != None:
                self.background = tmp_bg
            else:
                if hasattr(self,'background'):
                    del self.background
