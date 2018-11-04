###############################################################################################
# $Id: label.py,v 1.3 2002/02/26 15:35:56 slmm Exp $
###############################################################################################

import pygame
from pygame.locals import *
from widget import Widget
import widget

class Label(Widget):
    """
    This class defines a simple label with a text rendered in a certain font. 
    """

    def __init__ (self, font, text, position = (0,0), callbacks = None,
                  color = (255,255,255), background = (0,0,0), background_image = None):
        """Initializes the widget. Renders the font using the passed data."""

        # firts call superclass constructor
        Widget.__init__ (self, position, callbacks)

        # create the surface
        self.surface = font.render ( text, 1, color )

        # store the needed data so that we can set the text later
        self.font = font
        self.color = color
        self.background = background
	self.background_img = background_image

        # store our text too
        self.text = text


    def setText (self, text):
        """Sets a new text for the label. Renders the new label using the font and colors passed in
        the constrctor."""



        # create the surface
	try:
		textsurface = self.font.render( text, 1, self.color )
		self.surface = textsurface
		if self.background_img:
			self.surface.blit(self.background_img,(0,0))

		# store the new text
		self.text = text

		# we're dirty now
		self.dirty = 1
	except:
		return

    def getText (self):
        """Returns the current text of the label."""
        return self.text



#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
