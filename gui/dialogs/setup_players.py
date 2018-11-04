###############################################################################################
# $Id: setup_players.py,v 1.1.1.1 2002/02/19 10:16:06 slmm Exp $
###############################################################################################

import os
import getpass
import re
import organization
import scenario
import scenario_parser
import properties
import widget
from dialog import *
from button import Button
from checkbox import CheckBox
from label import Label
from editfield import EditField
from widget_manager import WidgetManager

# return codes used to indicate what should happen
CANCEL = 0
OK     = 1

class SetupPlayers(Dialog):
    """
    This class is used as a dialog for setting up the players for the game. This information
    includes the side the local player will play as (rebel/union), the network information of the
    remote server (hostname) as well as which machine acts as a server. By default the rebel machine
    is the server.
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
        self.wm.register ( Label (self.titlefont, "Setup player information", (10, 10), color=(255, 0, 0)))

        self.wm.register ( Label (self.smallfont, "My name: ",       (50, 190), color=(255, 255, 255)) )
        self.wm.register ( Label (self.smallfont, "Remote host: ",   (50, 250), color=(255, 255, 255)) )
        self.wm.register ( Label (self.smallfont, "Play as: ",       (50, 300), color=(255, 255, 255)) )
        self.wm.register ( Label (self.smallfont, "Act as server: ", (50, 340), color=(255, 255, 255)))


        # the editfields
        self.username = EditField ( self.smallfont, "chakie", 200, (200, 180), color=(255,255,0),
                                    background = (80,80,80))
        self.hostname = EditField ( self.smallfont, "localhost", 200, (200, 240), color=(255,255,0),
                                    background = (80,80,80))
        self.wm.register ( self.username )
        self.wm.register ( self.hostname )

        # buttons
        self.wm.register ( Button ( properties.path_dialogs + "butt-ok-moff.png",
                                    properties.path_dialogs + "butt-ok-mover.png",
                                    (284, 650 ), {widget.MOUSEBUTTONUP : self.ok } ) )
        self.wm.register ( Button ( properties.path_dialogs + "butt-cancel-moff.png",
                                    properties.path_dialogs + "butt-cancel-mover.png",
                                    (528, 650 ), {widget.MOUSEBUTTONUP : self.cancel } ) )

        # checkboxes
        self.union = CheckBox ( "Union", self.smallfont,
                                properties.path_dialogs + "butt-radio-set.png",
                                properties.path_dialogs + "butt-radio-unset.png",
                                checked=1, position=(200, 300), color=(255,255,0),
                                callbacks={widget.MOUSEBUTTONUP : self.togglePlayer } )
        self.rebel = CheckBox ( "Rebel", self.smallfont,
                                properties.path_dialogs + "butt-radio-set.png",
                                properties.path_dialogs + "butt-radio-unset.png",
                                checked=0, position=(300, 300), color=(255,255,0),
                                callbacks={widget.MOUSEBUTTONUP : self.togglePlayer } )
        self.server = CheckBox ( "Server", self.smallfont,
                                 properties.path_dialogs + "butt-radio-set.png",
                                 properties.path_dialogs + "butt-radio-unset.png",
                                 checked=1, position=(200, 340), color=(255,255,0),
                                 callbacks={widget.MOUSEBUTTONUP : self.toggleServer } )
        self.client = CheckBox ( "Client", self.smallfont,
                                 properties.path_dialogs + "butt-radio-set.png",
                                 properties.path_dialogs + "butt-radio-unset.png",
                                 checked=0, position=(300, 340), color=(255,255,0),
                                 callbacks={widget.MOUSEBUTTONUP : self.toggleServer } )

        self.wm.register ( self.rebel ) 
        self.wm.register ( self.union )
        self.wm.register ( self.server ) 
        self.wm.register ( self.client )



    def togglePlayer (self, trigger, event):
        """Callback triggered when one of the checkboxes are clicked. This method makes sure the
        other checkboxes are unchecked."""
        # who triggered the event?
        if trigger == self.union:
            # disable the other button
            self.rebel.setChecked ( 0 )

        else:
            # disable the other button
            self.union.setChecked ( 0 )

        # force a repaint as checkboxes leave stuff behind
        self.wm.paint(1)
            

    def toggleServer (self, trigger, event):
        """Callback triggered when one of the client/server checkboxes are clicked. This method
        makes sure the  other checkboxes are unchecked."""
        # who triggered the event?
        if trigger == self.server:
            # disable the other button
            self.client.setChecked ( 0 )

        else:
            # disable the other button
            self.server.setChecked ( 0 )

        # force a repaint as checkboxes leave stuff behind
        self.wm.paint(1)
            
    
    def ok (self, trigger, event):
        """Callback triggered when the user clicks the 'Ok' button. Applies the changes after
        verifying the given data, and closes the dialog."""
        # store the passed data, first the side we have
        if self.rebel.isChecked ():
           # we're playing as rebel 
           scenario.local_player_id = organization.REBEL
        else:
           # we're playing as union 
           scenario.local_player_id = organization.UNION

        # are we a server?
        if self.server.isChecked ():
           # we're the server
           scenario.act_as_server = 1
        else:
           # we're the client
           scenario.act_as_server = 0

        # store our name, if we got anything
        if self.username.getText () == "":
            # nothing there, use the login name
            scenario.local_player_name = getpass.getuser ()
        else:
            scenario.local_player_name = self.username.getText ()

        # did we get a hostname?
        if self.hostname.getText () == "":
            # oops, no host given
            print "No host given"
            return widget.HANDLED

        # store the name of the rmeote host
        scenario.remote_host = self.hostname.getText ()
        
        # is the host valid?
#        if self.checkHost ( self.hostname.getText () ):
#            # all is ok
#            scenario.remote_host = self.hostname.getText ()
#        else:
#            print "Could not reach remote host"
#            return widget.HANDLED
#        
        # we're accepting the dialog
        self.state = ACCEPTED
        
        return widget.DONE


    def checkHost (self, hostname):
        """Verifies that the given host can be reached by running ping against it. This is really
        crude and should be changed later. But we can't connect yet, so we just verify that the host
        exists at all. This does of course not guarantee that the host is the correct one. Returns 1
        on success and 0 on failure."""

        # define the regexp
        pingRegex = r'.*(?P<trans>\d+)\s+packets transmitted.*\s+' + \
                    r'(?P<recv>\d+)\s+packets received.*\s+' + \
                    r'(?P<loss>\d+)% packet loss'

        # run the external ping
        ping = os.popen ('ping -c 2 -i 1 ' + hostname + ' 2>&1')
        data = ping.read ()

        # does what we got match the expression
        match = re.match (pingRegex, data, re.DOTALL)
        if match:
            # do we have any lost packets?
            if match.group('loss') != '0':
                print "Ping failure: " 
                return 0

        else:
            # did not match regexp
            print "Ping error "
            return 0

        # all is ok as we got this far
        return 1
    
                
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
