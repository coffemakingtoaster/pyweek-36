from panda3d.core import BitMask32

class GAME_CONSTANTS:
   PLAYER_MOVEMENT_SPEED = 15
   PLAYER_MAX_HP = 5
   SAMPLE_ENEMY_MAX_HP = 1
   BULLET_SPEED = 40 
   BULLET_MAX_DISTANCE = 30
   PLAYER_DASH_COOLDOWN = 1
   PLAYER_DASH_SPEED = 100 
   PLAYER_DASH_DURATION = 0.2
   
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
   
class MAP_CONSTANTS:
   ROOM_SIZE = 24
   ROOM_HEIGHT = 5
   MAP_LENGTH = 15
   ROOM_TYPES = 3
   
class ENTITY_TEAMS:
   PLAYER = "player"
   PLAYER_BITMASK = BitMask32(0x01)
   ENEMIES = "enemies"
   ENEMIES_BITMASK = BitMask32(0x02)
   MAP = "map"
   MAP_BITMASK = BitMask32(0x03)