###############################################################################################
# $Id: setup_network.py,v 1.1.1.1 2002/02/19 10:16:02 slmm Exp $
###############################################################################################

import pygame
import pygame.display
import pygame.surface
import os
import getpass
import traceback
import re
import scenario
import scenario_parser
import properties
from socket         import *
from net.connection import Connection
import gui.widget
from gui.image          import Image
from gui.dialog         import *
from gui.button         import Button
from gui.checkbox       import CheckBox
from gui.label          import Label
from gui.editfield      import EditField
from gui.widget_manager import WidgetManager
from gui.messagebox     import Messagebox
from gui.wait_client    import WaitClient

# return codes used to indicate what should happen
CANCEL = 0
OK     = 1

class SetupNetwork(Dialog):
    """
    This class is used as a dialog for setting up the connection to the game server. It asks for the
    user name (whatever name) and the name and port of the host where the server runs. The network
    connection is then initialized if all is ok.
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
       

    def createWidgets (self):
        """Creates all widgets for the dialog. Depending on wether we're a server or a client
        different widgets will be shown."""

        # are we a server?
        if not scenario.run_as_server:
            # we're running as client. need an additional label and editfield for the hostname
            self.wm.register ( Label (self.smallfont, "Server host: ",   (250, 240), color=(255, 255, 255)) )

            self.host = EditField ( self.smallfont, "localhost", 200, (450, 240), color=(255,255,0),
                                    background = (80,80,80))

            self.wm.register ( self.host )

        # common widgets
        self.wm.register ( Label (self.titlefont, "Setup network information", (10, 10), color=(255, 0, 0)))

        self.wm.register ( Label (self.smallfont, "Server port: ",   (250, 300), color=(255, 255, 255)) )
        self.port = EditField ( self.smallfont, str(properties.network_port), 200, (450, 300),
                                color=(255,255,0), background = (80,80,80))

        self.wm.register ( self.port )
           
        # buttons
        self.wm.register ( Button ( properties.path_dialogs + "butt-ok-moff.png",
                                    properties.path_dialogs + "butt-ok-mover.png",
                                    (284, 650 ), {widget.MOUSEBUTTONUP : self.ok } ) )
        self.wm.register ( Button ( properties.path_dialogs + "butt-back-moff.png",
                                    properties.path_dialogs + "butt-back-mover.png",
                                    (528, 650 ), {widget.MOUSEBUTTONUP : self.back } ) )

    
    def ok (self, trigger, event):
        """Callback triggered when the user clicks the 'Ok' button. Applies the changes after
        verifying the given data, and closes the dialog. Tries to connect to the remote server or
        waits for a remote client to connect to us, and if all is ok the dialog is accepted. If
        something fails the player may choose again. If some data is missing the player must choose
        again"""

        # get the port. this is common for both client and server
        try:
            port = int ( self.port.getText () )

            # is it valid?
            if not 1 <= port <= 65535:
                # not a valid number, show a messagebox
                Messagebox ( "Invalid port number, must be in the range 1 to 65535!" )

                # repaint and go away
                self.wm.paint (force=1, clear=1)
                return widget.HANDLED
            
        except TypeError:
            # not a valid number, show a messagebox
            Messagebox ( "Invalid port number!" )

            # repaint and go away
            self.wm.paint (force=1, clear=1)
            return widget.HANDLED


        # are we a server?
        if scenario.run_as_server:
            # init serverside socket
            return self.initServerSocket ( port )

        else:
            # init clientside socket
            return self.initClientSocket ( port )


    def initServerSocket (self, port):
        """ """
        try:
            # create the socket
            s = socket (AF_INET, SOCK_STREAM)
            
            # allow bind()ing while a previous socket is still in TIME_WAIT.
            s.setsockopt ( SOL_SOCKET, SO_REUSEADDR, 1 )
            
            # bind our socket for incoming requests
            s.bind ( ( 'localhost', port ) )
        except:
            # not a valid number, show a messagebox
            Messagebox ( "Could not use socket! It may already be in use." )

            # repaint and go away
            self.wm.paint (force=1, clear=1)
            return widget.HANDLED

        # listen for clients
        s.listen ( 1 )

        # run a dialog that shows some nice info while we wait for the client to connect
        dialog = WaitClient ( s )
        dialog.run ()

        # set our status to the status of the executed dialog
        self.state = dialog.state

        # we're done anyway
        return widget.DONE


    def initClientSocket (self, port):
        """Connects to the server. If all is ok a connection is stored in the scenario. On error a
        dialog is shown to the user and the user may try again."""
        
        # get the name of the host
        host = self.host.getText ()

        # did we get a hostname?
        if host == "":
            # oops, no host given, show a messagebox
            Messagebox ( "No server hostname given!" )

            # repaint and go away
            self.wm.paint (force=1, clear=1)
            return widget.HANDLED

        try:
            # create the socket
            newSocket = socket (AF_INET, SOCK_STREAM)
        
            # connect to the remote system
            newSocket.connect ( ( host, port  ) )

            # all ok, store the new and connected socket and the extra info
            scenario.connection = Connection ( socket=newSocket, host=host, port=port )

        except:
            Messagebox ( "Could not connect to server!" )

            # repaint and go away
            self.wm.paint (force=1, clear=1)

            return widget.HANDLED
       
        # all is ok, we're accepting the dialog
        self.state = ACCEPTED
        
        return widget.DONE

               
    def back (self, trigger, event):
        """Callback triggered when the user clicks the 'Back' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes. This is used when the player wants to
        change something."""
        # we're cancelling the dialog
        self.state = REJECTED
        
        return widget.DONE



#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
