###############################################################################################
# $Id: select_scenario.py,v 1.1.1.1 2002/02/19 10:16:04 slmm Exp $
###############################################################################################

import pygame
from pygame.locals import *
import os, string
import re, sys
import scenario
import properties
import widget
import urllib
from dialog import *
from button import Button
from label import Label
from image import Image
from widget_manager   import WidgetManager
from scenario_manager import ServerScenarioManager
from info_scenario    import InfoScenario
from scenario_parser  import ScenarioParser

class SelectScenario(Dialog):
    """
    This class is used as a dialog for selecting a scenario among the available scenarios. It
    displays all scenarios in a nice list.
    """

    def __init__ (self):
        "Creates the dialog."
        # load the fonts too
        self.titlefont = pygame.font.Font  ( properties.titlefont, 24 )
        self.smallfont = pygame.font.Font  ( properties.textfont, 12 )

        # define a map with the scenario names to the filenames
        self.namemap = { }
        self.info = None

        # no scenario data yet
        self.lines = None
        
        # init superclass
        Dialog.__init__ (self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground ( properties.window_background )
        
        # no selection widget yet, it is created later
        self.selection = None

 
    def createWidgets (self):
        "Creates all widgets for the dialog."
        # labels
        self.wm.register ( Label (self.titlefont, "Select a scenario", (10, 10), color=(255, 0, 0)))

        # start index for the labels
        x = 100
        y = 100
        
        # create a scenario manager if we don't already have one. This will read the scenarios from
        # the server
        if scenario.scenario_manager == None:
            scenario.scenario_manager = ServerScenarioManager ()
    
            # read in all scenario info:s
            scenario.scenario_manager.loadScenarioIndex ( properties.path_scenarios )

        # start from index 0
        index = 0
        
        # loop over all infos we got
        for info in scenario.scenario_manager.getScenarios ():
            # get the name and location
            name = info.getName ()
            location = info.getLocation ()

            # get the date and create a string
            (year, month, day, hour, minute) = info.getDate ()
            date = `year` + "." + `month` + "." + `day` + " " + `hour` + ":" + `minute`

            # create a label
            text = name + ", " + location + ", " + date

            # create a label
            label = Label (self.smallfont, text, (x, y), color=(255, 255, 255),
                           callbacks = {widget.MOUSEBUTTONUP : self.select } )

            # register it
            self.wm.register ( label )

            # make sure we know the filename from the label later
            self.namemap [text] = ( index, info )
           
            # increment the y-offset and index
            y += label.getHeight () + 5
            index += 1

        # buttons. We create only the Cancel button so far, the other are created later
        self.wm.register ( Button ( properties.path_dialogs + "butt-cancel-moff.png",
                                    properties.path_dialogs + "butt-cancel-mover.png",
                                    (650, 650 ), {widget.MOUSEBUTTONUP : self.cancel } ) )



    def select (self, trigger, event):
        """Callback triggered when the user clicks one of the scenario labels. Shows the yellow box
        that indicates the wanted scenario as well as the 'Ok' button (if not shown)."""

        # get the url and index of the clicked label
        (index, info) = self.namemap [trigger.getText ()]

        # store the current scenario info
        self.info = info
        
        # now we have a selected scenario, show 'Ok' button and the 'Info' button
        self.wm.register ( Button ( properties.path_dialogs + "butt-ok-moff.png",
                                    properties.path_dialogs + "butt-ok-mover.png",
                                    (406, 650 ), {widget.MOUSEBUTTONUP : self.ok } ) )

        self.wm.register ( Button ( properties.path_dialogs + "butt-info-moff.png",
                                    properties.path_dialogs + "butt-info-mover.png",
                                    (162, 650 ), {widget.MOUSEBUTTONUP : self.showInfo } ) )

        
        # set coordinates for the box
        x = 70
        y = index * 22 + 98

        # do we have a selection widget?
        if self.selection == None:
            # nope, create and register a new image for the selection box
            self.selection = Image ( properties.scenario_selection_icon, (x,y) )
            self.wm.register ( self.selection )

        else:
            # already there, just reposition it
            self.selection.setPosition ( ( x, y ) )

        # we must repaint the entire dialog to get the old box cleared out
        self.wm.paint ( clear=1, force=1 )
        
        # we've selected a scenario
        self.state = ACCEPTED

        # we're done here
        return widget.HANDLED

    
    def ok (self, trigger, event):
        """Callback triggered when the user clicks the 'Ok' button. Reads in a selected scenario."""

        # load the scenario
        self.lines = scenario.scenario_manager.loadScenario ( self.info.getId () )

        # did we get anything?
        if self.lines == None:
            # oops, bad data
            Messagebox ( "Could not load scenario '%s'!" % self.info.getName () )

            # repaint and go away
            self.wm.paint (force=1, clear=1)
 
            # we're cancelling the dialog
            self.state = REJECTED
            return widget.DONE
 
        # parse the read data after flattening it to a string
        ScenarioParser ().parseString ( string.join ( self.lines ) )

        # we're ok the dialog
        self.state = ACCEPTED
        return widget.DONE


    def cancel (self, trigger, event):
        """Callback triggered when the user clicks the 'Cancel' button. Simply closes the dialog and
        returns to the main dialog."""
        # we're cancelling the dialog
        self.state = REJECTED
        
        return widget.DONE
   

    def showInfo (self, trigger, event):
        """Callback triggered when the user clicks the 'Info' button. """

        # create a new dialog and run it
        InfoScenario ( self.info ).run ()
        
        # repaint the stuff if needed
        self.wm.paint (force=1, clear=1)

        return widget.HANDLED


    def getChosenScenario (self):
        """Returns the data for the chosen scenario. The data is returned as a list of string. If no
        scenario had been chosen None is returned."""

        return self.lines
    

#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
