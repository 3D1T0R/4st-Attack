###############################################################################################
# $Id: info_map.py,v 1.1.1.1 2002/02/19 10:16:05 slmm Exp $
###############################################################################################

import pygame
import pygame.image
from pygame.locals import *
import scenario
import properties
import widget
from button import Button
from info_units import InfoUnits
from widget_manager import WidgetManager

class InfoMap:
    """
    This class is used as a dialog for.
    """

    def __init__ (self):
        "Creates the dialog."

        # create a new surface matching the display
        self.surface = sdl.surface_new ( (properties.window_size_x, properties.window_size_y), 1)
        self.surface = self.surface.convert ()
        
        # load the fonts too
        self.titlefont = pygame.font.Font  ( properties.titlefont, 24 )

        # create the static labels
        self.title = self.titlefont.render ( "Scenario map ", 1, (255, 0, 0) )

        # blit 'em
        self.surface.blit ( self.title, (10, 10 ))

        # get the map
        map = scenario.map
        
        # get the hexes of the map
        hexes = scenario.map.getHexes ()

        # create a new surface for it. It must contain the entire map (2x2 pixels per hex) and be a
        # little wider as every even row is adjusted half a hex to the right
        self.minimap = sdl.surface_new ( (map.getXsize () * 4 + 1, map.getYsize () * 3 + 1), 1 )
        
        # loop over the hexes in the map
        for y in range ( map.getYsize () ):
            for x in range ( map.getXsize () ):
                # get the hex for that position
                hex = hexes [x][y]

                # get the miniicon for the hex
                icon = hex.getMiniIcon ()
                
                # is this an odd or even row?
                if y % 2:
                    # odd
                    self.minimap.blit ( icon, (x * 4 + 2, y * 3 ))
                else:
                    # even
                    self.minimap.blit ( icon, (x * 4, y * 3 ))


        # calculate the x position for the map
        xpos = properties.window_size_x / 2 - ( self.minimap.get_size ()[0] / 2 )
        
        # blit out the created surface
        self.surface.blit ( self.minimap, (xpos, self.title.get_size()[1] + 40 ) )

        # create the widget manager
        self.wm = WidgetManager (self.surface)

        # create all widgets
        self.createWidgets ()
      
        # blit out or full surface to the main surface
        scenario.sdl.blit ( self.surface, (0, 0 ))

        # update the whole screen
        scenario.sdl.update ()
        #pygame.display.update ()



    def createWidgets (self):
        "Creates all widgets for the dialog."
        # create the buttons for the next and previous buttons
        self.wm.register ( Button ( properties.path_dialogs + "butt-back-moff.png",
                                    properties.path_dialogs + "butt-back-mover.png",
                                    (284, 650 ), {widget.MOUSEBUTTONUP : self.prevScreen } ) )
        self.wm.register ( Button ( properties.path_dialogs + "butt-forward-moff.png",
                                    properties.path_dialogs + "butt-forward-mover.png",
                                    (528, 650 ), {widget.MOUSEBUTTONUP : self.nextScreen } ) )


    def run (self):
        """Executes the dialog and runs its internal loop until a key is pressed. When that happens
        shows the dialog InfoUnits. When that dialog is terminated this method also returns."""

        # loop forever
        while 1:
            # get next event
            event = pygame.event.wait ()

            # see wether the widget manager wants to handle it
            if event != -1:
                # handle event and get the return code that tells us wehter it was handled or not
                returncode = self.wm.handle ( event )

                # is the event loop done?
                if returncode == widget.DONE:
                    return


    def nextScreen (self, event):
        """Callback triggered when the user clicks the 'Next' button. Shows the 'Order of battle'
        dialog. After the dialog has been shown this dialog is repainted."""

        # show the dialog
        InfoUnits ().run ()

        # blit out or full surface to the main surface
        scenario.sdl.blit ( self.surface, (0, 0 ))

        # update the whole screen
        scenario.sdl.update ()
        #pygame.display.update ()

        # we've handled the event
        return widget.HANDLED
    

    def prevScreen (self, event):
        """Callback triggered when the user clicks the 'Previous' button. This method simply cancels
        the event loop for this dialog's widget manager. Basically this dialog quits."""
        # we're done
        return widget.DONE
    

#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
