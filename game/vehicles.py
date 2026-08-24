import pygame
import random
import math

class Vehicle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.speed = random.uniform(2, 4)
        self.max_speed = self.speed + 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.health = 100
        self.max_health = 100
        self.fuel = 100
        self.max_fuel = 100
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.vehicle_type = random.choice(['car', 'truck', 'sports'])
        self.rotation = 0
        self.player = None
        self.state = 'idle'  # idle, moving, crashed
        self.target_x = x
        self.target_y = y
    
    def update(self):
        # Consume fuel
        if self.state == 'moving':
            self.fuel = max(0, self.fuel - 0.1)
        
        # AI driving
        if not self.player:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 10:
                self.velocity_x = (dx / distance) * self.speed
                self.velocity_y = (dy / distance) * self.speed
                self.state = 'moving'
            else:
                self.velocity_x = 0
                self.velocity_y = 0
                self.state = 'idle'
                # Pick new target
                if random.random() > 0.9:
                    self.target_x = random.randint(0, 1200)
                    self.target_y = random.randint(0, 650)
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Boundary checking
        if self.x < 0:
            self.x = 0
            self.velocity_x = 0
        elif self.x > 1280 - self.width:
            self.x = 1280 - self.width
            self.velocity_x = 0
        
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        elif self.y > 720 - self.height:
            self.y = 720 - self.height
            self.velocity_y = 0
        
        # Rotation based on velocity
        if self.velocity_x != 0 or self.velocity_y != 0:
            self.rotation = math.degrees(math.atan2(self.velocity_y, self.velocity_x))
    
    def draw(self, screen):
        # Draw vehicle body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw vehicle outline
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        
        # Draw windows
        pygame.draw.rect(screen, (100, 150, 255), (self.x + 5, self.y + 5, 12, 8))
        pygame.draw.rect(screen, (100, 150, 255), (self.x + 33, self.y + 5, 12, 8))
        
        # Draw wheels
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 10), int(self.y + self.height)), 5)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + self.width - 10), int(self.y + self.height)), 5)
        
        # Draw health bar
        if self.health < self.max_health:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, self.width, 3))
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, self.width * (self.health / self.max_health), 3))
        
        # Draw fuel indicator
        pygame.draw.rect(screen, (255, 100, 0), (self.x, self.y - 5, self.width, 2))
        pygame.draw.rect(screen, (255, 200, 0), (self.x, self.y - 5, self.width * (self.fuel / self.max_fuel), 2))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.state = 'crashed'
    
    def refuel(self, amount=None):
        if amount is None:
            amount = self.max_fuel
        self.fuel = min(self.max_fuel, self.fuel + amount)
    
    def repair(self, amount=None):
        if amount is None:
            amount = self.max_health
        self.health = min(self.max_health, self.health + amount)
    
    def accelerate(self):
        self.speed = min(self.max_speed, self.speed + 0.5)
    
    def brake(self):
        self.speed = max(0, self.speed - 0.5)
        self.velocity_x *= 0.9
        self.velocity_y *= 0.9
    
    def set_player(self, player):
        self.player = player
        if player:
            self.state = 'moving'

class VehicleManager:
    def __init__(self):
        self.vehicles = []
    
    def spawn_vehicles(self, count):
        for _ in range(count):
            x = random.randint(0, 1200)
            y = random.randint(0, 650)
            self.vehicles.append(Vehicle(x, y))
    
    def update(self):
        for vehicle in self.vehicles:
            vehicle.update()
    
    def draw(self, screen):
        for vehicle in self.vehicles:
            if vehicle.state != 'crashed':
                vehicle.draw(screen)
    
    def get_nearest_vehicle(self, x, y):
        nearest = None
        min_distance = float('inf')
        
        for vehicle in self.vehicles:
            distance = math.sqrt((vehicle.x - x)**2 + (vehicle.y - y)**2)
            if distance < min_distance and distance < 100:
                min_distance = distance
                nearest = vehicle
        
        return nearest
