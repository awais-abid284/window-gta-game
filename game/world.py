import pygame
import random

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buildings = self.generate_buildings()
        self.roads = self.generate_roads()
        self.water = self.generate_water()
        self.trees = self.generate_trees()
    
    def generate_buildings(self):
        buildings = []
        # Create a grid of buildings
        for i in range(0, self.width, 200):
            for j in range(0, self.height, 200):
                if random.random() > 0.3:  # 70% chance of building
                    width = random.randint(80, 120)
                    height = random.randint(80, 120)
                    buildings.append({
                        'x': i + random.randint(0, 50),
                        'y': j + random.randint(0, 50),
                        'width': width,
                        'height': height,
                        'color': (random.randint(100, 180), random.randint(100, 180), random.randint(100, 180)),
                        'type': random.choice(['office', 'residential', 'shop'])
                    })
        return buildings
    
    def generate_roads(self):
        roads = []
        # Horizontal roads
        for y in range(0, self.height, 150):
            roads.append({
                'x': 0,
                'y': y,
                'width': self.width,
                'height': 30,
                'type': 'horizontal'
            })
        # Vertical roads
        for x in range(0, self.width, 150):
            roads.append({
                'x': x,
                'y': 0,
                'width': 30,
                'height': self.height,
                'type': 'vertical'
            })
        return roads
    
    def generate_water(self):
        water = []
        # Random water bodies
        for _ in range(3):
            water.append({
                'x': random.randint(0, self.width - 100),
                'y': random.randint(0, self.height - 100),
                'width': random.randint(80, 150),
                'height': random.randint(80, 150)
            })
        return water
    
    def generate_trees(self):
        trees = []
        for _ in range(20):
            trees.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'radius': random.randint(5, 10)
            })
        return trees
    
    def draw(self, screen):
        # Draw water
        for water in self.water:
            pygame.draw.rect(screen, (0, 100, 200), (water['x'], water['y'], water['width'], water['height']))
        
        # Draw roads
        for road in self.roads:
            pygame.draw.rect(screen, (64, 64, 64), (road['x'], road['y'], road['width'], road['height']))
            # Draw road markings
            if road['type'] == 'horizontal':
                for x in range(0, self.width, 40):
                    pygame.draw.line(screen, (255, 255, 0), (x, road['y'] + 15), (x + 20, road['y'] + 15), 2)
            else:
                for y in range(0, self.height, 40):
                    pygame.draw.line(screen, (255, 255, 0), (road['x'] + 15, y), (road['x'] + 15, y + 20), 2)
        
        # Draw buildings
        for building in self.buildings:
            pygame.draw.rect(screen, building['color'], (building['x'], building['y'], building['width'], building['height']))
            # Draw building outline
            pygame.draw.rect(screen, (0, 0, 0), (building['x'], building['y'], building['width'], building['height']), 2)
            # Draw windows
            for wx in range(building['x'], building['x'] + building['width'], 15):
                for wy in range(building['y'], building['y'] + building['height'], 15):
                    pygame.draw.rect(screen, (255, 255, 100), (wx, wy, 8, 8))
        
        # Draw trees
        for tree in self.trees:
            pygame.draw.circle(screen, (34, 139, 34), (tree['x'], tree['y']), tree['radius'])
            pygame.draw.line(screen, (139, 69, 19), (tree['x'], tree['y']), (tree['x'], tree['y'] + tree['radius']), 2)
    
    def is_walkable(self, x, y, width, height):
        # Check if position collides with buildings
        rect = pygame.Rect(x, y, width, height)
        for building in self.buildings:
            building_rect = pygame.Rect(building['x'], building['y'], building['width'], building['height'])
            if rect.colliderect(building_rect):
                return False
        return True
