from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG
from gui.Battle import GUI as Battle
from gui.BattleStats import GUI as BattleStats
from direct.interval.IntervalGlobal import Sequence, Func, Wait

class BattleHandler(DirectObject):
    def __init__(self, cr):
        self.battle = Battle()

        self.battle.frmBattle["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.battle.frmBattle["sortOrder"] = 980
        self.battle.frmBattle["state"] = DGG.NORMAL
        self.battle.frmBattle.setState()


        self.battle.frmRollInitiative["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.battle.frmRollInitiative["state"] = DGG.NORMAL
        self.battle.frmRollInitiative.setState()

        self.show = self.battle.show
        self.hide = self.battle.hide

        self.acceptOnce("rollInitiative", self.rolledInitiative)

        self.hide()

        self.playerStatsList = []
        self.enemyStatsList = []

    def addBattleStats(self, stats):
        s = None
        if stats.isEnemy:
            i = len(self.playerStatsList)
            s = BattleStats(self.battle.frmEnemies)
            s.frmStats.setZ((self.battle.frmEnemies["frameSize"][3]-0.15) - i*0.3)
            self.playerStatsList.append(s)
        else:
            i = len(self.enemyStatsList)
            s = BattleStats(self.battle.frmPlayers)
            s.frmStats.setZ((self.battle.frmPlayers["frameSize"][3]-0.15) - i*0.3)
            self.enemyStatsList.append(s)
        s.lblNameValue["text"] = stats.name
        s.lblAttackValue["text"] = str(stats.atack)
        s.lblDefenseValue["text"] = str(stats.defense)
        s.lblHit.hide()

    def showHit(self, name, hitpoints):
        seq = None
        for s in self.playerStatsList:
            if s.lblNameValue["text"] == name:
                s.lblHit["text"] = str(hitpoints)
                Sequence(
                    Func(s.lblHit.show),
                    s.lblHit.scaleInterval(1.0, s.lblHit.getScale(), startScale=0),
                    Wait(1),
                    Func(s.lblHit.hide)).start()
                break
        for s in self.enemyStatsList:
            if s.lblNameValue["text"] == name:
                s.lblHit["text"] = str(hitpoints)
                Sequence(
                    Func(s.lblHit.show),
                    s.lblHit.scaleInterval(1.0, s.lblHit.getScale(), startScale=0),
                    Wait(1),
                    Func(s.lblHit.hide)).start()
                break

    def clearBattleStats(self):
        for s in self.playerStatsList:
            s.destroy()
        self.playerStatsList = []

        for s in self.enemyStatsList:
            s.destroy()
        self.enemyStatsList = []

    def setActivePlayer(self, name):
        print("SET ACTIVE PLAYER TO:", name)
        for s in self.playerStatsList:
            if s.lblNameValue["text"] == name:
                print("THIS PLAYER IS ACTIVE")
                s.frmStats.setScale(1.05)
            else:
                s.frmStats.setScale(1)
        for s in self.enemyStatsList:
            if s.lblNameValue["text"] == name:
                print("THIS ENEMY IS ACTIVE")
                s.frmStats.setScale(1.05)
            else:
                s.frmStats.setScale(1)

    def enableAttackButton(self):
        print("ENABLE ATTACK BUTTON")
        self.battle.btnAttack["state"] = DGG.NORMAL
        self.battle.btnAttack.setState()

    def disableAttackButton(self):
        self.battle.btnAttack["state"] = DGG.DISABLED
        self.battle.btnAttack.setState()

    def rolledInitiative(self):
        self.battle.frmRollInitiative.hide()

    def destroy(self):
        self.ignoreAll()
        self.battle.destroy()
        del self.battle

    def setSpectate(self):
        self.battle.frmRollInitiative.hide()
        self.battle.btnAttack.hide()
