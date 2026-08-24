import pygame

class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def draw(self, screen, player, mission_manager, game_time):
        # Draw HUD background
        hud_height = 120
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), hud_height))
        pygame.draw.rect(screen, (100, 100, 100), (0, 0, screen.get_width(), hud_height), 2)
        
        # Draw player stats
        stats_text = [
            f"Health: {int(player.health)}/{int(player.max_health)}",
            f"Money: ${player.money}",
            f"Level: {player.level} (XP: {player.experience})",
            f"Time: {game_time // 60}s"
        ]
        
        y_offset = 10
        for stat in stats_text:
            text = self.font_small.render(stat, True, (255, 255, 255))
            screen.blit(text, (10, y_offset))
            y_offset += 25
        
        # Draw mission info
        mission_info = mission_manager.get_active_mission_info()
        if mission_info:
            mission_x = screen.get_width() - 400
            mission_bg = pygame.Surface((390, hud_height - 10))
            mission_bg.set_alpha(200)
            mission_bg.fill((50, 50, 100))
            screen.blit(mission_bg, (mission_x, 5))
            
            mission_title = self.font_medium.render(f"Mission: {mission_info['title']}", True, (255, 200, 0))
            mission_reward = self.font_small.render(f"Reward: ${mission_info['reward']}", True, (0, 255, 0))
            mission_time = self.font_small.render(f"Time: {mission_info['time_remaining']}s", True, (255, 100, 0))
            mission_difficulty = self.font_small.render(f"Difficulty: {mission_info['difficulty']}", True, (255, 255, 100))
            
            screen.blit(mission_title, (mission_x + 10, 10))
            screen.blit(mission_reward, (mission_x + 10, 40))
            screen.blit(mission_time, (mission_x + 10, 65))
            screen.blit(mission_difficulty, (mission_x + 10, 90))
        
        # Draw controls info at bottom
        controls_y = screen.get_height() - 30
        controls_text = "W/A/S/D or Arrow Keys: Move | C: Enter Vehicle | M: Accept Mission | ESC: Pause"
        controls = self.font_small.render(controls_text, True, (200, 200, 200))
        screen.blit(controls, (10, controls_y))
        
        # Draw vehicle info if in vehicle
        if player.in_vehicle and player.vehicle:
            vehicle_info_x = 10
            vehicle_info_y = screen.get_height() - 80
            
            vehicle_bg = pygame.Surface((300, 60))
            vehicle_bg.set_alpha(200)
            vehicle_bg.fill((50, 50, 50))
            screen.blit(vehicle_bg, (vehicle_info_x, vehicle_info_y))
            
            vehicle_health = self.font_small.render(f"Vehicle Health: {int(player.vehicle.health)}", True, (255, 100, 100))
            vehicle_fuel = self.font_small.render(f"Fuel: {int(player.vehicle.fuel)}", True, (255, 200, 0))
            vehicle_speed = self.font_small.render(f"Speed: {player.vehicle.speed:.1f}", True, (100, 200, 255))
            
            screen.blit(vehicle_health, (vehicle_info_x + 10, vehicle_info_y + 5))
            screen.blit(vehicle_fuel, (vehicle_info_x + 10, vehicle_info_y + 25))
            screen.blit(vehicle_speed, (vehicle_info_x + 10, vehicle_info_y + 45))
    
    def draw_death_screen(self, screen):
        font = pygame.font.Font(None, 72)
        text = font.render("YOU DIED", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(text, text_rect)
    
    def draw_mission_complete(self, screen, reward):
        font = pygame.font.Font(None, 48)
        text = font.render(f"Mission Complete! +${reward}", True, (0, 255, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text, text_rect)
    
    def draw_minimap(self, screen, player, npcs, vehicles):
        minimap_width = 150
        minimap_height = 150
        minimap_x = screen.get_width() - minimap_width - 10
        minimap_y = 130
        
        # Draw minimap background
        pygame.draw.rect(screen, (0, 0, 0), (minimap_x, minimap_y, minimap_width, minimap_height))
        pygame.draw.rect(screen, (100, 100, 100), (minimap_x, minimap_y, minimap_width, minimap_height), 2)
        
        # Scale factor
        scale_x = minimap_width / screen.get_width()
        scale_y = minimap_height / screen.get_height()
        
        # Draw player on minimap
        player_mini_x = minimap_x + player.x * scale_x
        player_mini_y = minimap_y + player.y * scale_y
        pygame.draw.circle(screen, (0, 255, 0), (int(player_mini_x), int(player_mini_y)), 3)
        
        # Draw NPCs on minimap
        for npc in npcs:
            npc_mini_x = minimap_x + npc.x * scale_x
            npc_mini_y = minimap_y + npc.y * scale_y
            pygame.draw.circle(screen, (255, 0, 0), (int(npc_mini_x), int(npc_mini_y)), 2)
        
        # Draw vehicles on minimap
        for vehicle in vehicles:
            vehicle_mini_x = minimap_x + vehicle.x * scale_x
            vehicle_mini_y = minimap_y + vehicle.y * scale_y
            pygame.draw.circle(screen, (255, 255, 0), (int(vehicle_mini_x), int(vehicle_mini_y)), 2)
