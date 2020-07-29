
from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG

from gui.Inventory import GUI as Inventory

class InventoryHandler(DirectObject):
    def __init__(self):
        self.inventory = Inventory(base.a2dBottomRight)

        self.destroy = self.inventory.destroy
        self.show = self.inventory.show
        self.hide = self.inventory.hide

        self.origBtnZPos = self.inventory.btnToggleInventory.getZ()

        self.accept("toggleInventory", self.toggleInventory)

        self.hide()

    def setItems(self, level, inventoryAssetPath):
        self.inventory.frmWeapon["image"] = inventoryAssetPath + "weapon{}.png".format(level)
        self.inventory.frmArmor["image"] = inventoryAssetPath + "armor{}.png".format(level)
        self.inventory.frmPotion1["image"] = inventoryAssetPath + "HealthPotion.png"
        self.inventory.frmPotion2["image"] = inventoryAssetPath + "HealthPotion.png"
        self.inventory.frmPotion3["image"] = inventoryAssetPath + "HealthPotion.png"

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
            self.inventory.btnToggleInventory.setZ(self.origBtnZPos)
        else:
            self.inventory.frmMain.hide()
            self.inventory.btnToggleInventory.setZ(-self.inventory.btnToggleInventory["frameSize"][2])
