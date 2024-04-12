#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from gui.GameOver import GUI as GameOver
from direct.gui import DirectGuiGlobals as DGG

class GameOverHandler(GameOver):
    def __init__(self):
        GameOver.__init__(self)
        self.frmMain["text_scale"] = 0.07
        self.frmMain["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.frmMain["state"] = DGG.NORMAL
        self.frmMain.setState()
        self.hide()

    def setEndMessage(self, msg):
        self.lblMessage["text"] = msg

    def show(self, msg):
        self.setEndMessage(msg)
        GameOver.show(self)
