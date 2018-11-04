###############################################################################################
# $Id: button.py,v 1.1.1.1 2002/02/19 10:16:00 slmm Exp $
###############################################################################################

from widget import Widget
import widget
import pygame
import pygame.image
import pygame.mixer
from pygame.locals import *

class Button(Widget):
    """
    This class defines a simple pushbutton which can can be clicked. It needs a surfaces that
    represent the button. The surface will be loaded by the constructor from a passed filename.

    This class plays a small sound when the button is clicked.
    """

    # define a shared cache
    cache = {}

    def __init__ (self, button_image, button_image_pressed, position = (0,0), callbacks = None, sound_clicked = None, args = None):
        """Initializes the widget. Loads the icons from the passed filename."""

        # firts call superclass constructor
        Widget.__init__ (self, position, callbacks, args)

        self.surface_released = button_image 
            
        self.surface_pressed = button_image_pressed          

        # initial surface is the non-pressed one
        self.surface = self.surface_released
 
        # set our internal callbacks so that we can trap keys
        self.internal = {widget.MOUSEBUTTONUP   : self.mouseUp,
                         widget.MOUSEBUTTONDOWN : self.mouseDown }


    def mouseUp (self, event):
        """Internal callback triggered when the mouse is released when it is over a button. This
        sets a new icon for the button."""
        # set the new icon
        self.surface = self.surface_released

        # play a sound
        #audio.playSample ( self.sound_clicked )
        
        # we're dirty
        self.dirty = 1


    def mouseDown (self, event):
        """Internal callback triggered when the mouse is pressed when it is over a button. This
        sets a new icon for the button."""
        # set the new icon
        self.surface = self.surface_pressed

        # we're dirty
        self.dirty = 1

        
#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
