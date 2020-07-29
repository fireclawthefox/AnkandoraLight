import os
import csv
from panda3d.core import ExecutionEnvironment

class ClassManager():
    def __init__(self):
        rootdir = ExecutionEnvironment.getEnvironmentVariable("MAIN_DIR")
        self.classConfigurationCSV = os.path.join(rootdir, "config", "playerClasses.csv")
        self.classDefinitions = []

        with open(self.classConfigurationCSV, newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                self.classDefinitions.append(row)

    def getDataFor(self, classType):
        if self.classDefinitions is None: return None
        for row in self.classDefinitions:
            if row["class_type"] == classType.lower():
                return row

    def getAttack(self, classType, level):
        data = self.getDataFor(classType)
        if data is None:
            print("ERROR READING ATTACK VALUE")
            return 0

        return int(data["attack_lv{}".format(level)])

    def getDefense(self, classType, level):
        data = self.getDataFor(classType)
        if data is None:
            print("ERROR READING DEFENSE VALUE")
            return 0

        return int(data["defense_lv{}".format(level)])

    def getModel(self, classType):
        data = self.getDataFor(classType)
        if data is None:
            print("ERROR READING MODEL VALUE")
            return ""

        return data["model"]

    def getInventoryDir(self, classType):
        data = self.getDataFor(classType)
        if data is None:
            print("ERROR READING INVENTORY VALUE")
            return ""

        return data["inventory"]
