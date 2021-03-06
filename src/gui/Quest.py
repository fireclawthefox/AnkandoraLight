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

        self.lblDescription = DirectFrame(
            frameColor=(1.0, 1.0, 1.0, 0.0),
            frameSize=(-0.75, 0.75, -0.8, 0.8),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/quest/QuestBG.png',
            pos=LPoint3f(0, 0, 0),
            image_scale=LVecBase3f(0.75, 1, 0.8),
            image_pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.lblDescription.setTransparency(2)

        self.lblHeader = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.59),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Quest',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.lblDescription,
        )
        self.lblHeader.setTransparency(1)

        self.lblQuestDesc = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.6, 0, 0.525),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Quest description part 1',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.lblDescription,
        )
        self.lblQuestDesc.setTransparency(1)

        self.lblControl = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.6, 0, -0.25),
            scale=LVecBase3f(0.08, 0.08, 0.08),
            text='Controls',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.lblDescription,
        )
        self.lblControl.setTransparency(1)

        self.lblControlDesc = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.6, 0, -0.315),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text="If it's your turn, click the dice button or hit D",
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.lblDescription,
        )
        self.lblControlDesc.setTransparency(1)

        self.btnClose = DirectButton(
            frameColor=(0.8, 0.8, 0.8, 0.75),
            frameSize=(-1.288, 1.387, -0.213, 0.825),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.65),
            relief=1,
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Close',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.lblDescription,
            pressEffect=1,
        )
        self.btnClose.setTransparency(0)


    def show(self):
        self.lblDescription.show()

    def hide(self):
        self.lblDescription.hide()

    def destroy(self):
        self.lblDescription.destroy()
