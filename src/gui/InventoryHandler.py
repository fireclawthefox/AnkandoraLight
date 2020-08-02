import random
from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG

from gui.Inventory import GUI as Inventory

class InventoryHandler(DirectObject):
    def __init__(self):
        self.inventory = Inventory(base.a2dBottomRight)
        self.inventory.frmMain.setScale(0.9)

        self.show = self.inventory.show
        self.hide = self.inventory.hide

        self.accept("toggleInventory", self.toggleInventory)
        self.accept("updateInventory", self.setItems)

        potion = "assets/inventory/potions/Potion{}.png"
        self.inventory.frmPotion1["image"] = potion.format(random.randint(1,5))
        self.inventory.frmPotion2["image"] = potion.format(random.randint(1,5))
        self.inventory.frmPotion3["image"] = potion.format(random.randint(1,5))

        self.hide()

    def destroy(self):
        self.ignoreAll()
        self.inventory.destroy()

    def setItems(self, level, inventoryAssetPath):
        self.inventory.frmWeapon["image"] = inventoryAssetPath + "/weapon{}.png".format(level)
        self.inventory.frmArmor["image"] = inventoryAssetPath + "/armor{}.png".format(level)

    def setHealPotionCount(self, count):
        self.inventory.frmPotion1.hide()
        self.inventory.frmPotion2.hide()
        self.inventory.frmPotion3.hide()

        if count > 0:
            self.inventory.frmPotion1.show()
        if count > 1:
            self.inventory.frmPotion2.show()
        if count > 2:
            self.inventory.frmPotion3.show()

    def toggleInventory(self):
        if self.inventory.frmMain.isHidden():
            self.inventory.frmMain.show()
        else:
            self.inventory.frmMain.hide()
