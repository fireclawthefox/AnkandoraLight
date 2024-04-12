#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import os
import csv
from panda3d.core import ExecutionEnvironment
from globalData import RoomGlobals
from dice.SixSidedDice import SixSidedDice

class EnemyAI():
    def __init__(self, enemyFieldName, difficultyNameID):
        rootdir = ExecutionEnvironment.getEnvironmentVariable("MAIN_DIR")
        self.enemyConfigurationCSV = os.path.join(rootdir, "config", "enemies.csv")
        self.enemyDefinitions = []

        # create the enemies dice
        self.dice = SixSidedDice()

        self.enemyFieldName = enemyFieldName
        self.difficultyName = RoomGlobals.DIFFICULTIES_AS_NAMES[difficultyNameID]

        # load the csv file data
        with open(self.enemyConfigurationCSV, newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                self.enemyDefinitions.append(row)

        self.numEnemies = self.getNumEnemies()

    def getData(self):
        if self.enemyDefinitions is None: return None
        for row in self.enemyDefinitions:
            if row["field"] == self.enemyFieldName and row["difficulty"] == self.difficultyName:
                return row

    def getAttack(self):
        data = self.getData()
        if data is None:
            print("ERROR READING ATTACK VALUE")
            return 0

        return int(data["attack"])

    def getDefense(self):
        data = self.getData()
        if data is None:
            print("ERROR READING DEFENSE VALUE")
            return 0

        return int(data["defense"])

    def getInitiative(self):
        data = self.getData()
        if data is None:
            print("ERROR READING INITIATIVE VALUE")
            return 0

        return int(data["initiative"])

    def getNumEnemies(self):
        """Get the number of enemies stored in the configuration file"""
        data = self.getData()
        if data is None:
            print("ERROR READING NUMBER ENEMIES VALUE")
            return 0

        return int(data["number_enemies"])

    def rollAttack(self):
        """Calculates one attack of this enemy"""
        roll = self.dice.roll()
        attack = roll + self.getAttack()
        return attack

    def defeatedOne(self, attackStrength):
        """Check if an enemy has been defeated given the strength of the attack.
        If an enemy is defeated, the numEnemies variable will be reduced by one
        and this function will return True, False otherwise."""
        if attackStrength >= self.getDefense():
            self.numEnemies -= 1
            return True
        return False

    def defeatedAll(self):
        """Check if all enemies have been defeated"""
        return self.numEnemies <= 0
