import pygame
from pygame.locals import *

class Handler:
    """
    This class is the main event handler for all widgets.
    Call the update method as often as possible to update
    the current state of the GUI widgets.
    """

    def __init__(self):
        # registered widgets
        self.objects = []
        # active widget
        self.focused = None
        self.offset  = 0,0
        # object which mouse was last over
        self.mouseover = None

    def add(self,obj):
        """ register new widget for handler """
        if obj not in self.objects:
            self.objects.append(obj)
            if self.focused == None:
                self.setFocus(obj)

    def remove(self,obj):
        """ remove registered widget from handler """
        focused_obj = self.objects[self.focused]
        if obj in self.objects:
            self.objects.remove(obj)
        if focused_obj == obj:
            self.focused = None
        else:
            self.setFocus(focused_obj)

    def removeAll(self):
        """ remove all registered widgets from handler """
        self.objects = []
        self.focused = None

    def setFocus(self,obj):
        """ give focus to 'obj' """
        if not obj.can_focus: return
        if obj in self.objects:
            index = self.objects.index(obj)
            if self.focused == index: return
            if self.focused != None:
                if len(self.objects) > self.focused:
                    self.objects[self.focused].takeFocus()
            self.focused = index
            obj.setFocus()

    def update(self,list):
        """
        Update all registered GUI components
        Pass a list of all events to check in 'list'
        """
        # parse all events
        mouse_pos = pygame.mouse.get_pos()
        # find object where mouse is over
        old = self.mouseover
        self.mouseover = None
        for obj in self.objects:
            if obj.rect.collidepoint(mouse_pos[0]-self.offset[0],
                                     mouse_pos[1]-self.offset[1]):
                self.mouseover = obj
                break

        if not self.mouseover:
            if old:
                old.mouseOut()
        elif self.mouseover != old:
            if old:
                old.mouseOut()
            self.mouseover.mouseOver()
                    
        for e in list:
            # check all registered widgets
            if e.type == MOUSEBUTTONDOWN:
                if self.mouseover:
                    self.setFocus(self.mouseover)
                    self.mouseover.mouseButtonDown()
                    self.button_down_obj = self.mouseover
            elif e.type == MOUSEBUTTONUP:
                if self.mouseover:
                    self.setFocus(self.mouseover)
                    self.mouseover.mouseButtonUp()
                    self.mouseover.click()
            elif e.type == KEYDOWN:
                if e.key == K_TAB:
                    if self.focused == None:
                        if len(self.objects) > 0:
                            self.focused = 0
                    elif self.focused == len(self.objects):
                        for i in range(len(self.objects)):
                            if self.objects[i].can_focus:
                                self.focused = i
                                break
                    else:
                        old = self.focused
                        for i in range(len(self.objects)-1-self.focused):
                            if self.objects[i+1+self.focused].can_focus:
                                self.focused = i+1+self.focused
                                break
                        if old == self.focused:
                            for i in range(self.focused):
                                if self.objects[i].can_focus:
                                    self.focused = i
                                    break
                    if self.focused != None:
                        self.setFocus(self.objects[self.focused])
                    return
                        
                elif e.key in [K_SPACE,K_RETURN,K_KP_ENTER]:
                    if self.focused != None:
                        self.objects[self.focused].click()

                if self.focused != None and \
		   hasattr(self.objects[self.focused],'keyDown'):
                    self.objects[self.focused].keyDown(self,e.key,e.unicode,e.mod)

    def repaint(self):
        """
        Repaint all widgets
        """
        for obj in self.objects:
            obj.draw()
