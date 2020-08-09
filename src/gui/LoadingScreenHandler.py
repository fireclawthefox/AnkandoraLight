#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG
from gui.LoadingScreen import GUI as LoadingScreen

class LoadingScreenHandler(DirectObject, LoadingScreen):
    """A semi-automatic loading screen which will listen for registered events
    to update itself.

    Simply call the registerLoadEvent for any portion of code that should update
    the waitbar. All events must have been registered before any of the
    registered events will be thrown!. E.g.:

    lsh = LoadingScreenHandler
    # register some events
    lsh.registerLoadEvent("event1")
    lsh.registerLoadEvent("event2")

    do some stuff...

    # throw the first event
    base.messenger.send("event1")

    # this event will be ignored by the loading screen!
    lsh.registerLoadEvent("event3")

    # this call will make the loading screen go to 100% and automatically
    # close it.
    base.messenger.send("event2")

    """
    def __init__(self):
        LoadingScreen.__init__(self)
        self.frmMain["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.frmMain["sortOrder"] = 1000
        self.frmMain["state"] = DGG.NORMAL
        self.frmMain.setState()
        self.reset()
        # make sure we're rendering this loading screen
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

        self.accept("registerLoadEvent", self.registerLoadEvent)

    def destroy(self):
        """Cleanup"""
        self.ignoreAll()
        LoadingScreen.destroy(self)

    def reset(self):
        """Reset the loading screen to it's initial state"""
        self.waitbar["value"] = 0
        self.waitbar["text"] = "0%"
        self.numLoadEvents = 0
        self.step = self.waitbar["range"]
        self.waitBarLocked = False

    def registerLoadEvent(self, loadDoneEvent):
        """Register an event which will update the waitbar"""
        if self.waitBarLocked: return False
        self.acceptOnce(loadDoneEvent, self.updateWaitbar)

        self.numLoadEvents += 1

        self.step = self.waitbar["range"] / self.numLoadEvents
        return True

    def updateWaitbar(self):
        """This function will be called for any registered event and should
        only be called internally. It will lock the loading screen and prevent
        registering any further events as well as add one step further to the
        waitbar"""
        self.waitBarLocked = True
        self.waitbar["value"] += self.step
        self.waitbar["text"] = "{}%".format(self.waitbar["value"])

        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

        # automatically hide the loading screen once it reached its end
        if self.waitbar["value"] == self.waitbar["range"]:
            self.frmMain.hide()
