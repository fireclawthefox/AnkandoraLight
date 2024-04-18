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
                    "direct.showbase.PhysicsManagerGlobal",

                    "chat.DMessage",
                    "roomManager.DRoomManager",
                    "board.DBoard",
                    "questCard.DQuestCard",
                    "room.DRoom",
                    "player.DBotPlayer",
                    "player.DPlayer",
                    "piece.DPiece",
                    "battle.DBattle",
                    "roomManager.DRoomManagerAI",
                    "board.DBoardAI",
                    "questCard.DQuestCardAI",
                    "room.DRoomAI",
                    "player.DBotPlayerAI",
                    "player.DPlayerAI",
                    "piece.DPieceAI",
                    "battle.DBattleAI",

                    "direct.distributed.DistributedObject",
                    "direct.distributed.TimeManager",
                    "direct.distributed.DistributedNode",
                    "direct.distributed.DistributedSmoothNode",
                    "direct.distributed.DistributedObjectAI",
                    "direct.distributed.TimeManagerAI",
                    "direct.distributed.DistributedNodeAI",
                    "direct.distributed.DistributedSmoothNodeAI"
                ]
            }
        }
    }
)
