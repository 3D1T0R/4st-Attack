###############################################################################################
# $Id: editfield.py,v 1.2 2002/04/06 12:00:00 slmm Exp $
###############################################################################################

import pygame
import pygame.display
import pygame.surface
import pygame.key
from pygame.locals import *
from widget import Widget
import widget

class EditField(Widget):
    """
    This class defines a simple edit field where the user may input some text while the widget has
    focus. 
    """

    # static images for the frame around the editable text
    frameicons = {}

    # names for the icons
    frameiconnames = [ 'topleft', 'top', 'topright', 'right', 'botright', 'bot', 'botleft', 'left' ]

    
    def __init__ (self, font, text="", width=100, position = (0,0), cursor = None, frameicons = None, callbacks = None,
    	color = (255,255,255), background = (0,0,0)):		      
        """Initializes the widget. Renders the font using the passed data."""

        # firts call superclass constructor
        Widget.__init__ (self, position, callbacks)

        # store the text
        if text == None:
            self.text = ""
        else:
            self.text = text

        # store the cursor position
        self.cursor = len ( self.text )

        # store all needed data so that we can create new surfaces later
        self.font = font
        self.color = color
        self.background = background
        self.width = width
	self.cursor_image = cursor
       	EditField.frameicons = frameicons

       
        # render the text
        self.textrendered = font.render ( text, 1, color )
        
        # create the background surface to fit the rendered text's height
        self.textsurface = pygame.Surface ( ( width, self.textrendered.get_height () + 3),
                                            HWSURFACE ).convert ()

        # fill with the proper background color 
        self.textsurface.fill ( background ) 

         # create the surface with the border in it
        self.createBorder ()
        
        # set our internal callbacks so that we can trap keys
        self.internal = {widget.KEYDOWN : self.keyDown }


    def setText (self, text):
        """Sets a new text to be rendered."""
        # store new text
        if text == None:
            self.text = ""
        else:
            self.text = text

        # render a new surface
        self.textrendered = self.font.render ( self.text, 1, self.color )



    def getText (self):
        """Returns the text of the editfield. The text is never None, but may be empty if the
        editfield was cleared."""
        return self.text


    
    def paint (self, destination, force=0):
        """Method that paints the editfield. This method will simply blit out the surface of the widget
        onto the destination surface. """
        # are we dirty or not?
        if not self.dirty and not force:
            # not dirty, nothing to do here
            return 0

        # we're dirty, blit out the frame first
        destination.blit ( self.surface, (self.position [0], self.position [1]) )
        
        # now the text background
        destination.blit ( self.textsurface, (self.position [0] + self.deltax, self.position [1] + self.deltay) )

        # and the text if we have any
        if self.textrendered:
            # yep, we have it, get the width we should use
            if self.width < self.textrendered.get_size ()[0] + 3:
                width = self.width - 3
            else:
                width = self.textrendered.get_size ()[0]

            # now blit out the text
            destination.blit ( self.textrendered,
                               (self.position [0] + self.deltax + 3, self.position [1] + self.deltay+ 3) )
            
        self.dirty = 0
        

	# slm : render cursor
        if len(self.text):
                cursorx = self.font.size(self.text[0:self.cursor])[0]
                cursor_space = self.font.size(" ")[0] / 2

                destination.blit(self.cursor_image,
                        (
                                (self.position [0] + self.deltax)+(cursorx+cursor_space),
                                (self.position [1] + self.deltay+ 3)
                        )
                )

	
        # we did something, make sure the widget manager knows that
        return 1



    def keyDown (self,  event):
        """Callback triggered when the user presses a key inside the editfield. Gets the pressed key
        and modifies the internal string if needed. Renders a new surface too if needed. Some
        special keys are ignored."""

        # get the key and the unicode string
        key   = event.key
        value = event.unicode

        # a special key?
        if key == K_BACKSPACE:
	    if not len(self.text): return
            # remove one character
            self.text = self.text [0:self.cursor - 1] + self.text[self.cursor:]

            # update cursor position
            self.cursor -= 1

	    text = self.text
            # set the new surface
	    if len(self.text) == 0: text = ' '
            self.textrendered = self.font.render ( text, 1, self.color )

            # we're dirty now
            self.dirty = 1
            return

        elif key == K_DELETE:
            # remove one character from the right
            self.text = self.text [0:self.cursor] + self.text[self.cursor + 1:]
	    text = self.text
            # set the new surface
	    if len(self.text) == 0: text = ' '
            self.textrendered = self.font.render ( text, 1, self.color )
	    # we're dirty now
            self.dirty = 1
	    return

        elif key == K_TAB or key == K_RETURN:
            # dont do jack
            print "editfield.keyDown(): tab/return not handled"
            return

	# arrow handling
	elif key ==  K_LEFT:
	    self.cursor -= 1 
	    if self.cursor < 0: self.cursor = 0
	
	elif key ==  K_RIGHT:
	    self.cursor += 1
	    if self.cursor > len(self.text): self.cursor = len(self.text)
	    
	elif key == K_HOME:
	    self.cursor = 0
	
	elif key == K_END:
	    self.cursor = len(self.text)

	else:
	        # merge in the text
        	text = self.text [0:self.cursor] + value + self.text[self.cursor:]
		if self.font.render( text+" ", 1, self.color ).get_width() > self.width : return
        	self.text = text
	        # update cursor position
        	self.cursor += 1

        # do we still have any text left?
        if self.text == "":
            self.textrendered = None
            self.cursor = 0
        else:
            # set the new surface
            self.textrendered = self.font.render ( self.text, 1, self.color )

        # we're dirty now
        self.dirty = 1


    def createBorder (self):
        """Creates the border for the widget. Uses the 8 static icons and creates a surface that is
        slightly larger than the text surface (self.textsurface). This method is one ugly thing of
        coordinates and offsets. Don't touch unless you know what you do."""
        # get the delta values. These are used so that we know where to paint the text surface
        self.deltax = EditField.frameicons ['left'].get_width()
        self.deltay = EditField.frameicons ['top'].get_height()
        
        # get height and width of new surface
        size   = self.textsurface.get_size ()
        width  = size[0] + self.deltax + EditField.frameicons ['right'].get_width()
        height = size[1] + self.deltay + EditField.frameicons ['bot'].get_height()

        # create the needed surface
        self.surface = pygame.Surface ( (width, height), HWSURFACE ).convert ()

        # now some gory details. We need to blit stuff onto our frame surface to create the actual
        # frame. We first blit out the borders and the the corners. the corners then overpaint the
        # borders at proper positions
        top      = EditField.frameicons ['top']
        bot      = EditField.frameicons ['bot']
        left     = EditField.frameicons ['left']
        right    = EditField.frameicons ['right']
        topleft  = EditField.frameicons ['topleft']
        topright = EditField.frameicons ['topright']
        botleft  = EditField.frameicons ['botleft']
        botright = EditField.frameicons ['botright']

        # top/bottom borders
        x = 0
        while x < width:
            # what width should be used?
            if x + top.get_size ()[0] < width:
                # full width of icon
                widthx = top.get_size ()[0]
            else:
                # use only the missing part
                widthx = width - x

            # blit it all out
            self.surface.blit ( top, ( x, 0))
            self.surface.blit ( bot, ( x, height - bot.get_height () + 1 ) )
            x += widthx
        
        # left/right borders
        y = 0
        while y < height:
            # what height should be used?
            if y + left.get_size ()[1] < height:
                # full height of icon
                heighty = left.get_size ()[1]
            else:
                # use only the missing part
                heighty = height - y

            # blit it all out
            self.surface.blit ( left, ( 0, y ))
            self.surface.blit ( right, ( width - right.get_size ()[0], y ))
            y += heighty
        

        # top left corner
        self.surface.blit ( topleft, ( 0, 0 ))

        # top right corner
        self.surface.blit ( topright, ( width -  topright.get_width (), 0 ))

        # bottom left corner
        self.surface.blit ( botleft, ( 0, height - botleft.get_height () ))

        # bottom right corner
        self.surface.blit ( botright, ( width -  botright.get_width(), height - botright.get_height()))

#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
