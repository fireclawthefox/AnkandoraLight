#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectButton import DirectButton
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):

        self.frmMain = DirectFrame(
            frameColor=(1.0, 1.0, 1.0, 0.0),
            frameSize=(-0.436, 0.45, -0.5, 0.5),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/inventory/InventoryPlate.png',
            pos=LPoint3f(-0.4, 0, 0.52),
            image_scale=LVecBase3f(0.436, 1, 0.5),
            image_pos=LPoint3f(0, 0, 0),
            parent=rootParent,
        )
        self.frmMain.setTransparency(1)

        self.frmWeapon = DirectFrame(
            frameColor=(1.0, 0.0, 1.0, 0.0),
            frameSize=(-0.09, 0.09, -0.242, 0.242),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/inventory/thief/weapon1.png',
            pos=LPoint3f(-0.165, 0, 0.15),
            image_scale=LVecBase3f(0.09, 0, 0.242),
            image_pos=LPoint3f(0, 0, 0),
            parent=self.frmMain,
        )
        self.frmWeapon.setTransparency(1)

        self.frmArmor = DirectFrame(
            frameColor=(1.0, 0.0, 1.0, 0.0),
            frameSize=(-0.09, 0.09, -0.242, 0.242),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/inventory/thief/weapon1.png',
            pos=LPoint3f(0.18, 0, 0.15),
            image_scale=LVecBase3f(0.09, 0, 0.242),
            image_pos=LPoint3f(0, 0, 0),
            parent=self.frmMain,
        )
        self.frmArmor.setTransparency(1)

        self.frmPotion1 = DirectFrame(
            frameColor=(0.0, 1.0, 1.0, 0.0),
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/inventory/potions/Potion1.png',
            pos=LPoint3f(-0.23, 0, -0.315),
            image_scale=LVecBase3f(0.09, 0.09, 0.09),
            image_pos=LPoint3f(0, 0, 0),
            parent=self.frmMain,
        )
        self.frmPotion1.setTransparency(1)

        self.frmPotion2 = DirectFrame(
            frameColor=(0.0, 1.0, 1.0, 0.0),
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/inventory/potions/Potion2.png',
            pos=LPoint3f(0, 0, -0.325),
            image_scale=LVecBase3f(0.09, 0.09, 0.09),
            image_pos=LPoint3f(0, 0, 0),
            parent=self.frmMain,
        )
        self.frmPotion2.setTransparency(1)

        self.frmPotion3 = DirectFrame(
            frameColor=(0.0, 1.0, 1.0, 0.0),
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            hpr=LVecBase3f(0, 0, 0),
            image='./assets/inventory/potions/Potion3.png',
            pos=LPoint3f(0.25, 0, -0.315),
            image_scale=LVecBase3f(0.09, 0.1, 0.09),
            image_pos=LPoint3f(0, 0, 0),
            parent=self.frmMain,
        )
        self.frmPotion3.setTransparency(1)

        self.btnToggleInventory = DirectButton(
            frameColor=(0.15, 0.15, 0.15, 1.0),
            frameSize=(-0.4, 0.4, -0.02, 0.05),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.4, 0, 0.02),
            relief=1,
            scale=LVecBase3f(1, 1, 1),
            text='Toggle Inventory',
            text_align=TextNode.A_center,
            text_scale=(0.05, 0.05),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0.8, 0.8, 0.8, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=rootParent,
            command=base.messenger.send,
            extraArgs=["toggleInventory"],
            pressEffect=1,
        )
        self.btnToggleInventory.setTransparency(0)


    def show(self):
        self.frmMain.show()
        self.btnToggleInventory.show()

    def hide(self):
        self.frmMain.hide()
        self.btnToggleInventory.hide()

    def destroy(self):
        self.frmMain.destroy()
        self.btnToggleInventory.destroy()
