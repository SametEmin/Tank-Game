import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, RED, BROWN, WHITE

class Item:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

     