from panda3d.core import ConfigVariableString
from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG

from gui.BattleOver import GUI as BattleOver

class BattleOverHandler(DirectObject, BattleOver):
    def __init__(self):
        BattleOver.__init__(self)
        BattleOver.hide(self)

    def show(self, message):
        self.frmMain.show()
        self.frmMain["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.frmMain["sortOrder"] = 989
        self.frmMain["state"] = DGG.NORMAL
        self.lblVictory.setText(message)
        base.taskMgr.doMethodLater(3, self.destroy, "delayed hiding", extraArgs=[])
