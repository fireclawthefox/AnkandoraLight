#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from gui.TopBar import GUI as TopBar

class TopBarHandler(DirectObject, TopBar):
    def __init__(self, cr):
        self.cr = cr
        TopBar.__init__(self, base.a2dTopLeft)
        self.accept(self.cr.uniqueName("setPlayerName"), self.setPlayerName)

        self.hide()

    def destroy(self):
        self.ignoreAll()
        TopBar.destroy(self)

    def setPlayerName(self, playerName):
        self.lblPlayerName["text"] = playerName
