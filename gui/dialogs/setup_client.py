###############################################################################################
# $Id: setup_client.py,v 1.1.1.1 2002/02/19 10:16:05 slmm Exp $
###############################################################################################

import pygame
import pygame.display
import pygame.surface
import os
import getpass
import traceback
import re
import scenario
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

# return codes used to indicate what should happen
CANCEL = 0
OK     = 1

class SetupClient(Dialog):
    """
    This class is used as a dialog for letting the player select wether to run as a client or a
    server. A name can also be given by the players. This is a human readable name that is used for
    the communication between the players. 
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
        "Creates all widgets for the dialog."
        # labels
        self.wm.register ( Label (self.titlefont, "Setup network information", (10, 10), color=(255, 0, 0)))

        self.wm.register ( Label (self.smallfont, "My name: ",       (250, 240), color=(255, 255, 255)) )
        self.wm.register ( Label (self.smallfont, "Run as server: ", (250, 300), color=(255, 255, 255)) )

        # get the user name from the environment if it works
        try:
            name = os.environ['USER']
        except:
            name = "My name"

        # the editfields
        self.user = EditField ( self.smallfont, name,    200, (450, 230), color=(255,255,0),
                                background = (80,80,80))

        self.server = CheckBox ( "Server", self.smallfont,
                                 properties.path_dialogs + "butt-radio-set.png",
                                 properties.path_dialogs + "butt-radio-unset.png",
                                 checked=1, position=(450, 290), color=(255,255,0),
                                 callbacks={widget.MOUSEBUTTONUP : self.toggleServer } )
        self.client = CheckBox ( "Client", self.smallfont,
                                 properties.path_dialogs + "butt-radio-set.png",
                                 properties.path_dialogs + "butt-radio-unset.png",
                                 checked=0, position=(570, 290), color=(255,255,0),
                                 callbacks={widget.MOUSEBUTTONUP : self.toggleServer } )

        self.wm.register ( self.user )
        self.wm.register ( self.server )
        self.wm.register ( self.client )

        # buttons
        self.wm.register ( Button ( properties.path_dialogs + "butt-ok-moff.png",
                                    properties.path_dialogs + "butt-ok-mover.png",
                                    (284, 650 ), {widget.MOUSEBUTTONUP : self.ok } ) )
        self.wm.register ( Button ( properties.path_dialogs + "butt-quit-moff.png",
                                    properties.path_dialogs + "butt-quit-mover.png",
                                    (528, 650 ), {widget.MOUSEBUTTONUP : self.cancel } ) )

    
    def ok (self, trigger, event):
        """Callback triggered when the user clicks the 'Ok' button. Applies the changes after
        verifying the given data, and closes the dialog. """
        
        # store our name, if we got anything
        if self.user.getText () == "":
            # nothing there, use the login name
            scenario.local_player_name = getpass.getuser ()
        else:
            scenario.local_player_name = self.user.getText ()
        
        # we're accepting the dialog
        self.state = ACCEPTED
        
        return widget.DONE

   
                
    def cancel (self, trigger, event):
        """Callback triggered when the user clicks the 'Cancel' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes."""
        # we're cancelling the dialog
        self.state = REJECTED
        
        return widget.DONE


    def toggleServer (self, trigger, event):
        """Callback triggered when one of the client/server checkboxes are clicked. This method
        makes sure the  other checkboxes are unchecked."""
        # who triggered the event?
        if trigger == self.server:
            # disable the other button
            self.client.setChecked ( 0 )

            # running as server
            scenario.run_as_server = 1
        else:
            # disable the other button
            self.server.setChecked ( 0 )

            # running as client
            scenario.run_as_server = 0

        # force a repaint as checkboxes leave stuff behind
        self.wm.paint(1)


#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
