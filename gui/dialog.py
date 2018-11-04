###############################################################################################
# $Id: dialog.py,v 1.3 2002/02/26 15:35:56 slmm Exp $
###############################################################################################

import pygame
import pygame.display
import pygame.event
import pygame.time
from pygame.locals import *
import widget
from widget import *
from button import Button
from label import Label
from widget_manager import WidgetManager
#import messagebox

# return codes used to indicate what should happen
ACCEPTED = 0
REJECTED = 1

class Dialog(Widget):
    """
    This class is used as a baseclass for dialogs. A dialog is a window with widgets that occupies
    the whole or part of the screen. Currently only whole screen dialogs are supported. This class
    contains the main widget manager to which widgets are added. Subclasses could override the
    method createWidgets() to create their own widgets, but that is not mandatory.

    It also contains the main event loop which is started using the method run(). The event loop
    handles events from all registered widgets and calls their callbacks.

    A dialog can have a background. It is set using setBackground() and can be either painted once
    or tiled over the entire screen.
    """

    # define a shared cache
    cache = {}

    def __init__ (self, surface):
        "Creates the dialog."
        # call superclass
        Widget.__init__ (self)
        
        # create the widget manager so that it manages our canvas and then paints out its stuff on
        # the root window
        self.wm = WidgetManager (surface, self)

	self.surface = surface

        # register ourselves as a paintable object to the widget manager. This should insure that we
        # get repainted too
        self.wm.register ( self )
        
        # create all widgets
        self.createWidgets ()

        # flags used for indicating what we've done
        self.state = REJECTED

        # no background
        self.background = None
        self.tile = 0

        
    def createWidgets (self):
        "Creates all widgets for the dialog. Override in subclasses."
        pass


    def setBackground (self, image, tile=0):
        """Sets a background for the entire dialog. The background is loaded from the passed
        'filename'. It is painted either only once or tiled, depending on the setting for 'tile'. A
        value of 1 will tile the image, any other value will draw the background once centered."""

        self.background = image 
            
        # store the tiling value
        self.tile = tile

        # we're dirty now
        self.dirty = 1
        

    def getWidth (self):
        "Returns the width of the dialog."
        return 0


    def getHeight (self):
        "Returns the height of the widget."
        return 0


    def getGeometry (self):
        """Returns the geometry of the widget. This is a tuple containing the x, y, width and height
        of the dialog. Not currently meaningful."""
        return ( self.position [0], self.position [1], 0, 0 )


    def isInside (self,position):
        """Checks wether the passed point is inside the dialog. Returns 1 if inside and 0 if
        outside. A point on the border of the widget is considered to be inside. Currently always
        returns 0."""
        # not inside
        return 0


    def paint (self, destination, force=0):
        """Method that paints the dialog. This method will simply blit out the background if one has
        been set. Override if custom painting is needed."""
        # are we dirty or not?
        if self.background == None or ( self.dirty == 0 and force == 0 ):
            # not dirty, or no background nothing to do here
            return 0

        # get the dimensions of the background
        width, height = self.background.get_size () 
        
        # should we tile or not?
        if self.tile:
            # perform tiling of the background
            for y in range ( self.surface.get_height() / height + 1 ):
                for x in range ( self.surface.get_width() / width + 1 ):
                    # what height should be used?
                    if y * height > self.surface.get_height:
                        # use only the missing part
                        heighty = (( y + 1 ) * height) - self.surface.get_height()

                    else:
                        # full height of icon
                        heighty = height

                    # what width should be used?
                    if x * width > self.surface.get_width():
                        # use only the missing part
                        widthx = (( x + 1 ) * width) - self.surface.get_width()

                    else:
                        # full width of icon
                        widthx = width

                        # blit it all out
                        destination.blit ( self.background, (x * width, y * height ) )
                        
        else:
            # no tiling, just blurt it out once
            destination.blit ( self.background, self.position )

        self.dirty = 0
        
        # we did something, make sure the widget manager knows that
        return 1



    def run (self):
        """Executes the dialog and runs its internal loop until a callback returns widget.DONE. When
        that dialog is terminated this method also returns.""" 

        # loop forever
        while 1:
            # repaint the stuff if needed
            self.wm.paint ()

            # get next event
            event = pygame.event.wait()

            # see wether the widget manager wants to handle it
            if event != -1:
                # handle event and get the return code that tells us wehter it was handled or not
                returncode = self.wm.handle ( event )

                # is the event loop done?
                if returncode == widget.DONE:
                    # disable the timer
                    self.disableTimer ()

                    return self.state

    def handleEvent(self, event):
		# repaint the stuff if needed
 		self.wm.paint ()

		# see wether the widget manager wants to handle it
		if event != -1:
                	# handle event and get the return code that tells us wehter it was handled or not
                	returncode = self.wm.handle ( event )

			# is the event loop done?
			if returncode == widget.DONE:
				# disable the timer
				self.disableTimer ()

				return self.state
			else:
				return -1
		else:
			return -1


    def accept (self):
        """Accepts the dialog. Will close it and return from it's event loop with the return status
        'dialog.ACCEPTED'."""
        # we're accepting the dialog
        self.state = ACCEPTED

        return widget.DONE


    def reject (self, trigger, event):
        """Accepts the dialog. Will close it and return from it's event loop with the return status
        'dialog.REJECTED'."""
        # we're cancelling the dialog
        self.state = REJECTED
        
        return widget.DONE


    def messagebox (self, message):
        
        # failed to init network connection, show a messagebox
        messagebox.Messagebox ( message )

        # repaint the stuff if needed
        self.wm.paint (force=1, clear=1)


    def enableTimer (self, ms):
        """Enables timer events. Calling this method will make the method timer() get called every
        'ms' milliseconds. Call disableTimer() to disable the timer."""
        # just call the method, make no checks
        pygame.time.set_timer ( USEREVENT, ms )
            

    def disableTimer (self):
        """Disables timer events."""
        # just call the method, make no checks
        pygame.time.set_timer ( USEREVENT, 0 )

        # remove all old stale events that may have been left in the queue
        pygame.event.get ( [USEREVENT] )
   

    def timer (self):
        """Callback triggered when the dialog has enabled timers and a timer fires. This should be
        overridden by subclasses to provide the needed code."""
        # by default we're handled
        return widget.HANDLED
    

#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
