###############################################################################################
# $Id: fader.py,v 1.1.1.1 2002/02/19 10:15:59 slmm Exp $
###############################################################################################

from widget import Widget
import widget
import pygame
from pygame.locals import *

class Fader (Widget):
    """
    This class defines a simple surface that works as a fader widget. It covers a part of a dialog
    with asurface that can gradially become less and less transparent, thus fading the part of the
    dialog towards that color.

    Call the setAlpha() method periodically to alter alpha.
    """

    def __init__ (self, size=(0,0), position=(0,0), alpha=0, color=(0,0,0), callbacks=None):
        """Initializes the widget. Creates the surface."""

        # firts call superclass constructor
        Widget.__init__ (self, position, callbacks)

        # create the surface
        self.surface = pygame.Surface ( size )

        # set the alpha too
        self.surface.set_alpha ( alpha, RLEACCEL )

        # store alpha too
        self.alpha = alpha
        

    def getAlpha (self):
        """Returns current alpha value."""
        return self.alpha
    

    def setAlpha (self, alpha):
        """Sets a new alpha value for the fader."""
        # store new alpha
        self.alpha = alpha
        
        # set the alpha too
        self.surface.set_alpha ( alpha, RLEACCEL )

        # we're dirty now
        self.dirty = 1
        
       
#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
