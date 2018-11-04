###############################################################################################
# $Id: info_units.py,v 1.1.1.1 2002/02/19 10:16:10 slmm Exp $
###############################################################################################

import scenario
import properties
import organization
import widget
import unit
from button import Button
from label import Label
from widget_manager import WidgetManager

class InfoUnits:
    """
    This class is used as a dialog for showing the 'order of battle', i.e. which units participate
    in the battle from the rebel and union sides. The full organizations are shown along with all
    available stats for all units.
    """

    def __init__ (self):
        "Creates the dialog."

        # create a new surface matching the display
        self.surface = sdl.surface_new ( 0, properties.window_size_x, properties.window_size_y,
                                         properties.window_depth, (0,0,0,0) ).convert_display () 
        
        # load the fonts too
        self.titlefont = pygame.font.Font  ( properties.titlefont, 24 )
        self.smallfont = pygame.font.Font  ( properties.textfont, 16 )
        self.tinyfont  = pygame.font.Font  ( properties.tinyfont, 12 )


        # create the labels for the rebel and union units
#        rebellabels = self.createLabels ( organization.REBEL )
#        unionlabels = self.createLabels ( organization.UNION )

        # loop over all lables we got
#        for index in range ( len (rebellabels) ):
#            # get the current label
#            indent, labels = rebellabels[index]
#
#            # do we have one or more labels?
#            if len (labels) == 1:
#                # we have only one label, it is a highlevel organization of some kind. Get the label
#                label = labels [0]
#                
#                # blit the label
#                self.surface.blit ( label, (0, 0, label.get_width(), label.get_height()),
#                                    (50 + indent * 50, 100 + index * label.get_height(), label.get_width(),
#                                     label.get_height() ) )
#            else:
#                # it is a tuple of labels for a unit
#                name, type, men, guns = labels
#
#                # blit the labels
#                self.surface.blit ( name, (0, 0, name.get_width(), name.get_height()),
#                                    (50 + indent * 50, 100 + index * name.get_height(), name.get_width(),
#                                     name.get_height() ) )
#                self.surface.blit ( type, (0, 0, type.get_width(), type.get_height()),
#                                    (100 + indent * 50, 100 + index * type.get_height(), type.get_width(),
#                                     type.get_height() ) )
#                self.surface.blit ( men, (0, 0, men.get_width(), men.get_height()),
#                                    (150 + indent * 50, 100 + index * men.get_height(), men.get_width(),
#                                     men.get_height() ) )
#                self.surface.blit ( guns, (0, 0, guns.get_width(), guns.get_height()),
#                                    (200 + indent * 50, 100 + index * guns.get_height(), guns.get_width(),
#                                     guns.get_height() ) )
#
        # create the widget manager
        self.wm = WidgetManager (self.surface)

        # create all widgets
        self.createWidgets ()
            
                
        # blit out or full surface to the main surface
