###############################################################################################
# $Id: new_game.py,v 1.1.1.1 2002/02/19 10:16:10 slmm Exp $
###############################################################################################

import scenario
import properties
import sys
import organization
import widget
from button import Button
from label import Label
from widget_manager import WidgetManager
from dialog import *
from select_scenario import SelectScenario
from checkbox        import CheckBox
#from setup_players   import SetupPlayers


class NewGame(Dialog):
    """
    This class is used as a dialog for setting up parameters for a new game.
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

        # flags used for showing the "Ok" button. The two first ones should be set for the button to
        # be shown, and the third is then set
        self.scenario_ok = 0
        self.ok_shown = 0

        # no scenario data yet
        self.lines = None
        

    def createWidgets (self):
        "Creates all widgets for the dialog."

        # labels
        self.wm.register ( Label (self.titlefont, "Start a new game", (10, 10), color=(255, 0, 0)))
        self.wm.register ( Label (self.smallfont, "Scenario:",        (50, 180), color=(255, 255, 255)))
        self.wm.register ( Label (self.smallfont, "Play as: ",        (50, 220), color=(255, 255, 255)) )

        # create the changeable labels
        self.scenariolabel = Label (self.smallfont, "no scenario selected", (200, 180), color=(255, 255, 0))
        #self.sidelabel     = Label (self.smallfont, "not yet set", (200, 210), color=(255, 255, 0))

       # checkboxes
        self.union = CheckBox ( "Union", self.smallfont,
                                properties.path_dialogs + "butt-radio-set.png",
                                properties.path_dialogs + "butt-radio-unset.png",
                                checked=1, position=(180, 210), color=(255,255,0),
                                callbacks={widget.MOUSEBUTTONUP : self.togglePlayer } )
        self.rebel = CheckBox ( "Rebel", self.smallfont,
                                properties.path_dialogs + "butt-radio-set.png",
                                properties.path_dialogs + "butt-radio-unset.png",
                                checked=0, position=(280, 210), color=(255,255,0),
                                callbacks={widget.MOUSEBUTTONUP : self.togglePlayer } )

        # buttons. We show only the 'Cancel' button here, as the 'Ok' button is shown when all is
        # setup properly
        self.wm.register ( Button ( properties.path_dialogs + "butt-scenario-moff.png",
                                    properties.path_dialogs + "butt-scenario-mover.png",
                                    (162, 650 ), {widget.MOUSEBUTTONUP : self.selectScenario } ) )
        self.wm.register ( Button ( properties.path_dialogs + "butt-cancel-moff.png",
                                    properties.path_dialogs + "butt-cancel-mover.png",
                                    (650, 650 ), {widget.MOUSEBUTTONUP : self.cancel } ) )

        # register the labels and checkboxesfor management
        self.wm.register ( self.scenariolabel )
        self.wm.register ( self.rebel ) 
        self.wm.register ( self.union )
 

    def selectScenario (self, widget, event):
        """Callback triggered when the user clicks the 'Select scenario' button. """

        # create the dialog for selecting the scenario
        dialog = SelectScenario ()
        state = dialog.run ()

        # was the dialog rejected?
        if state == REJECTED:
            # no scenario yet. We leave the 'scenario_ok' flag as it is, as it may have been set
            # earlier to a good value.
            self.scenariolabel.setText ( "no scenario selected" )

        else:
            # get the name and location
            name     = scenario.info.getName ()
            location = scenario.info.getLocation ()

            # as well as the raw data
            self.lines = dialog.getChosenScenario ()
            
            # get the date and create a string
            (year, month, day, hour, minute) = scenario.info.getDate ()
            date = `year` + "." + `month` + "." + `day` + " " + `hour` + ":" + `minute`
            
            # create a label and set it
            self.scenariolabel.setText ( name + ", " + location + ", " + date )
            
            # we now have a valid scenario
            self.scenario_ok = 1
 
        # check wether the 'Ok' button should be shown
        self.checkShowOkButton ()
            
        # repaint the stuff if needed
        self.wm.paint (force=1, clear=1)


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


    def checkShowOkButton (self):
        """This button checks wether the 'Ok' button should be shown. If both the 'players' and
        'scenario' dialogs have been accepted and are ok this method shows the 'Ok' button. It is
        only shown once."""
        # do we already have a button and are the flags ok?
        if not self.ok_shown and self.scenario_ok:
            # all is ok, show the button
            self.wm.register ( Button ( properties.path_dialogs + "butt-ok-moff.png",
                                        properties.path_dialogs + "butt-ok-mover.png", (406, 650 ),
                                        {widget.MOUSEBUTTONUP : self.ok } ) )

            # now we have shown the button
            self.ok_shown = 1
            
        
    def ok (self, triggered, event):
        """Callback triggered when the user clicks the 'Ok' button. Closes the dialog and returns to
        the main dialog. Performs some general scenario setup."""

        # perform general scenario etup
        self.setupScenario ()

        # we're accepting the dialog
        self.state = ACCEPTED

        return widget.DONE


    def cancel (self, trigger, event):
        """Callback triggered when the user clicks the 'Cancel' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes."""
        # we're cancelling the dialog
        self.state = REJECTED
        
        return widget.DONE


    def setupScenario (self):
        """Performs various scenario setup. When this method is called the scenario is already
        loaded and the players have been set up. Currently does:
        * set visibility of units
        * store id of local player. TODO: use the Player class!
        """

        # store the passed data, first the side we have
        if self.rebel.isChecked ():
           # we're playing as rebel 
           scenario.local_player_id = organization.REBEL
        else:
           # we're playing as union 
           scenario.local_player_id = organization.UNION


        # get all the units
        units = scenario.units

        # loop over all units
        for unit in units.values ():
            # set proper visibility on the unit.
            unit.calcView()


    def getChosenScenario (self):
        """Returns the data for the chosen scenario. The data is returned as a list of string. If no
        scenario had been chosen None is returned."""

        return self.lines
    

#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
