from panda3d.core import loadPrcFile, CollisionHandlerEvent, CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionSphere, CollisionNode, CollisionTube
from ui.main_menu import main_menu
from ui.pause_menu import pause_menu
from ui.settings_menu import settings_menu
from ui.victory_screen import victory_screen
from ui.hud import game_hud 
from config import GAME_STATUS, GAME_CONSTANTS, GAME_CONFIG, ENTITY_TEAMS
from helpers.utilities import load_config, save_config, lock_mouse_in_window, release_mouse_from_window
from entities.player import player_entity
from entities.sample_enemy import sample_enemy_entity
from entities.melee_enemy import melee_enemy
from entities.ranged_enemy import ranged_enemy

from entities.tank_enemy import tank_enemy

from panda3d.core import WindowProperties
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib, PointLight
from panda3d.core import LPoint3, LVector3, BitMask32

from direct.gui.DirectGui import OnscreenImage

from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from entities.enemy_actor import enemy_actor

from direct.actor.Actor import Actor

from os.path import join
from mapGen import MapLoader

# Load panda3d configfile that disables model caching
loadPrcFile("./settings.prc")

class main_game(ShowBase):
    def __init__(self):
        
        ShowBase.__init__(self)
        
        print(ENTITY_TEAMS.MAP_BITMASK)
        print(ENTITY_TEAMS.ENEMIES_BITMASK)
        print(ENTITY_TEAMS.PLAYER_BITMASK)
        
        # Set camera position 
        base.cam.setPos(0, 50, 0) 
        base.cam.setHpr(0, 180+40, 0)
        
        self.setupLights()
       
        load_config(join("user_config.json"))

        self.game_status = GAME_STATUS.MAIN_MENU 
        
        # This should be obvious
        base.enableParticles()
        
        self.player = None
        self.currentWave = 0
        self.mapLoader = None
        self.map = []
        self.currentRoomNumber = 0
        self.newestRoomNumber = 0
        self.currentRoom = None
        self.oldRoom = None
        self.loadedRooms = []
        
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        
        self.tempActor = None
        self.entities = []
        self.enemies  = 0
        
        self.current_hud = None
        
        self.static_entities = []

        self.status_display = OnscreenText(text=GAME_STATUS.MAIN_MENU, pos=(0.9,0.9 ), scale=0.07,fg=(255,0,0, 1))

        self.active_ui = None 
        self.goto_to_main_menu()

        # Create event handlers for events fired by UI
        self.accept("start_game", self.set_game_status, [GAME_STATUS.STARTING])

        # Create event handlers for events fired by keyboard
        self.accept("escape", self.toggle_pause)
        
        self.accept("pause_game", self.toggle_pause)

        self.accept("goto_main_menu", self.goto_to_main_menu)
        self.accept("toggle_settings", self.toggle_settings)

        self.gameTask = base.taskMgr.add(self.game_loop, "gameLoop")
        
        self.accept("l", self.enterRoom)
        self.accept("u", self.unloadOldestRoom)
        
        # Load music
        background_music = base.loader.loadMusic(join("assets", "music", "music.mp3")) 
        background_music.setLoop(True)
        background_music.play()
        
        base.disableMouse()
        
        base.cTrav.setRespectPrevTransform(True)
        
        self.current_run_duration = 0
        
        
    def game_loop(self, task):
        
        dt = self.clock.dt 

        if self.game_status == GAME_STATUS.STARTING:
            print("Starting")
            self.set_game_status(GAME_STATUS.LOADING_LEVEL)
            # Move this to task?
            self.load_game()

        # Do not progress game logic if game is not active
        if self.game_status != GAME_STATUS.RUNNING:
           return Task.cont 
       
        self.current_run_duration += dt
       
        self.player.update(dt)
        
        if self.player.is_dead:
            self.finish_game(False)
            return Task.cont
       
        if self.enemies == 0:
            if self.currentWave != 4 and self.currentWave != 0:
                self.spawnWave()
                self.currentWave += 1
            elif self.currentWave == 4:
                self.currentWave = 0
                self.loadNextRoom()
       
        for i, entity in enumerate(self.entities):
            entity.update(dt, self.player.model.getPos())
            if hasattr(entity, "is_dead"):
                if entity.is_dead:
                    entity.destroy()
                    if hasattr(entity, "enemy"):
                        self.enemies -= 1
                        print(self.enemies)
                    del self.entities[i]
                    
        
        return Task.cont
    
    def load_game(self):
        print("Loading game")
        self.current_run_duration = 0
        self.active_ui.destroy()
        self.setBackgroundColor((0, 0, 0, 1))
        self.player = player_entity()
        
        self.pusher.addCollider(self.player.collision, self.player.model)
        self.cTrav.addCollider(self.player.collision,self.pusher)
        self.pusher.setHorizontal(True)
    
        self.active_ui = game_hud()
        
        self.entities.append(melee_enemy(10,10))
        self.pusher.addCollider(self.entities[0].collision, self.entities[0].model)
        self.cTrav.addCollider(self.entities[0].collision, self.pusher)
        self.enemies += 1
        
        lock_mouse_in_window()
        self.mapLoader = MapLoader()
        self.map = self.mapLoader.mapGen()
        self.loadFirstRoom()
        
        
        self.static_entities = self.map 
        self.set_game_status(GAME_STATUS.RUNNING)

    def set_game_status(self, status):
        self.status_display["text"] = status
        self.game_status = status

    def toggle_pause(self):
        if self.game_status == GAME_STATUS.RUNNING:
            self.set_game_status(GAME_STATUS.PAUSED)
            # Not needed as of now as gui does not exist 
            self.current_hud = self.active_ui
            self.current_hud.pause()
            release_mouse_from_window()
            self.active_ui = pause_menu()
        elif self.game_status == GAME_STATUS.PAUSED:
            self.active_ui.destroy()
            self.current_hud.resume()
            self.active_ui = self.current_hud 
            lock_mouse_in_window() 
            self.set_game_status(GAME_STATUS.RUNNING)

    def goto_to_main_menu(self):
        print("Return to main menu")
        self.enemies = 0
        # no hud yet
        if self.active_ui is not None:
            self.active_ui.destroy()
        if self.current_hud is not None:
            self.current_hud.destroy()
            self.current_hud = None
        # delete all entities
        for entity in self.entities:
            entity.destroy()
        self.entities = []
        for static_entity in self.static_entities:
            static_entity.destroy()
        self.static_entities = []
        if self.player is not None:
            self.player.destroy()
            self.player = None
        self.current_run_duration = 0
        self.active_ui = main_menu()
        self.setBackgroundColor((0, 0, 0, 1))
        self.set_game_status(GAME_STATUS.MAIN_MENU)
        
        
    def toggle_settings(self):
        if self.game_status == GAME_STATUS.MAIN_MENU:
            self.active_ui.destroy()
            self.active_ui = settings_menu()
            self.set_game_status(GAME_STATUS.SETTINGS)
        elif self.game_status == GAME_STATUS.SETTINGS:
            self.active_ui.destroy()
            self.active_ui = main_menu() 
            self.set_game_status(GAME_STATUS.MAIN_MENU)
     
    def setupLights(self):  
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.1, .1, .1, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, -45, -45))
        directionalLight.setColor((0.3, 0.3, 0.3, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(ambientLight))
        plight = PointLight('plight')
        plight.setColor((2, 1.2, 0.6, 1))
        plight.attenuation = (1, 0, 0.1)
        plnp = render.attachNewNode(plight)
        plnp.setPos(0, 2, 0)
        render.setLight(plnp)
    
    
    def loadFirstRoom(self):
        
        self.loadedRooms.append(self.mapLoader.loadRoom(self.map[self.newestRoomNumber]))
        self.newestRoomNumber += 1
        self.loadedRooms.append(self.mapLoader.loadRoom(self.map[self.newestRoomNumber]))
        self.currentRoom = self.loadedRooms[self.currentRoomNumber]
        self.enterRoom()
        print("loadingFirstRoom")
        
    def loadNextRoom(self):
        #self.currentRoomNumber += 1
        self.newestRoomNumber += 1
        #self.oldRoom = self.currentRoom
        self.loadedRooms.append(self.mapLoader.loadRoom(self.map[self.newestRoomNumber]))
        
        
        if len(self.loadedRooms) >4:
            self.unloadOldestRoom()
            self.currentRoom = self.loadedRooms[2]
            
        else:
            self.currentRoom = self.loadedRooms[self.currentRoomNumber]
            
        
        self.currentRoom.openDoor()
            
        
        
        
    def enterRoom(self):
        self.spawnWave()
        self.currentWave = 1
        self.currentRoom.closeDoor()
        self.currentRoomNumber += 1
        
        
    
    
    def spawnWave(self):
        for spawner in self.currentRoom.spawners:
            if spawner.wave == self.currentWave:
                spawner.spawn(self.entities)
                self.pusher.addCollider(self.entities[-1].collision, self.entities[-1].model)
                self.cTrav.addCollider(self.entities[-1].collision, self.pusher)
                self.enemies += 1
                

              
    def unloadOldestRoom(self):
        self.mapLoader.unloadRoom(self.loadedRooms[0])
        self.loadedRooms.pop(0)
    
    
        
    def finish_game(self, success: bool):
        self.set_game_status(GAME_STATUS.GAME_FINISH)
        self.active_ui.destroy()
        self.current_hud = None
        self.active_ui = victory_screen(self.current_run_duration, success) 
        
def start_game():
    print("Starting game..")
    game = main_game()
    game.run()

if __name__ == "__main__":
    start_game()
    
    