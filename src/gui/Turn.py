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

        self.btnEndTurn = DirectButton(
            borderWidth=(0.0, 0.0),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            frameSize=(-3.0, 3.0, -1.0, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/Turn/EndTurn.png',
            pos=LPoint3f(0, 0, 0.1),
            relief=1,
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='End Turn',
            image_scale=LVecBase3f(3, 0, 1),
            image_pos=LPoint3f(0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(1.0, 1.0),
            text_pos=(0.0, -0.3),
            text_fg=LVecBase4f(1, 1, 1, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=rootParent,
            command=base.messenger.send,
            extraArgs=["endTurn"],
            pressEffect=0,
        )
        self.btnEndTurn.setTransparency(1)


    def show(self):
        self.btnEndTurn.show()

    def hide(self):
        self.btnEndTurn.hide()

    def destroy(self):
        self.btnEndTurn.destroy()
