import pygame
import numpy as np
from game.player import Player
from game.world import World
from game.ui import UI
from game.npc import NPCManager
from game.vehicles import VehicleManager
from game.missions import MissionManager

class Game:
    def __init__(self):
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Window GTA - Open World Game")
        
        # Initialize game components
        self.world = World(self.WIDTH, self.HEIGHT)
        self.player = Player(self.WIDTH // 2, self.HEIGHT // 2)
        self.npc_manager = NPCManager()
        self.vehicle_manager = VehicleManager()
        self.mission_manager = MissionManager()
        self.ui = UI()
        
        self.running = True
        self.paused = False
        self.game_time = 0
        
        # Spawn initial NPCs and vehicles
        self.npc_manager.spawn_npcs(5)
        self.vehicle_manager.spawn_vehicles(3)
        self.mission_manager.generate_missions()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_m:
                    self.mission_manager.accept_random_mission()
                elif event.key == pygame.K_c:
                    self.player.enter_vehicle(self.vehicle_manager.get_nearest_vehicle(self.player.x, self.player.y))
    
    def update(self):
        if not self.paused:
            self.game_time += 1
            
            # Update player
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.world)
            
            # Update NPCs
            self.npc_manager.update(self.world)
            
            # Update vehicles
            self.vehicle_manager.update()
            
            # Update missions
            self.mission_manager.update(self.player)
            
            # Check collisions
            self.check_collisions()
    
    def check_collisions(self):
        # Check vehicle collisions with NPCs
        if self.player.in_vehicle and self.player.vehicle:
            for npc in self.npc_manager.npcs:
                if self.check_rect_collision(self.player.vehicle.get_rect(), npc.get_rect()):
                    npc.damage(10)
                    self.player.money += 5
    
    def check_rect_collision(self, rect1, rect2):
        return rect1.colliderect(rect2)
    
    def draw(self):
        self.screen.fill((100, 150, 100))  # Green background
        
        # Draw world
        self.world.draw(self.screen)
        
        # Draw vehicles
        self.vehicle_manager.draw(self.screen)
        
        # Draw NPCs
        self.npc_manager.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.ui.draw(self.screen, self.player, self.mission_manager, self.game_time)
        
        # Draw pause menu
        if self.paused:
            self.draw_pause_menu()
        
        pygame.display.flip()
    
    def draw_pause_menu(self):
        font = pygame.font.Font(None, 36)
        text = font.render("PAUSED - Press ESC to Resume", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        
        # Draw semi-transparent background
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text, text_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
