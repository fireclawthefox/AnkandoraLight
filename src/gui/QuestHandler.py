#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from gui.Quest import GUI as Quest
from direct.interval.IntervalGlobal import LerpColorInterval
from globalData import RoomGlobals

DESC_NORMAL = \
"""Ankandora, a land full of adventures awaits you. Many have traveld the wide fields and step mountains, setteled in one of the cities and villages or fell, slain by the foes lurking in the darkest corners. Everyday new adventurers, scientists and tricksters come along and try their luck. Now follow the paths and fight against the foes standing in your way to save the land or clame it as yours and become the new king.

Normal Mode:
In this mode, you have to collect all the cards by beating the enemies waiting there for you. The last card (the crown) can only be reached once all other cards have been collected.
"""
DESC_RACE = \
"""Ankandora, a land full of adventures awaits you. Many have traveld the wide fields and step mountains, setteled in one of the cities and villages or fell, slain by the foes lurking in the darkest corners. Everyday new adventurers, scientists and tricksters come along and try their luck. Now follow the paths and fight against the foes standing in your way to save the land or clame it as yours and become the new king.

Race Mode:
Try be the first to reach the end field and beat the enemy there."""
CONTROL = \
"""If it's your turn, click the dice button or hit 'D'
Select any field that you could reach with your points and select it.
Finally, if you're done. Hit the Button in the bottom center or 'Space' to end your turn."""

class QuestHandler(Quest):
    def __init__(self, gameType):
        Quest.__init__(self)

        self.lblQuestDesc["text_wordwrap"] = 23
        self.lblControlDesc["text_wordwrap"] = 25

        self.lblQuestDesc["text"] = DESC_NORMAL if gameType == RoomGlobals.GAMETYPE_NORMAL else DESC_RACE
        self.lblControlDesc["text"] = CONTROL

        self.hide()

    def show(self, callbackFunc):
        self.btnClose["command"] = callbackFunc
        Quest.show(self)
        #TODO: Why doesn't this work with transparent textures...
        #LerpColorInterval(self.lblDescription, 1, (0,0,0,0), (1,1,1,0)).start()