#        scenario.sdl.blit ( self.surface, (0, 0, properties.window_size_x, properties.window_size_y )
#                            (0, 0, properties.window_size_x, properties.window_size_y ) )

        # update the whole screen
        scenario.sdl.update_rect ( (0, 0, properties.window_size_x, properties.window_size_y ) )


    def createWidgets (self):
        "Creates all widgets for the dialog."
        # create the buttons for the next and previous buttons
        self.wm.register ( Button ( properties.path_dialogs + "butt-back-moff.png",
                                    properties.path_dialogs + "butt-back-mover.png",
                                    (850, 30 ), {widget.MOUSEBUTTONUP : self.prevScreen } ) )

        # labels
        self.wm.register ( Label (self.titlefont, "Scenario order of battle ", (10,10), color=(255, 0, 0)) )

        unionlabel = Label (self.smallfont, "Union brigades", (50, 80), color=(255, 255, 0) )
        self.wm.register ( unionlabel )

        # create the label summarizing the units of the union side
        unionlabel = self.createSummary ( organization.UNION, 200, 83 )
        self.wm.register ( unionlabel )
        
        # create labels for all union brigades and store the coordinate of the last used y-position
        lasty = self.createBrigadeLabels ( organization.UNION, 80 + unionlabel.getHeight () + 30 );

        
        rebellabel = Label (self.smallfont, "Rebel brigades", (50, lasty + 30), color=(255, 255, 0))
        self.wm.register ( rebellabel )

        # create the label summarizing the units of the rebel side
        rebellabel = self.createSummary ( organization.REBEL, 200, lasty + 30 + 3 )
        self.wm.register ( rebellabel )

        # create labels for all rebel brigades
        unionBrigades = self.createBrigadeLabels ( organization.REBEL,
                                                   lasty + 30 + rebellabel.getHeight () + 30 );


    def createBrigadeLabels (self, owner, starty):
        """Creates labels for all brigades owned by 'owner'."""
        index = starty

        # loop over all brigades owned by the correct player
        for brigade in scenario.brigades [owner].values ():

            # render a label and register it
            label =  Label (self.smallfont, brigade.getName (), (150, index),
                            color=(255, 0, 255))

            # register label so that it gets managed
            self.wm.register ( label )

            # also create a label with info about the brigade
            # increment the index
            index += label.getHeight () + 20

        # we're done, return the last index we used
        return index
    

    def createSummary (self, owner, x, y):
        "Creates a summary label for all the units of the specified owner."

        companies = []
        
        # first get all companies of all the brigades
        for brigade in scenario.brigades [ owner ].values ():
            companies = companies + brigade.getCompanies ()

        # now set some counters
        counts = { unit.INFANTRY: 0,
                   unit.CAVALRY: 0,
                   unit.ARTILLERY: 0 }
        guns = 0

        # loop over all companies
        for company in companies:
            # add the men to the proper counter
            counts [company.getType ()] += company.getMen ()
            guns += company.getGuns ()

        # now create a suitable label
        labeltext  = "infantry: " + str (counts[unit.INFANTRY]) + ", cavalry: " + str (counts[unit.CAVALRY])
        labeltext += ", artillery (men/guns): " + str (counts[unit.ARTILLERY]) + "/" + str (guns)

        # create and return the label
        return Label ( self.tinyfont, labeltext, (x,y), color=(255, 255, 255))
        

    def run (self):
        """Executes the dialog and runs its internal loop until a key is pressed. When that happens
        this dialog is terminated and the method returns."""

        # loop forever
        while 1:
            # get next event
            event = sdl.events_wait ()

            # see wether the widget manager wants to handle it
            if event != -1:
                # handle event and get the return code that tells us wehter it was handled or not
                returncode = self.wm.handle ( event )

                # is the event loop done?
                if returncode == widget.DONE:
                    return


    def prevScreen (self, event):
        """Callback triggered when the user clicks the 'Previous' button. This method simply cancels
        the event loop for this dialog's widget manager. Basically this dialog quits."""
        # we're done
        return widget.DONE
        # loop forever
        while 1:
            # get next event
            event = sdl.events_wait ()

            # see wether the widegt manager wants to handle it
            if event != -1 and self.wm.handle ( event ):
                # it's handled, nothing to see here folks
                continue

            # did we gert anything?
            if event != -1 and event.get_type () == sdl.KEYDOWN:
                # we're done here, go away
                return



#    def createLabels (self, owner):
#        """Creates the labels for all organizations. The returned data is a list with pairs of the
#        type (label,indent). The label is the surface to be blitted and the indent is the
#        indentation this label should have. A more indented label is a part of a larger organization
#        (which is less indented)."""
#        labels = []
#
#        # loop over all brigades owned by the correct player
#        for brigade in scenario.brigades [owner].values ():
#
#            # render a label
#            labels.append ( self.renderLabel ( self.tinyfont, brigade.getName (), (255,0,255), 0 ))
#
#            # loop over all regiments
#            for regiment in brigade.getRegiments ():
#                # render a label
#                labels.append ( self.renderLabel ( self.tinyfont, regiment.getName (), (0,255,255), 1 ))
#
#                # loop over all battallions
#                for battallion in regiment.getBattallions ():
#                    # render a label
#                    labels.append ( self.renderLabel ( self.tinyfont, battallion.getName (),
#                                                           (128,128,128), 2 ))
#
#                    # loop over the companies
#                    for company in battallion.getCompanies ():
#                        # render a label
#                        labels.append ( self.renderUnitLabels ( self.tinyfont, company, (255,255,0), 3 ))
#
#                # and companies too
#                for company in regiment.getCompanies ():
#                    # render a label
#                    labels.append ( self.renderUnitLabels ( self.tinyfont, company, (255,0,255), 3 ))
#
#        return labels
#            
#
#    def renderLabel (self, font, text, color, indent):
#        """Help method for rendering one single label. Returns a pair with (label, indent)."""
#        return ( indent, (font.render ( text, color, (0,0,0) ), ) )
#
#
#    def renderUnitLabels (self, font, unit, color, indent):
#        """Help method for rendering one single label of an unit. Renders a lot Returns a tuple of
#        label. with (label, indent).""" 
#
#        return ( indent, ( font.render ( unit.getName (), color, (0,0,0)),
#                           font.render ( unit.getType (), color, (0,0,0)),
#                           font.render ( str (unit.getMen ()), color, (0,0,0)),
#                           font.render ( str (unit.getGuns ()), color, (0,0,0)) ) )


#  Local Variables:
#  mode: auto-fill
#  fill-column: 100
#  End:
