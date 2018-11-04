###############################################################################################
# $Id: widget_manager.py,v 1.1.1.1 2002/02/19 10:15:59 slmm Exp $
###############################################################################################

import pygame
import pygame.display
from pygame.locals import *
from widget import Widget
import widget

class WidgetManager:
    """
    This class defines a simple framework for managing widgets and their events. All created widgets
    should be added to a framework before they are of any use or can receive events. All SDL events
    should be sent to this framework for possible dispatching to widgets. If an event does not
    consern any widget the other parts of the application are free to do whatever they wish with the
    event.

    Every event should be sent to handle() as the raw SDL event as received from pygame.event.poll ()
    or pygame.event.wait().
    """

    def __init__ (self, surface, dialog=None):
        """Initializes the instance"""

        # clear the list of registered widgets
        self.widgets = []

        # the previous mouse position, for enter/leave events
        self.last_pos = (-1, -1)

        # the surface widgets are painted on
        self.surface = surface

        # store the dialog too
        self.dialog = dialog
        

    def register (self, widget):
        """Register a widget within the widget manager. The widget will after it has been registered
        be able to receive various events."""
        # is the widget already in the list?
        if not widget in self.widgets:
            # nope, add it
            self.widgets.append ( widget )
            

    def deRegister (self, widget):
        """Removes the passed widget from the management."""
        # do we have the widget in the list?
        if widget in self.widgets:
            # yep, remove it
            self.widgets.remove ( widget )


    def paint (self, force = 0, clear = 0):
        """Repaints the surface if needed."""
        paintneeded = 0

        # should we clear the disply first?
        if clear:
            # yep, do that first
            self.surface.fill ( (0,0,0) ) 
            
        # loop over all widgets
        for widget in self.widgets:
            # paint widget 
            if widget.paint (self.surface, force):
                # it did something, so set the flag
                paintneeded = 1
                
        # is a paint needed?
        if paintneeded:
            # update the whole screen
            pygame.display.flip()
         

    def handle (self, event):
        """Handles the passed event. If the event is of any interest to any of the registred widgets
        the widgets are allowed to act on the event. If any widget handled the event then this
        method will return 1 to indicate that it should not be processed any further. A value of 0
        indicates that the event was not processed."""

        # what type of event do we have?
        if event.type == widget.KEYDOWN:
            # keyboard key pressed 
            return self.handleKeyDown (event)
            
        elif event.type == widget.KEYUP:
            # keyboard key released
            return self.handleKeyUp (event)

        elif event.type == widget.MOUSEMOTION:
            # mouse moved 
            return self.handleMouseMotion (event)

        elif event.type == widget.MOUSEBUTTONDOWN:
            # mouse button pressed
            return self.handleMousePressed (event)

        elif event.type == widget.MOUSEBUTTONUP:
            # mouse button released 
            return self.handleMouseReleased (event)

        elif event.type == widget.USEREVENT:
            # timer event
            return self.handleTimer (event)

        elif event.type == widget.QUIT:
            # player wants to quit
            print "*** player wants to quit, what should we do? ***"
            
        # it was none of our events
        return 0
    

    def handleKeyDown (self, event):
        """Handles an event when a key was pressed but not yet released. Uses the last known
        position of the mouse to determine which widget has focus."""

        # by default we've not handled it
        handled = widget.UNHANDLED

        # loop over all widgets in the list
        for w in self.widgets:
            # is the mouse inside the widget?
            if w.isInside ( self.last_pos ):
                # have the widget handle the event
                w.handle ( widget.KEYDOWN, event )
                handled = widget.HANDLED
 
        return handled
       

    def handleKeyUp (self, event):
        """Handles an event when a pressed key released. Uses the last known
        position of the mouse to determine which widget has focus."""
        # by default we've not handled it
        handled = widget.UNHANDLED

        # loop over all widgets in the list
        for w in self.widgets:
            # is the mouse inside the widget?
            if w.isInside ( self.last_pos ):
                # have the widget handle the event
                w.handle ( widget.KEYUP, event )
                handled = widget.HANDLED

        return handled
     

    def handleMouseMotion (self, event):
        """Handles an event when the mouse pointer was moved within a widget."""

        # get the position of the mouse
        position = event.pos

        # by default we've not handled it
        handled = widget.UNHANDLED
        
        # loop over all widgets in the list
        for w in self.widgets:

            # is the mouse inside the widget?
            if w.isInside ( position ) and not w.isInside ( self.last_pos ):
                # have the widget handle the event
                w.handle ( widget.MOUSEENTEREVENT, event )
                handled = widget.HANDLED

            # is the mouse outside the widget
            elif not w.isInside ( position ) and w.isInside ( self.last_pos ):
                # have the widget handle the event
                w.handle ( widget.MOUSELEAVEEVENT, event )
                handled = widget.HANDLED

            # is the mouse the widget and the last move was too inside?
            elif w.isInside ( position ) and w.isInside ( self.last_pos ):
                # have the widget handle the event
                w.handle ( widget.MOUSEMOTION, event )
                handled = widget.HANDLED

        # store new last position
        self.last_pos = position

        return handled
            

    def handleMousePressed (self, event):
        """Handles an event when a mouse key was pressed but not yet released."""

        # get the position of the press
        position = event.pos
       
        # loop over all widgets in the list
        for w in self.widgets:
            # is the mouse inside the widget?
            if w.isInside ( position ):
                # have the widget handle the event
                status = w.handle ( widget.MOUSEBUTTONDOWN, event )

                # did it handle it?
                if status != widget.UNHANDLED:
                    # it handled it, we're done here
                    return status

        return widget.UNHANDLED
       

    def handleMouseReleased (self, event):
        """Handles an event when a pressed mouse button was released."""

        # get the position of the press
        position = event.pos
        
        # loop over all widgets in the list
        for w in self.widgets:
            # is the mouse inside the widget?
            if w.isInside ( position ):
                # have the widget handle the event
                status = w.handle ( widget.MOUSEBUTTONUP, event )

                # did it handle it?
                if status != widget.UNHANDLED:
                    # it handled it, we're done here
                    return status

        return widget.UNHANDLED


    def handleTimer (self, event):
        """Handles a timer event."""

        # do we have a dialog?
        if self.dialog != None:
            # yep, call it
            return self.dialog.timer ()
            
        # it was handled
        return widget.UNHANDLED
    
#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
