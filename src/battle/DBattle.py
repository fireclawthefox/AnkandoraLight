from direct.distributed.DistributedObject import DistributedObject
from gui.BattleHandler import BattleHandler
from gui.BattleOverHandler import BattleOverHandler
from battle.BattleStats import BattleStats

class DBattle(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.battleHandler = BattleHandler(self.cr)

    def announceGenerate(self):
        print("GENERATE DBattle")
        self.battleHandler.show()
        self.accept("rollInitiative", self.d_rollInitiative)
        self.sendUpdate("isSpectating")
        # call the base class method
        DistributedObject.announceGenerate(self)

    def delete(self):
        print("DELETE DBattle")
        self.ignoreAll()
        self.battleHandler.destroy()
        DistributedObject.delete(self)

    def doSpectate(self):
        self.battleHandler.setSpectate()

    def d_rollInitiative(self):
        print("DO ROLL INIT")
        self.sendUpdate("rollInitiative")

    def d_attack(self):
        print("DO ATTACK")
        self.sendUpdate("playerAttack")

    def startBattle(self):
        print("START BATTLE CLIENT")
        pass

    def updateBattleStats(self, activePlayerName, battleStatsList):
        self.battleHandler.clearBattleStats()
        print("UPDATE STATS", activePlayerName, battleStatsList)
        for entry in battleStatsList:
            stats = BattleStats(entry)
            self.battleHandler.addBattleStats(stats)
        self.battleHandler.setActivePlayer(activePlayerName)

    def startRound(self):
        print("START ROUND")
        self.accept("attack", self.d_attack)
        self.battleHandler.enableAttackButton()

    def endRound(self):
        print("END ROUND")
        self.ignore("attack")
        self.battleHandler.disableAttackButton()

    def rolledInitiativeFailed(self):
        # probably ignore for now
        pass

    def rolledInitiative(self, roll):
        # wait for other players to roll and official start of battle
        pass

    def showHit(self, name, hitpoints):
        self.battleHandler.showHit(name, hitpoints)

    def gotDefeated(self, lostAllLifes, healthPotionsLeft):
        # check if we lost the battle or got some healing potions left which we
        # should refresh the gui with now
        print("THIS PLAYER GOT DEFEATED", lostAllLifes)
        base.messenger.send("updateHealthPotions", [healthPotionsLeft])

    def attackFailed(self):
        # probably ignore for now
        pass

    def enemyDefeated(self):
        print("ENEMY DEFEATED")
        pass

    def endBattle(self, wonBattle):
        boh = BattleOverHandler()
        if wonBattle == 1:
            boh.show("You won")
        else:
            boh.show("You lost")

        self.battleHandler.hide()
