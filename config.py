from panda3d.core import BitMask32

class GAME_CONSTANTS:
   PLAYER_MOVEMENT_SPEED = 15
   PLAYER_MAX_HP = 5
   SAMPLE_ENEMY_MAX_HP = 3
   BULLET_SPEED = 40 
   BULLET_MAX_DISTANCE = 30
   PLAYER_DASH_COOLDOWN = 1
   PLAYER_DASH_SPEED = 100 
   PLAYER_DASH_DURATION = 0.2
   BLACK_HOLE_RANGE = 10
   BLACK_HOLE_DURATION = 2
   BLACK_HOLE_PULL_SPEED_MODIFIER = 5
   BLACK_HOLE_COOLDOWN = 5
   BLACK_HOLE_TANK_PULL_FACTOR = 0.5
   BOSS_HP = 75
   ENEMY_MOVEMENT_SPEED = 6
   BOSS_MOVEMENT_SPEED = 14
   BOSS_RANGED_ATTACK_COOLDOWN = 0.3
   BOSS_MELEE_ATTACK_COOLDOWN = 1
   
class PLAYER_ABILITIES:
   DASH = "dash"
   BLACK_HOLE = "black_hole"
   
class GAME_CONFIG:
   DEFAULT_WINDOW_HEIGHT = 720 
   DEFAULT_WINDOW_WIDTH = 1280

class GAME_STATUS:
   MAIN_MENU = "main_menu"
   LOADING_LEVEL = "loading_level"
   PAUSED = "paused"
   RUNNING = "running"
   STARTING = "starting"
   SETTINGS = "settings"
   GAME_FINISH = "game_finish'"
   
class MAP_CONSTANTS:
   ROOM_SIZE = 24
   ROOM_HEIGHT = 5
   MAP_LENGTH = 11
   ROOM_TYPES = 16
   
class ENTITY_TEAMS:
   PLAYER = "player"
   PLAYER_BITMASK = BitMask32(0x01)
   ENEMIES = "enemies"
   ENEMIES_BITMASK = BitMask32(0x02)
   MAP = "map"
   MAP_BITMASK = BitMask32(0x03)
   ABILITY = "ability"
   ABILITY_BITMASK = BitMask32(0x04)
   MELEE_ATTACK_BITMASK = BitMask32(0x08)
   ROOM = "room"
   ROOM_BITMASK = BitMask32(0x08)