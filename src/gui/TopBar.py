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
        
        self.frmMain = DirectFrame(
            frameColor=(0.25, 0.25, 0.25, 1.0),
            frameSize=(0.0, 2.0, -0.1, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmMain.setTransparency(0)

        self.btnLeave = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pad=(0.1, 0.1),
            pos=LPoint3f(0.115, 0, -0.075),
            relief=1,
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Leave',
            text_align=TextNode.A_center,
            text_scale=(0.75, 0.75),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
            command=base.messenger.send,
            extraArgs=["leaveRoom"],
        )
        self.btnLeave.setTransparency(0)

        self.lblPlayerName = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.55, 0, -0.075),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Label',
            text_align=TextNode.A_left,
            text_scale=(0.75, 0.75),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0.8, 0.8, 0.8, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblPlayerName.setTransparency(0)

        self.pg1983 = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.42, 0, -0.075),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Name:',
            text_align=TextNode.A_center,
            text_scale=(0.75, 0.75),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0.6, 0.6, 0.6, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.pg1983.setTransparency(0)


    def show(self):
        self.frmMain.show()

    def hide(self):
        self.frmMain.hide()

    def destroy(self):
        self.frmMain.destroy()
