import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, BROWN

class Health_Bar:
    def __init__(self,player):
        
        
        self.player = player

        self.width = self.player.width * 1.5
        self.height = 10

        self.health = self.player.health
        self.max_health = self.player.max_health

        self.padding = 15

        self.x = self.player.x
        self.y = self.player.y

    def draw(self, screen):
        # Draw the health bar
        pygame.draw.rect(screen, BLUE, (self.x , self.y - self.padding, self.width, self.height))
        pygame.draw.rect(screen, BROWN, (self.x , self.y - self.padding, self.width * (self.health / self.max_health), self.height))

    def update(self):
        self.x = self.player.x
        self.y = self.player.y

        self.x -= (self.width - self.player.width) / 2
