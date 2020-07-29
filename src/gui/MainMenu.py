#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):

        self.frmMenu = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(-0.4, 0.4, -0.5, 0.5),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmMenu.setTransparency(0)

        self.btnSingleplayer = DirectButton(
            frameSize=(-4.0, 4.0, -0.4, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.2),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Singleplayer',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMenu,
            command=base.messenger.send,
            extraArgs=["menu_singleplayer"],
        )
        self.btnSingleplayer.setTransparency(0)

        self.btnMultiplayer = DirectButton(
            frameSize=(-4.0, 4.0, -0.4, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.025),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Multiplayer',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMenu,
            command=base.messenger.send,
            extraArgs=["menu_multiplayer"],
        )
        self.btnMultiplayer.setTransparency(0)

        self.btnOptions = DirectButton(
            frameSize=(-4.0, 4.0, -0.4, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.15),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Options',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMenu,
            command=base.messenger.send,
            extraArgs=["menu_options"],
        )
        self.btnOptions.setTransparency(0)

        self.btnQuit = DirectButton(
            frameSize=(-4.0, 4.0, -0.4, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.325),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Quit',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMenu,
            command=base.messenger.send,
            extraArgs=["menu_quit"],
        )
        self.btnQuit.setTransparency(0)

        self.pg6375 = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            frameSize=(-4.25, 4.25, -1.25, 1.25),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/menu/Banner.png',
            pos=LPoint3f(0, 0, 0.475),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='',
            image_scale=LVecBase3f(4.5, 1, 1.5),
            image_pos=LPoint3f(0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMenu,
        )
        self.pg6375.setTransparency(1)


    def show(self):
        self.frmMenu.show()

    def hide(self):
        self.frmMenu.hide()

    def destroy(self):
        self.frmMenu.destroy()
