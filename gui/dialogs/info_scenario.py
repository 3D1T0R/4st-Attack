###############################################################################################
# $Id: info_scenario.py,v 1.1.1.1 2002/02/19 10:16:03 slmm Exp $
###############################################################################################

import pygame
import pygame.image
from pygame.locals import *
import scenario
import properties
import string
import widget
from dialog import *
from button import Button
from label import Label
#from info_map import InfoMap
from widget_manager import WidgetManager

class InfoScenario (Dialog):
    """
    This class is used as a dialog for showing information about the scenario. It shows the
    background information about the selected scenario. 
    """

    def __init__ (self, info):
        """Creates the dialog. The passed 'info' is a ScenarioInfo about which the data should
        be displayed."""
        
        # load the fonts too
        self.titlefont = pygame.font.Font  ( properties.titlefont, 24 )
        self.smallfont = pygame.font.Font  ( properties.textfont, 14 )

        # store the info
        self.info = info
 
        # init superclass
        Dialog.__init__ (self, scenario.sdl)

        #self.description =
        self.createDescription ( self.smallfont, color=(255, 255, 255) )

        # set our background to a tiled image
        self.setBackground ( properties.window_background )


    def createDescription (self, font, color):
        """Creates the description labels. The description may be one or more lines of free text,
        and it needs to be created into a series of labels that can be blitted out. This method
        tries to separate the text into as large lines as possible and create a list of labels."""

        # max width and starting x and y
        width = 770
        x = 200
        y = 200

        # number of lines so far
        count = 0

        # loop over all paragraphs in the description
        for para in self.info.getDescription ():
            # format the para to get rid of unwanted whitespace
            para = string.join ( para.split (), ' ' ) 
            
            # temporaries
            testline = ''
            
            # loop over all words in the paragraph
            for word in para.split ( ' ' ):
                # store the current full line
                okline = testline

                # merge a text we use to test the width with. Don't add a ' ' if we only have one word
                # so far
                if testline == '':
                    testline = word
                else:
                    testline =  testline + ' ' + word

                # get the size of the label as it would be when rendered
                sizex, sizey = font.size ( testline )
                
                # too wide?
                if sizex > width:
                    # yep, os use the last 'good' text that fits and render a label
                    label = Label (font, okline, (x, y + count * 20), color=color )
                    
                    # register it
                    self.wm.register ( label )

                    # start with a new full line that is the part that was 'too much'
                    testline = word

                    # one more label rendered
                    count += 1
        
            # still something in 'all' that has not made it into a full line? we add a last (short) line
            # with the extra text
            if testline != '':
                label = Label ( font, testline, (x, y + count * 20), color=color )
                
                # register it
                self.wm.register ( label )

                # one more label rendered, add some empty space too
                count += 2
                

    def createWidgets (self):
        "Creates all widgets for the dialog."
        # buttons
        self.wm.register ( Button ( properties.path_dialogs + "butt-ok-moff.png",
                                    properties.path_dialogs + "butt-ok-mover.png",
                                    (284, 650 ), {widget.MOUSEBUTTONUP : self.ok } ) )
        self.wm.register ( Button ( properties.path_dialogs + "butt-forward-moff.png",
                                    properties.path_dialogs + "butt-forward-mover.png",
                                    (528, 650 ), {widget.MOUSEBUTTONUP : self.nextScreen } ) )

        # get the date and create a string
        (year, month, day, hour, minute) = self.info.getDate ()
        date = `year` + "." + `month` + "." + `day` + " " + `hour` + ":" + `minute`
        
        # labels
        self.wm.register ( Label (self.titlefont, "Scenario information", (10, 10), color=(255, 0, 0)))
        self.wm.register ( Label (self.smallfont, "Name: ", (50, 80), color=(255, 255, 0) ))
        self.wm.register ( Label (self.smallfont, "Date: ", (50, 110), color=(255, 255, 0) ))
        self.wm.register ( Label (self.smallfont, date, (200,110), color=(255, 255, 255)) )
        self.wm.register ( Label (self.smallfont, self.info.getName (), (200, 80),
                                  color=(255, 255, 255)) )
        self.wm.register ( Label (self.smallfont, "Location: ", (50, 140),
                                  color=(255, 255, 0) ))
        self.wm.register ( Label (self.smallfont, self.info.getLocation (), (200,140),
                                  color=(255,255,255)) )
        self.wm.register ( Label (self.smallfont, "Turns: ", (50, 170),  (0,0,0),
                                  color=(255, 255, 0) ))
        self.wm.register ( Label (self.smallfont, str(self.info.getMaxTurns ()), (200, 170),
                                  color=(255, 255, 255) ))
        self.wm.register ( Label (self.smallfont, "Description:", (50, 200), color=(255, 255, 0)))



    def ok (self, trigger, event):
        """Callback triggered when the user clicks the 'Ok' button. Simply closes the dialog."""
        # we're cancelling the dialog
        self.state = ACCEPTED

        return widget.DONE

      
    def nextScreen (self, triggered, event):
        """Callback triggered when the user clicks the 'Next' button. Shows the map info
        dialog. After the dialog has been shown this dialog is repainted."""

        print "nextScreen"
        # run the dialog
#        InfoMap ().run ()
        
        # repaint the stuff if needed
        self.wm.paint (force=1, clear=1)


#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
