#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):
        
        self.frmStats = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(-0.55, 0.55, -0.1, 0.1),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmStats.setTransparency(0)

        self.lblName = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.3, 0, 0.05),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Name: ',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblName.setTransparency(0)

        self.lblAttack = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.3, 0, -0.01),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Attack:',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblAttack.setTransparency(0)

        self.lblDefense = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.3, 0, -0.075),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Defense:',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblDefense.setTransparency(0)

        self.imgPlayer = DirectLabel(
            frameSize=(-0.9, 0.9, -0.9, 0.9),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.445, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.imgPlayer.setTransparency(0)

        self.lblNameValue = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.075, 0, 0.05),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Player Name',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblNameValue.setTransparency(0)

        self.lblAttackValue = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.075, 0, -0.01),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='5',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblAttackValue.setTransparency(0)

        self.lblDefenseValue = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.075, 0, -0.075),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='10',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblDefenseValue.setTransparency(0)

        self.lblHealtPotions = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.12, 0, -0.075),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='Potions:',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblHealtPotions.setTransparency(0)

        self.lblHealthPotionsValue = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.325, 0, -0.075),
            scale=LVecBase3f(0.05, 0.05, 0.05),
            text='3',
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblHealthPotionsValue.setTransparency(0)

        self.lblHit = DirectLabel(
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.125),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='5',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(1, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmStats,
        )
        self.lblHit.setTransparency(0)


    def show(self):
        self.frmStats.show()

    def hide(self):
        self.frmStats.hide()

    def destroy(self):
        self.frmStats.destroy()
