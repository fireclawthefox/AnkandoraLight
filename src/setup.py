from setuptools import setup

setup(
    options={
        'build_apps': {
            'package_data_dirs': {
                'simplepbr': [
                    ('simplepbr/*.vert', '', {}),
                    ('simplepbr/*.frag', '', {}),
                ]
            },
            'include_modules': {
                "Ankandora": [
                    "direct.particles.ParticleManagerGlobal",

                    "chat.DMessage.DMessage",
                    "roomManager.DRoomManager.DRoomManager",
                    "board.DBoard.DBoard",
                    "questCard.DQuestCard.DQuestCard",
                    "room.DRoom.DRoom",
                    "player.DBotPlayer.DBotPlayer",
                    "player.DPlayer.DPlayer",
                    "piece.DPiece.DPiece",
                    "battle.DBattle.DBattle",
                    "roomManager.DRoomManagerAI.DRoomManagerAI",
                    "board.DBoardAI.DBoardAI",
                    "questCard.DQuestCardAI.DQuestCardAI",
                    "room.DRoomAI.DRoomAI",
                    "player.DBotPlayerAI.DBotPlayerAI",
                    "player.DPlayerAI.DPlayerAI",
                    "piece.DPieceAI.DPieceAI",
                    "battle.DBattleAI.DBattleAI",

                    "direct.distributed.DistributedObject",
                    "direct.distributed.TimeManager",
                    "direct.distributed.DistributedNode",
                    "direct.distributed.DistributedSmoothNode",
                    "direct.distributed.DistributedObjectAI",
                    "direct.distributed.TimeManagerAI",
                    "direct.distributed.DistributedNodeAI",
                    "direct.distributed.DistributedSmoothNodeAI",
                ]
            }
        }
    }
)
