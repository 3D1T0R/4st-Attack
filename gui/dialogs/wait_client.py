###############################################################################################
# $Id: wait_client.py,v 1.1.1.1 2002/02/19 10:16:04 slmm Exp $
###############################################################################################

import pygame
from pygame.locals import *
import scenario
import properties
import traceback
import sys
import string
import widget
from net.connection  import Connection
from select          import select
from button          import Button
from label           import Label
from image           import Image
from widget_manager  import WidgetManager
from dialog          import *
from messagebox      import Messagebox
from scenario_parser import ScenarioParser

class WaitClient(Dialog):
    """
    This class is used as a dialog for showing 
    """

    def __init__ (self, sock):
        "Creates the dialog."
        # load the fonts too
        self.titlefont = pygame.font.Font  ( properties.titlefont, 24 )
        self.smallfont = pygame.font.Font  ( properties.textfont, 14 )

        # init superclass
        Dialog.__init__ (self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground ( properties.window_background )

        # store the socket
        self.socket = sock

        # we want timer events
        self.enableTimer ( 300 )
        

    def createWidgets (self):
        "Creates all widgets for the dialog."

        # create a message
        message = "Waiting for client to connect..."
 
        # the status label
        self.label = Label (self.smallfont, message, (340, 213), color=(255, 255, 255))
        self.wm.register ( self.label )

        # create the cancel button
        self.wm.register ( Button ( properties.path_dialogs + "butt-cancel-moff.png",
                                    properties.path_dialogs + "butt-cancel-mover.png",
                                    (406, 650), {widget.MOUSEBUTTONUP : self.cancel } ) )



    def timer (self):
        """Callback triggered when the dialog has enabled timers and a timer fires. First tries to
        read the configuration from the connection, and if that succeeds further calls will read the
        raw scenario data. If all succeeds the dialog is accepted."""

        # perform the select. We're only interested in incoming events. wait forever
        incoming, out, execptional = select ( [self.socket], [], [], 0.0 )

        # was there something on the incoming socket that we listen on?
        if self.socket in incoming:
            # yep, we need to accept the new client
 
            # wait and accept the new client
            newsock, addr = self.socket.accept ()

            # create and return the new sockets as connections
            scenario.connection = Connection ( socket=newsock, host="localhost" )

            # we're done the dialog
            self.state = ACCEPTED
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
