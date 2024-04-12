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

        self.frmBattle = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-1.5, 1.5, -1.0, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmBattle.setTransparency(0)

        self.lblBattle = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.75),
            scale=LVecBase3f(0.2, 0.2, 0.2),
            text='Battle',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmBattle,
        )
        self.lblBattle.setTransparency(0)

        self.frmPlayers = DirectFrame(
            frameColor=(0.25, 0.25, 0.25, 0.25),
            frameSize=(-0.6, 0.6, -0.75, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.85, 0, -0.1),
            parent=self.frmBattle,
        )
        self.frmPlayers.setTransparency(0)

        self.frmEnemies = DirectFrame(
            frameColor=(0.25, 0.25, 0.25, 0.25),
            frameSize=(-0.6, 0.6, -0.75, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.85, 0, -0.1),
            parent=self.frmBattle,
        )
        self.frmEnemies.setTransparency(0)

        self.btnAttack = DirectButton(
            frameSize=(-2.0, 2.0, -2.0, 2.0),
            frameColor=(0,0,0,0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.1),
            relief=1,
            scale=LVecBase3f(0.1, 0.1, 0.1),
            image="assets/battle/attack.png",
            image_scale=(2,2,2),
            text='Attack',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0.0, -2.5),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmBattle,
            command=base.messenger.send,
            extraArgs=["attack"],
            pressEffect=0,
        )
        self.btnAttack.setTransparency(1)

        self.frmRollInitiative = DirectFrame(
            frameColor=(0.0, 0.0, 0.0, 0.25),
            frameSize=(-1.333, 1.333, -1.0, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            parent=self.frmBattle,
        )
        self.frmRollInitiative.setTransparency(0)

        self.btnRollInitiative = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Roll Initiative',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmRollInitiative,
            command=base.messenger.send,
            extraArgs=["rollInitiative"],
            pressEffect=1,
        )
        self.btnRollInitiative.setTransparency(0)


    def show(self):
        self.frmBattle.show()

    def hide(self):
        self.frmBattle.hide()

    def destroy(self):
        self.frmBattle.destroy()
