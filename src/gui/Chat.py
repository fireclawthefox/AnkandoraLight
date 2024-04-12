#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectButton import DirectButton
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):
        
        self.frmChat = DirectFrame(
            frameColor=(0.25, 0.25, 0.25, 1.0),
            frameSize=(-0.4, 0.4, -1.25, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmChat.setTransparency(0)

        self.frmMessages = DirectScrolledFrame(
            borderWidth=(0.005, 0.005),
            canvasSize=(-0.38, 0.34, -1.2, 0.0),
            frameColor=(1, 1, 1, 1),
            frameSize=(-0.38, 0.38, -1.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.1),
            relief=3,
            scrollBarWidth=0.03,
            state='normal',
            horizontalScroll_borderWidth=(0.01, 0.01),
            horizontalScroll_frameSize=(-0.05, 0.05, -0.015, 0.015),
            horizontalScroll_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_pos=LPoint3f(0, 0, 0),
            horizontalScroll_decButton_borderWidth=(0.01, 0.01),
            horizontalScroll_decButton_frameSize=(-0.05, 0.05, -0.04, 0.04),
            horizontalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_decButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_incButton_borderWidth=(0.01, 0.01),
            horizontalScroll_incButton_frameSize=(-0.05, 0.05, -0.04, 0.04),
            horizontalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_incButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_thumb_borderWidth=(0.01, 0.01),
            horizontalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_thumb_pos=LPoint3f(0, 0, 0),
            verticalScroll_borderWidth=(0.01, 0.01),
            verticalScroll_frameSize=(-0.015, 0.015, -0.05, 0.05),
            verticalScroll_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_pos=LPoint3f(0, 0, 0),
            verticalScroll_decButton_borderWidth=(0.01, 0.01),
            verticalScroll_decButton_frameSize=(-0.04, 0.04, -0.05, 0.05),
            verticalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_decButton_pos=LPoint3f(0.36, 0, -0.02),
            verticalScroll_incButton_borderWidth=(0.01, 0.01),
            verticalScroll_incButton_frameSize=(-0.04, 0.04, -0.05, 0.05),
            verticalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_incButton_pos=LPoint3f(0.36, 0, -0.98),
            verticalScroll_thumb_borderWidth=(0.01, 0.01),
            verticalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_thumb_pos=LPoint3f(0.36, 0, -0.418625),
            parent=self.frmChat,
        )
        self.frmMessages.setTransparency(0)

        self.txtMessage = DirectEntry(
            borderWidth=(0.005, 0.005),
            frameColor=(1.0, 1.0, 1.0, 1.0),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-0.375, 0, -1.195),
            relief=3,
            scale=LVecBase3f(0.045, 0.045, 0.045),
            width=14.0,
            text_align=TextNode.A_left,
            text_scale=(1.0, 1.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmChat,
        )
        self.txtMessage.setTransparency(0)

        self.btnSend = DirectButton(
            frameColor=(0.0, 0.0, 0.0, 0.0),
            frameSize=(-0.4, 0.4, -0.4, 0.4),
            hpr=LVecBase3f(0, 0, 0),
            image='assets/chat/ChatSend.png',
            pos=LPoint3f(0.33, 0, -1.18),
            relief=1,
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='',
            image_scale=LVecBase3f(0.4, 1, 0.4),
            image_pos=LPoint3f(0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmChat,
            command=base.messenger.send,
            extraArgs=["sendMessage"],
        )
        self.btnSend.setTransparency(1)

        self.btnToggleChat = DirectButton(
            frameColor=(0.15, 0.15, 0.15, 1.0),
            frameSize=(-0.4, 0.4, -0.02, 0.05),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.05),
            relief=1,
            scale=LVecBase3f(1, 1, 1),
            text='Toggle Chat',
            text_align=TextNode.A_center,
            text_scale=(0.05, 0.05),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0.8, 0.8, 0.8, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=rootParent,
            command=base.messenger.send,
            extraArgs=["toggleChat"],
        )
        self.btnToggleChat.setTransparency(0)


    def show(self):
        self.frmChat.show()
        self.btnToggleChat.show()

    def hide(self):
        self.frmChat.hide()
        self.btnToggleChat.hide()

    def destroy(self):
        self.frmChat.destroy()
        self.btnToggleChat.destroy()
