import pygame,pygame.font,pygame.transform

class Object:
    """
    General GUI object class
    Baseclass for every widget
    """

    def __init__(self,surface,rect,**kwargs):
        self.surface   = surface
        self.focused   = 0
        self.rect      = pygame.Rect(rect)
        # parse optional args
        for key in kwargs.keys():
            if key == 'onMouseButtonDown':
                self.onMouseButtonDown = kwargs[key]
            elif key == 'onMouseButtonUp':
                self.onMouseButtonUp = kwargs[key]
            elif key == 'onClick':
                self.onClick = kwargs[key]
            elif key == 'onMouseOver':
                self.onMouseOver = kwargs[key]
            elif key == 'onMouseOut':
                self.onMouseOut = kwargs[key]
            elif key == 'background':
                tmp = kwargs[key]
                if tmp.get_size() == self.rect.size:
                    self.background = pygame.Surface(self.rect.size)
                    self.background.blit(tmp,(0,0))
                    self.background.set_alpha(tmp.get_alpha())
                else:
                    self.background = pygame.Surface(self.rect.size)
                    self.background.blit(pygame.transform.scale(tmp,self.rect.size),(0,0))
                    self.background.set_alpha(tmp.get_alpha())
            elif key == 'font':
                self.font = kwargs[key]
            elif key == 'color':
                self.color = kwargs[key]
            elif key == 'bgcolor':
                self.bgcolor = kwargs[key]
            elif key == 'rectcolor':
                self.rectcolor = kwargs[key]
            elif key == 'can_focus':
                self.can_focus = kwargs[key]

        if not hasattr(self,'font'):
            self.font = pygame.font.Font(None,16)
        if not hasattr(self,'color'):
            self.color = 255,255,255
        if not hasattr(self,'bgcolor'):
            self.bgcolor = 0,0,0
        if not hasattr(self,'can_focus'):
            self.can_focus = 1
        
        self.draw()

    def draw(self):
        pass

    def setFocus(self):
        """ give focus to this object """
        self.focused = 1

    def takeFocus(self):
        """ takes focus from this object """
        self.focused = 0

    # callback routines
    def mouseButtonDown(self):
        if hasattr(self,'onMouseButtonDown'):
            self.onMouseButtonDown(self)

    def mouseButtonUp(self):
        if hasattr(self,'onMouseButtonUp'):
            self.onMouseButtonUp(self)

    def click(self):
        if hasattr(self,'onClick'):
            self.onClick(self)

    def mouseOver(self):
        if hasattr(self,'onMouseOver'):
            self.onMouseOver(self)

    def mouseOut(self):
        if hasattr(self,'onMouseOut'):
            self.onMouseOut(self)
