#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from gui.Options import GUI as Options

class OptionsHandler(DirectObject, Options):
    def __init__(self):
        Options.__init__(self)

        self.accept("options_ok", self.ok)
        self.accept("options_cancel", self.cancel)

        self.txtServer.enterText(base.serverHost.getValue())

        self.cbSFX["indicatorValue"] = base.sfxActive
        self.cbSFX.setIndicatorValue()

        self.cbMusic["indicatorValue"] = base.musicActive
        self.cbMusic.setIndicatorValue()


    def ok(self):
        serverUrl = self.txtServer.get()
        base.serverHost.setValue(serverUrl)

        base.enableSoundEffects(self.cbSFX["indicatorValue"])
        base.enableMusic(self.cbMusic["indicatorValue"])

        base.messenger.send("options_back")

    def cancel(self):
        base.messenger.send("options_back")
