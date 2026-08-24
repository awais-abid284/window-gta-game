import pygame
import random
import math

class NPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.speed = random.uniform(1, 2)
        self.velocity_x = 0
        self.velocity_y = 0
        self.health = 100
        self.max_health = 100
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.state = 'idle'  # idle, walking, talking, attacking
        self.state_timer = random.randint(30, 180)
        self.target_x = x
        self.target_y = y
        self.name = random.choice(['Alex', 'Jordan', 'Casey', 'Morgan', 'Riley', 'Taylor'])
        self.mood = random.choice(['happy', 'neutral', 'angry'])
        self.ai_type = random.choice(['patrol', 'wander', 'follow'])
    
    def update(self, world):
        self.state_timer -= 1
        
        if self.state == 'idle':
            if self.state_timer <= 0:
                self.state = 'walking'
                self.state_timer = random.randint(60, 240)
                self.target_x = random.randint(0, world.width)
                self.target_y = random.randint(0, world.height)
        
        elif self.state == 'walking':
            # Move towards target
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 5:
                self.velocity_x = (dx / distance) * self.speed
                self.velocity_y = (dy / distance) * self.speed
            else:
                self.velocity_x = 0
                self.velocity_y = 0
                self.state = 'idle'
                self.state_timer = random.randint(30, 180)
            
            # Update position
            new_x = self.x + self.velocity_x
            new_y = self.y + self.velocity_y
            
            # Boundary checking
            if 0 <= new_x <= world.width - self.width:
                self.x = new_x
            if 0 <= new_y <= world.height - self.height:
                self.y = new_y
    
    def draw(self, screen):
        # Draw NPC body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw head
        pygame.draw.circle(screen, (255, 200, 100), (int(self.x + self.width // 2), int(self.y - 5)), 5)
        
        # Draw health bar
        if self.health < self.max_health:
            health_bar_width = self.width
            health_bar_height = 3
            health_percentage = self.health / self.max_health
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, health_bar_width * health_percentage, health_bar_height))
        
        # Draw mood indicator
        mood_color = (255, 255, 0) if self.mood == 'happy' else (100, 100, 100) if self.mood == 'neutral' else (255, 0, 0)
        pygame.draw.circle(screen, mood_color, (int(self.x + self.width // 2), int(self.y - 15)), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def damage(self, amount):
        self.health = max(0, self.health - amount)
        self.mood = 'angry'
        if self.health <= 0:
            self.die()
    
    def die(self):
        self.state = 'dead'
    
    def interact(self, player):
        if self.mood == 'happy':
            return f"{self.name} gives you $50"
        elif self.mood == 'angry':
            return f"{self.name} attacks you!"
        else:
            return f"{self.name}: Hello..."

class NPCManager:
    def __init__(self):
        self.npcs = []
    
    def spawn_npcs(self, count):
        for _ in range(count):
            x = random.randint(0, 1200)
            y = random.randint(0, 650)
            self.npcs.append(NPC(x, y))
    
    def update(self, world):
        for npc in self.npcs:
            npc.update(world)
    
    def draw(self, screen):
        for npc in self.npcs:
            if npc.state != 'dead':
                npc.draw(screen)
    
    def get_npcs_in_range(self, x, y, range_distance):
        nearby_npcs = []
        for npc in self.npcs:
            distance = math.sqrt((npc.x - x)**2 + (npc.y - y)**2)
            if distance < range_distance:
                nearby_npcs.append(npc)
        return nearby_npcs
