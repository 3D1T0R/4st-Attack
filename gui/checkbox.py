import pygame.draw

from label import *

class Checkbox(Label):
    """
    Checkbox class
    """

    def __init__(self,surface,text,rect,**kwargs):
        self.checked      = 0
        self.pushed_color = 128,128,128

        # parse arguments for checkbox specific entries
        for key in kwargs.keys():
            if key == 'checked':
                self.checked = kwargs[key]
        
        Label.__init__(self,surface,text,rect,**kwargs)

    def click(self):
        self.checked = not self.checked
        Label.click(self)
        self.draw()

    def draw(self):
        self.surface.set_clip(self.rect)

        if hasattr(self,'background'):
            self.surface.blit(self.background,(self.rect[0],self.rect[1]))
        else:
            self.surface.subsurface(self.rect).fill(self.bgcolor)
        if hasattr(self,'rectcolor'):
            pygame.draw.rect(self.surface,self.rectcolor,
                             (self.rect[0],self.rect[1],self.rect[2]-1,self.rect[3]-1),1)
        
        tmp = self.rect
        self.rect = pygame.Rect(tmp[0]+15,tmp[1],tmp[2]-15,tmp[3])
        self.showText()
        self.rect = tmp

        # draw checkbox
        y = tmp[1]+tmp[3]/2
        self.surface.subsurface( (tmp[0]+2, y-5, 10, 10)).fill((255,255,255))

        if self.checked:
            pygame.draw.lines(self.surface, (0,0,0), 0,
                              ( (tmp[0]+3,y), (tmp[0]+5,y+4), (tmp[0]+11,y-4) ),2)

        self.surface.set_clip()
        pygame.display.update(self.rect)
