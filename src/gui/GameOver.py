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
            frameColor=(0.0, 0.0, 0.0, 0.75),
            frameSize=(-1, 1, -1, 1),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmMain.setTransparency(1)

        self.btnQuit = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.75),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Quit',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
            command=base.messenger.send,
            extraArgs=["quitRoom"],
            pressEffect=1,
        )
        self.btnQuit.setTransparency(0)

        self.lblMessage = DirectLabel(
            frameColor=(0.0, 0.0, 0.0, 0.0),
            frameSize=(-2.981, 3.106, -0.325, 0.725),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            scale=LVecBase3f(0.2, 0.2, 0.2),
            text='Player A Won',
            text_align=TextNode.A_center,
            text_scale=(1.0, 1.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(1, 1, 1, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblMessage.setTransparency(0)


    def show(self):
        self.frmMain.show()

    def hide(self):
        self.frmMain.hide()

    def destroy(self):
        self.frmMain.destroy()
