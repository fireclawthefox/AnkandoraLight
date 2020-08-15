#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectCheckButton import DirectCheckButton
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
            frameSize=(-1.777, 1.777, -1.0, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            image='assets/menu/Background.png',
            pos=LPoint3f(0, 0, 0),
            image_scale=LVecBase3f(1.77778, 0, 1.1638),
            image_pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmMain.setTransparency(0)

        self.lblptions = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.8),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Options',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblptions.setTransparency(0)

        self.lblServer = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.75, 0, 0.175),
            scale=LVecBase3f(1, 1, 1),
            text='Game Server URL:',
            text_align=TextNode.A_left,
            text_scale=(0.05, 0.05),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblServer.setTransparency(0)

        self.btnOk = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.375, 0, -0.775),
            relief=1,
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Ok',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
            command=base.messenger.send,
            extraArgs=["options_ok"],
            pressEffect=1,
        )
        self.btnOk.setTransparency(0)

        self.btnCancel = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.275, 0, -0.775),
            relief=1,
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Cancel',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
            command=base.messenger.send,
            extraArgs=["options_cancel"],
            pressEffect=1,
        )
        self.btnCancel.setTransparency(0)

        self.txtServer = DirectEntry(
            borderWidth=(0.01, 0.01),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.15, 0, 0.17),
            scale=LVecBase3f(1, 1, 1),
            width=25.0,
            text_align=TextNode.A_left,
            text_scale=(0.05, 0.05),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.txtServer.setTransparency(0)

        self.cbMusic = DirectCheckButton(
            frameSize=(-3.0, 2.0, -0.3, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            indicatorValue=1,
            pos=LPoint3f(0, 0, -0.21),
            scale=LVecBase3f(0.05, 0.1, 0.05),
            text='Music',
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-2.625, 0, 0.05),
            indicator_relief='sunken',
            indicator_text_align=TextNode.A_center,
            indicator_text_scale=(1, 1),
            indicator_text_pos=(0, -0.2),
            indicator_text_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text_bg=LVecBase4f(0, 0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(1.0, 1.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.cbMusic.setTransparency(0)

        self.cbSFX = DirectCheckButton(
            frameSize=(-3.0, 2.0, -0.3, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            indicatorValue=1,
            pos=LPoint3f(0, 0, -0.315),
            scale=LVecBase3f(0.05, 0.1, 0.05),
            text='SFX',
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-2.625, 0, 0.05),
            indicator_relief='sunken',
            indicator_text_align=TextNode.A_center,
            indicator_text_scale=(1, 1),
            indicator_text_pos=(0, -0.2),
            indicator_text_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text_bg=LVecBase4f(0, 0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.cbSFX.setTransparency(0)

        self.lblAudio = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.1),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Audio',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblAudio.setTransparency(0)

        self.lblConnection = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.3),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Connection',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMain,
        )
        self.lblConnection.setTransparency(0)


    def show(self):
        self.frmMain.show()

    def hide(self):
        self.frmMain.hide()

    def destroy(self):
        self.frmMain.destroy()
