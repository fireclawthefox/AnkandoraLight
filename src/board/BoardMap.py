from board.Field import Field

def connectFields(fieldA, fieldB):
    fieldA.connections.append(fieldB)
    fieldB.connections.append(fieldA)

fightFields = ["Moon", "Triangle", "Square", "Circle", "Star", "Diamond", "Arrow"]
raceLevelUp = ["race_levelUp"]
gameMap = []

gameMap.append(Field("Start_1", 0, "StartField")) # 0
gameMap.append(Field("Start_2", 0, "StartField")) # 1
gameMap.append(Field("Start_3", 0, "StartField")) # 2
gameMap.append(Field("Start_4", 0, "StartField")) # 3

gameMap.append(Field("Field_01", 1)) # 0    4
gameMap.append(Field("Field_02", 1)) # 1    5
gameMap.append(Field("Field_03", 1, "Moon")) # 2    6
gameMap.append(Field("Field_04", 2)) # 3    7
gameMap.append(Field("Field_05", 2)) # 4    8
gameMap.append(Field("Field_06", 2)) # 5    9
gameMap.append(Field("Field_07", 2, "Triangle")) # 6    10
gameMap.append(Field("Field_08", 3)) # 7    11
gameMap.append(Field("Field_09", 3)) # 8    12
gameMap.append(Field("Field_10", 3)) # 9    13
gameMap.append(Field("Field_11", 4, "Square")) # 10 14
gameMap.append(Field("Field_12", 5)) # 11   15
gameMap.append(Field("Field_13", 2, "Circle")) # 12 16
gameMap.append(Field("Field_14", 2)) # 13   17
gameMap.append(Field("Field_15", 4, "race_levelUp")) # 14   18
gameMap.append(Field("Field_16", 3)) # 15   19
gameMap.append(Field("Field_17", 3)) # 16   20
gameMap.append(Field("Field_18", 2, "Star")) # 17   21
gameMap.append(Field("Field_19", 2)) # 18   22
gameMap.append(Field("Field_20", 6)) # 19   23
gameMap.append(Field("Field_21", 3, "Diamond")) # 20    24
gameMap.append(Field("Field_22", 4, "Arrow")) # 21  25
gameMap.append(Field("Field_23", 4)) # 22   26

gameMap.append(Field("EndField_1", 0, "EndField")) # 23 27
gameMap.append(Field("EndField_2", 0, "EndField")) # 24 28
gameMap.append(Field("EndField_3", 0, "EndField")) # 25 29
gameMap.append(Field("EndField_4", 0, "EndField")) # 26 30

connectFields(gameMap[0], gameMap[4])
connectFields(gameMap[1], gameMap[4])
connectFields(gameMap[2], gameMap[4])
connectFields(gameMap[3], gameMap[4])

connectFields(gameMap[4], gameMap[5])
connectFields(gameMap[5], gameMap[6])
connectFields(gameMap[6], gameMap[7])
connectFields(gameMap[7], gameMap[10])

connectFields(gameMap[4], gameMap[8])
connectFields(gameMap[8], gameMap[9])
connectFields(gameMap[9], gameMap[10])

connectFields(gameMap[10], gameMap[11])

connectFields(gameMap[11], gameMap[12])
connectFields(gameMap[12], gameMap[13])
connectFields(gameMap[13], gameMap[14])
connectFields(gameMap[14], gameMap[17])

connectFields(gameMap[11], gameMap[15])
connectFields(gameMap[15], gameMap[16])
connectFields(gameMap[16], gameMap[17])

connectFields(gameMap[17], gameMap[18])

connectFields(gameMap[18], gameMap[19])
connectFields(gameMap[19], gameMap[20])
connectFields(gameMap[20], gameMap[21])
connectFields(gameMap[21], gameMap[22])
connectFields(gameMap[22], gameMap[24])

connectFields(gameMap[18], gameMap[23])
connectFields(gameMap[23], gameMap[24])

connectFields(gameMap[24], gameMap[25])
connectFields(gameMap[25], gameMap[26])

connectFields(gameMap[26], gameMap[27])
connectFields(gameMap[26], gameMap[28])
connectFields(gameMap[26], gameMap[29])
connectFields(gameMap[26], gameMap[30])
