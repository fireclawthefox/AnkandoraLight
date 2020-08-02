#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectOptionMenu import DirectOptionMenu
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):
        
        self.frmSinglePlayerCreateGame = DirectFrame(
            borderWidth=(0.01, 0.01),
            frameColor=(1, 1, 1, 1),
            frameSize=(-0.65, 0.65, -0.55, 0.55),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.025, 0, 0),
            relief=5,
            parent=rootParent,
        )
        self.frmSinglePlayerCreateGame.setTransparency(0)

        self.pg703 = DirectLabel(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.425),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Player Info',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmSinglePlayerCreateGame,
        )
        self.pg703.setTransparency(0)

        self.pg13803 = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.35, 0, -0.45),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Start',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmSinglePlayerCreateGame,
            command=base.messenger.send,
            extraArgs=["multiplayerPlayerInfo_start"],
        )
        self.pg13803.setTransparency(0)

        self.pg5219 = DirectLabel(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.6, 0, 0.02),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Player Class',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmSinglePlayerCreateGame,
        )
        self.pg5219.setTransparency(0)

        self.optionPlayerClass = DirectOptionMenu(
            items=['item1'],
            frameSize=(0.07500000298023224, 3.012500149011612, -0.11250001192092896, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.2, 0, 0.005),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='item1',
            cancelframe_frameSize=(-1, 1, -1, 1),
            cancelframe_hpr=LVecBase3f(0, 0, 0),
            cancelframe_pos=LPoint3f(0, 0, 0),
            cancelframe_relief=None,
            item_frameSize=(0.07500000298023224, 2.4125001430511475, -0.11250001192092896, 0.75),
            item_hpr=LVecBase3f(0, 0, 0),
            item_pos=LPoint3f(-0.075, 0, -0.75),
            item_text='item1',
            item0_text_align=TextNode.A_left,
            item0_text_scale=(1, 1),
            item0_text_pos=(0, 0),
            item0_text_fg=LVecBase4f(0, 0, 0, 1),
            item0_text_bg=LVecBase4f(0, 0, 0, 0),
            popupMarker_frameSize=(-0.5, 0.5, -0.2, 0.2),
            popupMarker_hpr=LVecBase3f(0, 0, 0),
            popupMarker_pos=LPoint3f(2.7125, 0, 0.31875),
            popupMarker_relief=2,
            popupMarker_scale=LVecBase3f(0.4, 0.4, 0.4),
            popupMenu_frameSize=(0, 2.3375001400709152, -0.862500011920929, 0),
            popupMenu_hpr=LVecBase3f(0, 0, 0),
            popupMenu_pos=LPoint3f(0, 0, 0),
            popupMenu_relief='raised',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmSinglePlayerCreateGame,
        )
        self.optionPlayerClass.setTransparency(0)

        self.btnCancel = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.325, 0, -0.45),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Cancel',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmSinglePlayerCreateGame,
            command=base.messenger.send,
            extraArgs=["multiplayerPlayerInfo_back"],
        )
        self.btnCancel.setTransparency(0)


    def show(self):
        self.frmSinglePlayerCreateGame.show()

    def hide(self):
        self.frmSinglePlayerCreateGame.hide()

    def destroy(self):
        self.frmSinglePlayerCreateGame.destroy()
