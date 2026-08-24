import random
import math

class Mission:
    def __init__(self, mission_id):
        self.id = mission_id
        self.title = random.choice([
            "Steal the Package",
            "Deliver the Goods",
            "Eliminate the Target",
            "Rescue the Hostage",
            "Rob the Store",
            "Race to the Finish",
            "Defend the Base",
            "Retrieve the Item"
        ])
        self.description = f"Complete mission: {self.title}"
        self.reward = random.randint(100, 500)
        self.difficulty = random.choice(['Easy', 'Medium', 'Hard'])
        self.target_x = random.randint(0, 1200)
        self.target_y = random.randint(0, 650)
        self.target_radius = 50
        self.time_limit = random.randint(60, 300)
        self.time_remaining = self.time_limit
        self.completed = False
        self.failed = False
        self.objective_description = self.generate_objective()
    
    def generate_objective(self):
        objectives = [
            f"Go to location ({self.target_x}, {self.target_y})",
            f"Collect item at ({self.target_x}, {self.target_y})",
            f"Reach checkpoint at ({self.target_x}, {self.target_y})",
            f"Find target within {self.time_limit} seconds"
        ]
        return random.choice(objectives)
    
    def update(self, player):
        if self.completed or self.failed:
            return
        
        self.time_remaining -= 1
        
        if self.time_remaining <= 0:
            self.failed = True
            return
        
        # Check if player reached target
        distance = math.sqrt((player.x - self.target_x)**2 + (player.y - self.target_y)**2)
        if distance < self.target_radius:
            self.completed = True
    
    def draw_marker(self, screen):
        if not self.completed and not self.failed:
            # Draw target marker
            import pygame
            pygame.draw.circle(screen, (255, 0, 0), (self.target_x, self.target_y), self.target_radius, 2)
            pygame.draw.line(screen, (255, 0, 0), 
                           (self.target_x - 10, self.target_y), 
                           (self.target_x + 10, self.target_y), 2)
            pygame.draw.line(screen, (255, 0, 0), 
                           (self.target_x, self.target_y - 10), 
                           (self.target_x, self.target_y + 10), 2)

class MissionManager:
    def __init__(self):
        self.missions = []
        self.active_mission = None
        self.completed_missions = 0
        self.total_mission_rewards = 0
    
    def generate_missions(self, count=5):
        for i in range(count):
            self.missions.append(Mission(i))
    
    def accept_random_mission(self):
        available_missions = [m for m in self.missions if not m.completed and not m.failed]
        if available_missions:
            self.active_mission = random.choice(available_missions)
            return f"Mission Accepted: {self.active_mission.title}"
        return "No missions available"
    
    def accept_mission(self, mission_id):
        for mission in self.missions:
            if mission.id == mission_id and not mission.completed and not mission.failed:
                self.active_mission = mission
                return f"Mission Accepted: {mission.title}"
        return "Mission not found"
    
    def update(self, player):
        if self.active_mission:
            self.active_mission.update(player)
            
            if self.active_mission.completed:
                player.add_money(self.active_mission.reward)
                player.add_experience(self.active_mission.reward // 2)
                self.completed_missions += 1
                self.total_mission_rewards += self.active_mission.reward
                self.active_mission = None
            
            elif self.active_mission.failed:
                player.damage(25)
                self.active_mission = None
    
    def get_active_mission_info(self):
        if self.active_mission:
            return {
                'title': self.active_mission.title,
                'description': self.active_mission.objective_description,
                'reward': self.active_mission.reward,
                'time_remaining': self.active_mission.time_remaining,
                'difficulty': self.active_mission.difficulty
            }
        return None
    
    def draw_mission_markers(self, screen):
        if self.active_mission:
            self.active_mission.draw_marker(screen)
