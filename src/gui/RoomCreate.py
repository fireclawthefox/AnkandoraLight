#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectOptionMenu import DirectOptionMenu
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):
        
        self.frmCreateRoom = DirectFrame(
            borderWidth=(0.01, 0.01),
            frameColor=(1, 1, 1, 1),
            frameSize=(-0.65, 0.65, -0.55, 0.55),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            relief=5,
            parent=rootParent,
        )
        self.frmCreateRoom.setTransparency(0)

        self.btnOk = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.425, 0, -0.45),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='OK',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmCreateRoom,
            command=base.messenger.send,
            extraArgs=["createRoom_Ok"],
        )
        self.btnOk.setTransparency(0)

        self.btnCancel = DirectButton(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.4, 0, -0.45),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Cancel',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmCreateRoom,
            command=base.messenger.send,
            extraArgs=["createRoom_Cancel"],
        )
        self.btnCancel.setTransparency(0)

        self.pg1640 = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.425),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Create New Room',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmCreateRoom,
        )
        self.pg1640.setTransparency(0)

        self.pg2148 = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.05, 0, 0.24),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Room Name',
            text_align=TextNode.A_right,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmCreateRoom,
        )
        self.pg2148.setTransparency(0)

        self.pg2173 = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.05, 0, 0.065),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='# of Players',
            text_align=TextNode.A_right,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmCreateRoom,
        )
        self.pg2173.setTransparency(0)

        self.pg2201 = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.05, 0, -0.115),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Game Type',
            text_align=TextNode.A_right,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmCreateRoom,
        )
        self.pg2201.setTransparency(0)

        self.entryRoomName = DirectEntry(
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(0.08, 0, 0.25),
            scale=LVecBase3f(0.05, 0.1, 0.05),
            width=8.0,
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmCreateRoom,
        )
        self.entryRoomName.setTransparency(0)

        self.optionNumPlayers = DirectOptionMenu(
            items=['item1'],
            frameSize=(0.07500000298023224, 3.012500149011612, -0.11250001192092896, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.175, 0, 0.06),
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
            parent=self.frmCreateRoom,
        )
        self.optionNumPlayers.setTransparency(0)

        self.optionGameType = DirectOptionMenu(
            items=['item1'],
            frameSize=(0.07500000298023224, 3.012500149011612, -0.11250001192092896, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.175, 0, -0.125),
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
            parent=self.frmCreateRoom,
        )
        self.optionGameType.setTransparency(0)

        self.pg629 = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            frameSize=(-1.15, 1.25, -0.113, 0.725),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.055, 0, -0.3),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Difficulty',
            text_align=TextNode.A_right,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmCreateRoom,
        )
        self.pg629.setTransparency(0)

        self.optionDifficulty = DirectOptionMenu(
            items=['item1'],
            frameSize=(0.1, 3.013, -0.113, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.175, 0, -0.305),
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
            parent=self.frmCreateRoom,
        )
        self.optionDifficulty.setTransparency(0)


    def show(self):
        self.frmCreateRoom.show()

    def hide(self):
        self.frmCreateRoom.hide()

    def destroy(self):
        self.frmCreateRoom.destroy()
