#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import random
from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG
from direct.interval.IntervalGlobal import Sequence, Func

from gui.Inventory import GUI as Inventory

class InventoryHandler(DirectObject, Inventory):
    def __init__(self):
        Inventory.__init__(self, base.a2dBottomRight)
        self.frmMain.setScale(0.9)

        self.accept("toggleInventory", self.toggleInventory)
        self.accept("updateInventory", self.setItems)

        potion = "assets/inventory/potions/Potion{}.png"
        self.frmPotion1["image"] = potion.format(random.randint(1,5))
        self.frmPotion2["image"] = potion.format(random.randint(1,5))
        self.frmPotion3["image"] = potion.format(random.randint(1,5))

        self.hideIval = None

        self.hide()

    def destroy(self):
        self.ignoreAll()
        Inventory.destroy(self)

    def setItems(self, level, inventoryAssetPath):
        """Set the weapon and armor slots according to the given level and
        inventory asset path. It will look for a weapon{level}.png and
        armor{level}.png file."""
        self.frmWeapon["image"] = inventoryAssetPath + "/weapon{}.png".format(level)
        self.frmArmor["image"] = inventoryAssetPath + "/armor{}.png".format(level)

    def setHealPotionCount(self, count):
        """Show as much health potions as given with count. Count can go up to
        a maximum of 3. Higher values will be discarded."""
        self.frmPotion1.hide()
        self.frmPotion2.hide()
        self.frmPotion3.hide()

        if count > 0:
            self.frmPotion1.show()
        if count > 1:
            self.frmPotion2.show()
        if count > 2:
            self.frmPotion3.show()

    def toggleInventory(self):
        """Show or hide the inventory frame dependend on its current
        visibility"""
        if self.hideIval is not None and not self.hideIval.isStopped():
            print("Ival is running")
            return
        print("toggle inventory")
        base.messenger.send("playSFXSlide")
        if self.frmMain.isHidden():
            self.hideIval = Sequence(
                Func(self.frmMain.show),
                self.frmMain.posInterval(
                    0.5,
                    (self.frmMain.getX(), self.frmMain.getY(), self.frmMain.getZ() + 1)))
            self.hideIval.start()
        else:
            self.hideIval = Sequence(
                self.frmMain.posInterval(
                    0.5,
                    (self.frmMain.getX(), self.frmMain.getY(), self.frmMain.getZ() - 1)),
                Func(self.frmMain.hide))
            self.hideIval.start()
