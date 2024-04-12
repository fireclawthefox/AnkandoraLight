#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
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
            frameColor=(1, 1, 1, 1),
            frameSize=(-1.777778, 1.77777778, -1.1638, 1.1638),
            hpr=LVecBase3f(0, 0, 0),
            image='assets/menu/Background.png',
            pos=LPoint3f(0, 0, 0),
            image_scale=LVecBase3f(1.77778, 1, 1.1638),
            image_pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmMain.setTransparency(0)

        self.frmRoomList = DirectScrolledFrame(
            canvasSize=(-1.0, 1.0, -2.0, 0.0),
            frameColor=(1, 1, 1, 1),
            frameSize=(-1.0, 1.08, -1.4, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.7),
            scrollBarWidth=0.08,
            state='normal',
            horizontalScroll_borderWidth=(0.01, 0.01),
            horizontalScroll_frameSize=(-0.05, 0.05, -0.04, 0.04),
            horizontalScroll_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_pos=LPoint3f(0, 0, 0),
            horizontalScroll_decButton_borderWidth=(0.01, 0.01),
            horizontalScroll_decButton_frameSize=(-0.05, 0.05, -0.04, 0.04),
            horizontalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_decButton_pos=LPoint3f(-0.96, 0, -1.36),
            horizontalScroll_incButton_borderWidth=(0.01, 0.01),
            horizontalScroll_incButton_frameSize=(-0.05, 0.05, -0.04, 0.04),
            horizontalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_incButton_pos=LPoint3f(0.96, 0, -1.36),
            horizontalScroll_thumb_borderWidth=(0.01, 0.01),
            horizontalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_thumb_pos=LPoint3f(0, 0, -1.36),
            verticalScroll_borderWidth=(0.01, 0.01),
            verticalScroll_frameSize=(-0.04, 0.04, -0.05, 0.05),
            verticalScroll_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_pos=LPoint3f(0, 0, 0),
            verticalScroll_decButton_borderWidth=(0.01, 0.01),
            verticalScroll_decButton_frameSize=(-0.04, 0.04, -0.05, 0.05),
            verticalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_decButton_pos=LPoint3f(1.04, 0, -0.04),
            verticalScroll_incButton_borderWidth=(0.01, 0.01),
            verticalScroll_incButton_frameSize=(-0.04, 0.04, -0.05, 0.05),
            verticalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_incButton_pos=LPoint3f(1.04, 0, -1.28),
            verticalScroll_thumb_borderWidth=(0.01, 0.01),
            verticalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_thumb_pos=LPoint3f(1.04, 0, -0.4628),
            parent=self.frmMain,
        )
        self.frmRoomList.setTransparency(0)

        self.btnBack = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.96, 0, -0.825),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Back',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
            command=base.messenger.send,
            extraArgs=["roomList_back"],
        )
        self.btnBack.setTransparency(0)

        self.lblRoomName = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-1, 0, 0.725),
            scale=LVecBase3f(0.07, 0.1, 0.07),
            text='Room Name',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblRoomName.setTransparency(0)

        self.lblPlayerCount = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.15, 0, 0.725),
            scale=LVecBase3f(0.07, 0.1, 0.07),
            text='Players',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblPlayerCount.setTransparency(0)

        self.btnCreateRoom = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pad=(0.2, 0.2),
            pos=LPoint3f(-0.955, 0, -0.815),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='+',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.btnCreateRoom.setTransparency(0)

        self.btnReloadRoomList = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.025, 0, -0.825),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Reload Rooms',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
            command=base.messenger.send,
            extraArgs=["roomList_reload"],
        )
        self.btnReloadRoomList.setTransparency(0)

        self.lblGameType = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.125, 0, 0.725),
            scale=LVecBase3f(0.07, 0.1, 0.07),
            text='Type',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblGameType.setTransparency(0)

        self.lblDifficulty = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.54, 0, 0.72),
            scale=LVecBase3f(0.07, 0.1, 0.07),
            text='Difficulty',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblDifficulty.setTransparency(0)


    def show(self):
        self.frmMain.show()

    def hide(self):
        self.frmMain.hide()

    def destroy(self):
        self.frmMain.destroy()
