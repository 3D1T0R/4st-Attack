###############################################################################################
# $Id: image.py,v 1.1.1.1 2002/02/19 10:16:01 slmm Exp $
###############################################################################################

from widget import Widget
import widget
import pygame
import pygame.image
from pygame.locals import *

class Image (Widget):
    """
    This class defines a simple image on the screen. No interaction can be had with it. It needs a
    filename from which the surface is loaded.
    """

    # define a shared cache
    cache = {}

    def __init__ (self, image, position = (0,0), callbacks = None):
        """Initializes the widget. Loads the icons from the passed filename."""

        # firts call superclass constructor
        Widget.__init__ (self, position, callbacks)

        self.surface = image
       
#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
