###############################################################################################
# $Id: start_game.py,v 1.1.1.1 2002/02/19 10:16:04 slmm Exp $
###############################################################################################

import pygame
from pygame.locals import *
import scenario
import properties
import traceback
import sys
import string
import widget
from button          import Button
from label           import Label
from image           import Image
from widget_manager  import WidgetManager
from dialog          import *
from messagebox      import Messagebox
from scenario_parser import ScenarioParser

class StartGame(Dialog):
    """
    This class is used as a dialog for showing some information to the player while the game sets up
    the network connection and receives the scenario information. Shows a centered splash screen
    with a label of information on it.
    """

    def __init__ (self):
        "Creates the dialog."
        # load the fonts too
        self.titlefont = pygame.font.Font  ( properties.titlefont, 24 )
        self.smallfont = pygame.font.Font  ( properties.textfont, 14 )
        
        # init superclass
        Dialog.__init__ (self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground ( properties.window_background )

        # load the images for the progress bar
        #self.progressimages = []
        #for image in (properties.progress_bar_start, properties.progress_bar_mid, properties.progress_bar_end):
            

        # no error yet
        self.error = ()

        # no lines to read yet
        self.linecount = -1

        # neither scenario data not config data read
        self.configread = 0
        self.scenarioread = 0
        
        # no scenario data yet
        self.buffer = ''
        
        # we want timer events
        self.enableTimer ( 300 )
        

    def createWidgets (self):
        "Creates all widgets for the dialog."

        # create a message
        message = "Waiting for other player to perform setup..."
            
        # create the splash
        self.splash = Image ( properties.dialog_splash, (272, 204) )
        self.wm.register ( self.splash )
 
        # the status label
        self.statuslabel = Label (self.smallfont, message, (340, 213), color=(255, 255, 255))
        self.wm.register ( self.statuslabel )

        # create the cancel button
        self.wm.register ( Button ( properties.path_dialogs + "butt-cancel-moff.png",
                                    properties.path_dialogs + "butt-cancel-mover.png",
                                    (406, 650), {widget.MOUSEBUTTONUP : self.cancel } ) )



    def timer (self):
        """Callback triggered when the dialog has enabled timers and a timer fires. First tries to
        read the configuration from the connection, and if that succeeds further calls will read the
        raw scenario data. If all succeeds the dialog is accepted."""

        # do we have lines to read, i.e. have we started to receive the scenario?
        if not self.configread:
            # read scenario config
            return self.readConfig ()

        elif not self.scenarioread:
            # read the scenario data instead
            return self.readScenario ()

        # we're cancelling the dialog
        self.state = ACCEPTED
        return widget.DONE


    def readConfig (self):
        """Reads the configuration data from the network connection. If all is ok sets the flag that
        indicates that the configuration is now read."""
        
        # wait for the server to send a status
        status = scenario.connection.readLine ( timeout = 0.01 )

        # did we get a status
        if not status:
            # nothing was read, go on
            return

        # split up the received message into components
        parts = status.split ()

        # precautions. we need at least 4 parts: "start id lines name"
        if len ( parts ) < 4 or parts[0] != 'start':
            # oops, bad data
            Messagebox ( "Bad data received from server!" )

            # repaint and go away
            self.wm.paint (force=1, clear=1)
 
            # we're cancelling the dialog
            self.state = REJECTED
        
            return widget.DONE

        # get all data from the read parts
        scenario.local_player_id = int ( parts[1] )
        scenario.remote_player_name = string.join ( parts [3:] )

        # also the number of lines in the scenario we're about to read
        self.linecount = int ( parts[2] )

        # configuration is now read
        self.configread = 1

        return widget.HANDLED

        
    def readScenario (self):
        """Retrieves a scenario from the server. Sends the id of the scenario to the server and
        reads the XML data the server sends back."""

        # optimize away a dot
        connection = scenario.connection
        
        try:
            lastratio = 0
            xpos = 352
            ypos = 461
            
            # create initial progress icon, the leftmost
##             progress = Image ( properties.progress_bar_start, ( 100, 200 ) )
##             self.wm.register ( progress )

            # let the player know what we do
            self.statuslabel.setText ( 'Downloading scenario...' )
            
            # we must repaint so that the label is shown
            self.wm.paint ( clear=1, force=1 )

            # loop and read the lines
            for index in range ( self.linecount ):
                # read a line
                line = connection.readLine ( timeout = 5 )

                # did we get a line?
                if not line:
                    continue
                
                # add to the internal list
                self.buffer += line

                # get a ratio [0..9] of the progress
                ratio = int ( float (index) / self.linecount * 33.0 )

                # have we advanced another 10%?
                if ratio > lastratio:
                    # yep, let the user feel the update
                    lastratio = ratio

                    # create a new part of the progress bar
                    progress = Image ( filename=properties.progress_bar_mid, position=(xpos, ypos))
                    self.wm.register ( progress )

                    # go onwards
                    xpos += 10
                    
                    # we must repaint the entire dialog
                    self.wm.paint ( clear=0, force=0 )

            # let the player know what we do
            self.statuslabel.setText ( 'Building scenario...' )
            
            # we must repaint so that the label is shown
            self.wm.paint ( clear=1, force=1 )

            # parse the read data
            ScenarioParser ().parseString ( self.buffer )

            # scenario is read now
            self.scenarioread = 1
           
            # we're done with the dialog
            return widget.HANDLED
        
        except:
            raise
            # serious error
            Messagebox ( "Could not read scenario!" )
            
            # repaint and go away
            self.wm.paint (force=1, clear=1)
 
            # we're cancelling the dialog
            self.state = REJECTED
            return widget.DONE


    def cancel (self, trigger, event):
        """Callback triggered when the user clicks the 'Cancel' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes."""

        # we're cancelling the dialog
        self.state = REJECTED
        
        return widget.DONE



#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
