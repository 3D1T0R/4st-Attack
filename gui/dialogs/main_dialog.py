###############################################################################################
# $Id: main_dialog.py,v 1.1.1.1 2002/02/19 10:16:08 slmm Exp $
###############################################################################################

import pygame
import pygame.font
from pygame.locals import *
import scenario
import properties
from organization import REBEL, UNION, toString
import sys
import widget
from dialog          import *
from new_game        import NewGame
from button          import Button
from label           import Label
from info_scenario   import InfoScenario
from widget_manager  import WidgetManager
from start_game      import StartGame

class MainDialog(Dialog):
    """
    This class is used as the main dialog for the application. It is launched as the first graphical
    part of civil as soon as it starts. It presents the user with a basic dialog where some actions
    can be performed through clicking buttons:

    o start a new game with a new scenario
    o load a saved game (not yet implemented)
    o set options for the game
    o start the game
    o quit
    """

    def __init__ (self):
        "Creates the dialog."
        # load the fonts too
        self.titlefont = pygame.font.Font ( properties.titlefont, 24 )
        self.smallfont = pygame.font.Font ( properties.textfont, 14 )

        # init superclass
        Dialog.__init__ (self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground ( properties.window_background )


    def createWidgets (self):
        "Creates all widgets for the dialog."
        # labels
        self.wm.register ( Label (self.titlefont, "Welcome to Civil", (10,  10), color=(255, 0, 0)))
        self.wm.register ( Label (self.smallfont, "Scenario:",        (50, 180), color=(255, 255, 255)))
        self.wm.register ( Label (self.smallfont, "Play as: ",        (50, 210), color=(255, 255, 255)) )
        self.wm.register ( Label (self.smallfont, "Server name: ",    (50, 240), color=(255, 255, 255)) )
        self.wm.register ( Label (self.smallfont, "My name: ",        (50, 270), color=(255, 255, 255)))

        # create the changeable labels
        self.scenariolabel = Label (self.smallfont, "no scenario selected", (200, 180), color=(255, 255, 0))
        self.sidelabel     = Label (self.smallfont, "not yet set", (200, 210), color=(255, 255, 0))
        self.serverlabel   = Label (self.smallfont, scenario.connection.getHost (), (200, 240),
                                    color=(255, 255, 0))
        self.usernamelabel = Label (self.smallfont, scenario.local_player_name, (200, 270),
                                    color=(255, 255, 0))

        # register the labels for management
        self.wm.register ( self.serverlabel )
        self.wm.register ( self.scenariolabel )
        self.wm.register ( self.sidelabel )
        self.wm.register ( self.usernamelabel )

        # buttons
        self.wm.register ( Button ( properties.path_dialogs + "butt-new-game-moff.png",
                                    properties.path_dialogs + "butt-new-game-mover.png",
                                    (40, 650 ), {widget.MOUSEBUTTONUP : self.newGame } ) )
        self.wm.register ( Button ( properties.path_dialogs + "butt-loadgame-moff.png",
                                    properties.path_dialogs + "butt-loadgame-mover.png",
                                    (282, 650 ), {widget.MOUSEBUTTONUP : self.loadGame } ) )
        self.wm.register ( Button ( properties.path_dialogs + "butt-quit-moff.png",
                                    properties.path_dialogs + "butt-quit-mover.png",
                                    (772, 650 ), {widget.MOUSEBUTTONUP : self.quit } ) )


    def newGame (self, trigger, event):
        """Callback triggered when the user clicks the 'New game' button. """
        # create a dialog and run it
        dialog = NewGame ()
        state = dialog.run ()

        # was it accepted or rejected?
        if state == ACCEPTED:
            # dialog was ok:ed, we should now activate the button that allows us to start the game
            self.wm.register ( Button ( properties.path_dialogs + "butt-startgame-moff.png",
                                        properties.path_dialogs + "butt-startgame-mover.png",
                                        (528, 650 ), {widget.MOUSEBUTTONUP : self.startGame } ) )

            # do we noe have some info about the scenario?
            if scenario.info:
                # yep, update the label, create the text for the label

                # get the name and location
                name     = scenario.info.getName ()
                location = scenario.info.getLocation ()

                # get the scenario data
                self.lines = dialog.getChosenScenario ()

                # get the date and create a string
                (year, month, day, hour, minute) = scenario.info.getDate ()
                date = `year` + "." + `month` + "." + `day` + " " + `hour` + ":" + `minute`

                # create a label of the data and set it
                self.scenariolabel.setText ( name + ", " + location + ", " + date )

                # yep, so we need to update our display too, first set the labels
                self.sidelabel.setText ( toString ( scenario.local_player_id ) )
        
        # repaint the stuff if needed
        self.wm.paint (force=1, clear=1)


    def loadGame (self, trigger, event):
        """Callback triggered when the user clicks the 'Load game' button. """
        print "loadGame: not yet implemented"

     
    def quit (self, trigger, event):
        """Callback triggered when the user clicks the 'Quit' button. Will send the command 'quit'
        to the server and the quit. """
        # send our resignation
        scenario.connection.send ( 'quit\n' )

        # just go away
        pygame.quit ()
        sys.exit ( 0 )


    def startGame (self, trigger, event):
        """Callback triggered when the user clicks the 'Start game' button."""

        print "MainDialog.startGame: sending scenario."

        scenario.connection.send ( 'start %d %d %s\n' % ( (UNION, REBEL)[ scenario.local_player_id],
                                                          len ( self.lines ), scenario.local_player_name ) )
       
        for line in self.lines:
            scenario.connection.send ( line )

        print "MainDialog.startGame: sent scenario."
        

        # create the dialog
##         dialog = StartGame ()

##         # attempt to start the game
##         if dialog.run () != ACCEPTED:
##             # failed to start the game, get the error code
##             #error = dialog.getError ()
            
##             print "Failed to start the game" # + error[1]

##             # repaint the stuff in our dialog
##             self.wm.paint (force=1, clear=1)
##             return

##         print "MainDialog.startGame: all ok, game starting"
        
##         # repaint the stuff if needed
##         self.wm.paint (force=1, clear=1)

        # we're accepting the dialog the dialog
        self.state = ACCEPTED
        
        return widget.DONE
       

#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
