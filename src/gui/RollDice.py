#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectButton import DirectButton
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):

        self.btnRollDice = DirectButton(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            frameSize=(-0.25, 0.25, -0.25, 0.25),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/Dice/DiceButton.png',
            pos=LPoint3f(0.25, 0, 0.25),
            relief=1,
            scale=LVecBase3f(1, 1, 1),
            text='',
            image_scale=LVecBase3f(0.25, 0.25, 0.25),
            image_pos=LPoint3f(0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(0.15, 0.15),
            text_pos=(-0.08, -0.09),
            text_fg=LVecBase4f(1, 1, 1, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=rootParent,
            command=base.messenger.send,
            extraArgs=["rollDice"],
            pressEffect=0,
        )
        self.btnRollDice.setTransparency(1)


    def show(self):
        self.btnRollDice.show()

    def hide(self):
        self.btnRollDice.hide()

    def destroy(self):
        self.btnRollDice.destroy()
