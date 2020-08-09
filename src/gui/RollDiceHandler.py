#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG

from gui.RollDice import GUI as RollDice

class RollDiceHandler(RollDice):
    def __init__(self):
        RollDice.__init__(self, base.a2dBottomLeft)
        self.hide()

    def updateRoll(self, roll):
        self.btnRollDice["text"] = str(roll)

    def clearRoll(self):
        self.btnRollDice["text"] = ""
