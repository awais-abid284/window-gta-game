import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.health = 100
        self.max_health = 100
        self.money = 0
        self.level = 1
        self.experience = 0
        self.in_vehicle = False
        self.vehicle = None
        self.direction = "down"
        self.color = (255, 0, 0)  # Red
        self.animation_frame = 0
    
    def update(self, keys, world):
        # Movement input
        self.velocity_x = 0
        self.velocity_y = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -self.speed
            self.direction = "up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = self.speed
            self.direction = "down"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.direction = "right"
        
        # Apply velocity
        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y
        
        # Boundary checking
        if 0 <= new_x <= world.width - self.width:
            self.x = new_x
        if 0 <= new_y <= world.height - self.height:
            self.y = new_y
        
        # Animation
        self.animation_frame = (self.animation_frame + 1) % 60
        
        # Natural health regeneration
        if self.health < self.max_health:
            self.health = min(self.max_health, self.health + 0.05)
    
    def draw(self, screen):
        if self.in_vehicle:
            # Don't draw player when in vehicle (vehicle draws it)
            return
        
        # Draw player body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw head
        pygame.draw.circle(screen, (255, 200, 100), (int(self.x + self.width // 2), int(self.y - 5)), 5)
        
        # Draw health bar above player
        health_bar_width = self.width
        health_bar_height = 3
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, health_bar_width * health_percentage, health_bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.respawn()
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def add_money(self, amount):
        self.money += amount
    
    def add_experience(self, amount):
        self.experience += amount
        if self.experience >= 100 * self.level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 10
        self.health = self.max_health
        self.speed += 0.5
    
    def enter_vehicle(self, vehicle):
        if vehicle:
            self.in_vehicle = True
            self.vehicle = vehicle
            vehicle.set_player(self)
    
    def exit_vehicle(self):
        if self.vehicle:
            self.x = self.vehicle.x + self.vehicle.width
            self.y = self.vehicle.y + self.vehicle.height
            self.vehicle.set_player(None)
            self.in_vehicle = False
            self.vehicle = None
    
    def respawn(self):
        self.x = 100
        self.y = 100
        self.health = self.max_health
        self.money = max(0, self.money - 50)  # Lose money on death
