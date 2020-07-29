from direct.distributed.DistributedObjectAI import DistributedObjectAI
from enemy.EnemyAI import EnemyAI
from operator import itemgetter
from battle.BattleStats import BattleStats
from dice.SixSidedDice import SixSidedDice

from globalData.RoomGlobals import DIFFICULTY_EASY

class DBattleAI(DistributedObjectAI):
    def __init__(self, air, field, playersOnField, spectatorPlayers):
        DistributedObjectAI.__init__(self, air)

        self.playersOnField = playersOnField
        print("BATTLE WITH", len(self.playersOnField), "PLAYERS")
        self.spectatorPlayers = spectatorPlayers

        self.readyPlayers = []

        self.afterShowHitDelay = 3

        self.playerInitiatives = {}
        self.activePlayerId = -1

        self.fightOrder = []

        self.dice = SixSidedDice()

        self.enemyAI = EnemyAI(field.special, DIFFICULTY_EASY)

        self.field = field

    def rollInitiative(self):
        playerId = self.air.getAvatarIdFromSender()

        print("PLAYER", playerId, "ROLL INITIATIVE")

        if playerId in self.playerInitiatives.keys():
            self.sendUpdateToAvatarId(playerId, "rolledInitiativeFailed", [])
            return

        roll = self.dice.roll()
        self.playerInitiatives[playerId] = roll
        self.sendUpdateToAvatarId(playerId, "rolledInitiative", [roll])

        if len(self.playerInitiatives) == len(self.playersOnField):
            print("SORT AND START")
            self.sortByInitiativesAndStart()
        else:
            print("WAITING...", len(self.playerInitiatives), "/", len(self.playersOnField))

    def sortByInitiativesAndStart(self):
        enemyInit = self.enemyAI.getInitiative()
        for i in range(self.enemyAI.numEnemies):
            self.playerInitiatives[-1-i] = enemyInit
        self.fightOrder = sorted(
            self.playerInitiatives.items(),
            key=itemgetter(1),
            reverse=True)

        print("ORDER:", self.fightOrder)

        self.d_startBattle()

    def d_startBattle(self):
        print("START BATTLE")
        self.activePlayerId = self.fightOrder[0][0]

        self.sendUpdate("startBattle", [])

        self.d_updateBattleStats()

        if self.activePlayerId != -1:
            print("PLAYER START TURN")
            # player starts turn
            self.sendUpdateToAvatarId(self.activePlayerId, "startRound", [])

        else:
            print("ENEMY START TURN")
            # enemy starts turn
            self.enemyAttack()

    def d_updateBattleStats(self):
        statslist = []

        activePlayerName = ""
        for player in self.playersOnField:
            stats = BattleStats()
            stats.isEnemy = 0
            stats.name = player.name
            stats.atack = player.getAttack()
            stats.defense = player.getDefense()
            statslist.append(stats)
            if self.fightOrder[0][0] == player.avId:
                activePlayerName = player.name

        for enemyIdx in range(self.enemyAI.numEnemies):
            stats = BattleStats()
            stats.isEnemy = 1
            stats.name = "Enemy {}".format(enemyIdx+1)
            stats.atack = self.enemyAI.getAttack()
            stats.defense = self.enemyAI.getDefense()
            statslist.append(stats)
            enemyID = -1 * (enemyIdx+1)
            if self.fightOrder[0][0] == enemyID:
                activePlayerName = stats.name

        self.sendUpdate("updateBattleStats", [activePlayerName, statslist])

    def nextFighter(self):
        print("ROTATE")

        # rotate the fight order
        self.fightOrder = self.fightOrder[1:] + self.fightOrder[:1]

        self.activePlayerId = self.fightOrder[0][0]

        self.d_updateBattleStats()

        if self.activePlayerId < 0:
            # all IDs less then 0 (e.g. -1, -2, etc), are enemy IDs
            print("ENEMIES TURN")
            # enemies turn
            base.taskMgr.doMethodLater(2, self.enemyAttack, "delayedEnemyAttackTask", extraArgs=[], appendTask=False)
        else:
            print("PLAYERS TURN")
            # players turn
            print("SEND UPDATE TO", self.activePlayerId)
            self.sendUpdateToAvatarId(self.activePlayerId, "startRound", [])

    def enemyAttack(self):
        print("ENEMY ATTACK")
        atk = self.enemyAI.rollAttack()

        #TODO: Check difficulty:
        # Easy: Search for player with highest defense
        # Medium: Search for next player in Order
        # Hard: Search for player with lowest defense

        attackedPlayer = None
        # look for next player in order
        for fighterInfo in self.fightOrder:
            for player in self.playersOnField:
                if player.avId == fighterInfo[0]:
                    attackedPlayer = player
                    break
            if attackedPlayer is not None:
                break

        print("ENEMY ATTACKS:", attackedPlayer)
        if attackedPlayer.getDefense() <= atk:
            #player defeated
            if player.numHealPotions == 0:
                # has no potions left
                self.spectatorPlayers.append(player)
                self.playersOnField.remove(player)
                self.sendUpdateToAvatarId(player.avId, "gotDefeated", [True, 0])
                for entry in self.fightOrder[:]:
                    if entry[0] == player.avId:
                        self.fightOrder.remove(entry)
                        break

                print("PLAYER DEFEATED")
                if len(self.playersOnField) == 0:
                    print("ALL PLAYERS DEFEATED")
                    self.sendUpdate("showHit", [attackedPlayer.name, atk])

                    base.taskMgr.doMethodLater(self.afterShowHitDelay, self.battleOver, "delayedBattleOver", extraArgs=[False], appendTask=False)
                    return
            else:
                # can heal himself
                print("PLAYER CAN HEAL HIMSELF")
                player.numHealPotions -= 1
                self.sendUpdateToAvatarId(player.avId, "gotDefeated", [False, player.numHealPotions])

        self.sendUpdate("showHit", [attackedPlayer.name, atk])

        base.taskMgr.doMethodLater(self.afterShowHitDelay, self.nextFighter, "delayedNextFighter", extraArgs=[], appendTask=False)

    def playerAttack(self):
        playerId = self.air.getAvatarIdFromSender()

        if playerId != self.fightOrder[0][0]:
            self.sendUpdateToAvatarId(playerId, "attackFailed", [])
            return

        enemyName = "Enemy {}".format(self.enemyAI.numEnemies)
        atk = 0
        for player in self.playersOnField:
            if player.avId == playerId:
                atk = self.dice.roll() + player.getAttack()
                break

        if self.enemyAI.defeatedOne(atk):
            self.sendUpdate("enemyDefeated", [])
            for entry in self.fightOrder[:]:
                if entry[0] == -(self.enemyAI.numEnemies+1):
                    self.fightOrder.remove(entry)
                    break
            if self.enemyAI.defeatedAll():
                self.sendUpdate("showHit", [enemyName, atk])
                base.taskMgr.doMethodLater(self.afterShowHitDelay, self.battleOver, "delayedBattleOver", extraArgs=[True], appendTask=False)
                return

        self.sendUpdate("showHit", [enemyName, atk])

        self.sendUpdateToAvatarId(playerId, "endRound", [])
        base.taskMgr.doMethodLater(self.afterShowHitDelay, self.nextFighter, "delayedNextFighter", extraArgs=[], appendTask=False)

    def battleOver(self, playersWon):
        self.sendUpdate("endBattle", [playersWon])
        base.taskMgr.doMethodLater(3, self.endBattle, "delayedEndBattle", extraArgs=[playersWon], appendTask=False)

    def endBattle(self, playersWon):
        print("SEND", self.uniqueName("endBattle"))
        base.messenger.send(self.uniqueName("endBattle"), [self.field, playersWon])
