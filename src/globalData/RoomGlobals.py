# GAME INFORMATION

GAMETYPE_NORMAL = 0
GAMETYPE_RACE = 1
ALL_GAMETYPES = [GAMETYPE_NORMAL, GAMETYPE_RACE]
ALL_GAMETYPES_AS_NAMES = ["Normal", "Race"]

PLAYERCLASS_WARRIOR = 0
PLAYERCLASS_THIEVE = 1
PLAYERCLASS_MAGE = 2
PLAYERCLASS_ARCHER = 3
ALL_PLAYERCLASSES = [PLAYERCLASS_WARRIOR, PLAYERCLASS_THIEVE, PLAYERCLASS_MAGE, PLAYERCLASS_ARCHER]
ALL_PLAYERCLASSES_AS_NAMES = ["Warrior", "Thief", "Mage", "Archer"]
Name2PlayerClassID = {
    ALL_PLAYERCLASSES_AS_NAMES[0]:PLAYERCLASS_WARRIOR,
    ALL_PLAYERCLASSES_AS_NAMES[1]:PLAYERCLASS_THIEVE,
    ALL_PLAYERCLASSES_AS_NAMES[2]:PLAYERCLASS_MAGE,
    ALL_PLAYERCLASSES_AS_NAMES[3]:PLAYERCLASS_ARCHER
    }
PlayerClassID2Name = {
    PLAYERCLASS_WARRIOR:ALL_PLAYERCLASSES_AS_NAMES[0],
    PLAYERCLASS_THIEVE:ALL_PLAYERCLASSES_AS_NAMES[1],
    PLAYERCLASS_MAGE:ALL_PLAYERCLASSES_AS_NAMES[2],
    PLAYERCLASS_ARCHER:ALL_PLAYERCLASSES_AS_NAMES[3]
    }

DIFFICULTY_EASY = 0
DIFFICULTY_MEDIUM = 1
DIFFICULTY_HARD = 2
DIFFICULTIES = [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD]
DIFFICULTIES_AS_NAMES = ["easy", "medium", "hard"]

ROOM_NAME = 0
ROOM_MAX_PLAYER_COUNT = 1
ROOM_PLAYER_COUNT = 2
ROOM_AI_PLAYER_COUNT = 3
ROOM_DIFFICULTY = 4
ROOM_TYPE = 5
ROOM_ID = 6
