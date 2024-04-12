#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from gui.MainMenu import GUI as MainMenu

class MainMenuHandler(MainMenu):
    def __init__(self):
        MainMenu.__init__(self)

        imageList = [
            'assets/menu/button/Normal.png',
            'assets/menu/button/Hover.png',
            'assets/menu/button/Click.png',
            'assets/menu/button/Disable.png']

        self.btnSingleplayer["image"] = imageList
        self.btnMultiplayer["image"] = imageList
        self.btnOptions["image"] = imageList
        self.btnQuit["image"] = imageList
