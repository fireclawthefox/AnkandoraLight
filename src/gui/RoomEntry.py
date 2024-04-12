#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectButton import DirectButton
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):
        
        self.frmRoomEntry = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(-1.0, 1.0, -0.1, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmRoomEntry.setTransparency(0)

        self.lblRoomName = DirectLabel(
            frameSize=(0.075, 15.0, -0.2, 0.8),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.975, 0, -0.065),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Room Name',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmRoomEntry,
        )
        self.lblRoomName.setTransparency(0)

        self.lblPlayerCount = DirectLabel(
            frameSize=(-1.15, 1.25, -0.2, 0.8),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.15, 0, -0.065),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='0/4',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmRoomEntry,
        )
        self.lblPlayerCount.setTransparency(0)

        self.lblGameType = DirectLabel(
            frameSize=(-4.0, 4.0, -0.2, 0.8),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.125, 0, -0.065),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Game Type',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmRoomEntry,
        )
        self.lblGameType.setTransparency(0)

        self.btnJoin = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pad=(0.1, 0.1),
            pos=LPoint3f(0.855, 0, -0.075),
            scale=LVecBase3f(0.075, 0.075, 0.075),
            text='Join',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmRoomEntry,
            command=base.messenger.send,
            extraArgs=["room_join"],
        )
        self.btnJoin.setTransparency(0)

        self.lblDifficulty = DirectLabel(
            frameSize=(-4.0, 4.0, -0.2, 0.8),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.545, 0, -0.065),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Difficulty',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmRoomEntry,
        )
        self.lblDifficulty.setTransparency(0)


    def show(self):
        self.frmRoomEntry.show()

    def hide(self):
        self.frmRoomEntry.hide()

    def destroy(self):
        self.frmRoomEntry.destroy()
