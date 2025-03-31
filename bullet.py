import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, RED, BROWN, WHITE

class Bullet:
    def __init__(self, x, y, width, height, speed, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.acceleration = 0.9
        self.direction = direction # angle in degrees

        self.isEnemy = False
        
    def update(self):
        self.x += self.speed * math.cos(math.radians(self.direction))
        self.y += self.speed * math.sin(math.radians(self.direction))

    def draw(self, screen):
        # draw if it is in the screen
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
    def collide(self, enemy):
        # use colliderect() to check for collision
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height))

