###############################################################################################
# $Id: canvas.py,v 1.1.1.1 2002/02/19 10:15:58 slmm Exp $
###############################################################################################

from widget import Widget
import widget
import pygame
import pygame.image
from pygame.locals import *

class Canvas (Widget):
    """
    This class defines a...
    """

    def __init__ (self, position = (0,0), size = (1,1), color = (0,0,0,0)):
        """Initializes the widget. Loads the icons from the passed filename."""

        # firts call superclass constructor
        Widget.__init__ (self, position, None)

        # create the surface
        self.surface = pygame.Surface ( (size[0], size[1]), HWSURFACE ).convert ()
 
    
#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
