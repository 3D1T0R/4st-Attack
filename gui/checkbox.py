###############################################################################################
# $Id: checkbox.py,v 1.2 2002/05/21 20:49:51 slmm Exp $
###############################################################################################

from widget import Widget
import widget
import pygame
from pygame.locals import *

# needed for resetting the background
import copy

class CheckBox(Widget):
    """
    This class defines a checkbox which can be in a checked or unchecked state. The two needed
    images will be loaded by the constructor from the passed filenames.

    This class plays a small sound when the checkbox is toggled.
    """

    def __init__ (self, image_checked, image_unchecked, position = (0,0), checked = 0,
                  callbacks = None):
        """Initializes the widget. Loads the icons from the passed filenamea."""

        # firts call superclass constructor
        Widget.__init__ (self, position, callbacks)

        # load the icons
        self.checked   = image_checked 
        self.unchecked = image_unchecked 
        
        # store the default state
        self.state = checked

        # set the surface too, so that isInside() has something to check
        self.surface = self.checked

        # set our internal callbacks so that we can trap changes
        self.internal = {widget.MOUSEBUTTONUP : self.toggle }

	# set the original background to none, is used in the paint method
	self.original_background = None
 

    def isChecked (self):
        """Returns 1 if the checkbox is checked and 0 if it is not checked."""
        return self.state


    def setChecked (self, checked = 1):
        """Sets the checkbox as unchecked if the parameter is 0, and to checked for all other
        values. """
        if checked == 0:
            self.state = 0
        else:
            self.state = 1

        # we're dirty now
        self.dirty = 1


    def toggle (self, event):
        """Toggles the state of a checkbox."""
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

        # play a sound
        #audio.playSample ( self.sound_toggled )

        # we're dirty now
        self.dirty = 1
        

    def paint (self, destination, force=0):
        """Method that paints the editfield. This method will simply blit out the surface of the widget
        onto the destination surface. """

        if self.original_background is None:
		self.original_background = pygame.Surface(self.checked.get_size())
	        self.original_background.blit(destination.subsurface(
				self.position,
				(self.position[0]+self.checked.get_width(), self.position[1]+self.checked.get_height())
			), (0,0)
		)
	

	
        # are we dirty or not?
        if not self.dirty and not force:
            # not dirty, nothing to do here
            return 0

	destination.blit ( self.original_background, (self.position [0], self.position [1] ) )
        
	# what surface should we use?
        if self.state:
            usedsurface = self.checked
        else:
            usedsurface = self.unchecked
        
        # we're dirty, blit out the button
        destination.blit ( usedsurface, (self.position [0], self.position [1] ) )
             
        self.dirty = 0
        
        # we did something, make sure the widget manager knows that
        return 1

   
    
#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
