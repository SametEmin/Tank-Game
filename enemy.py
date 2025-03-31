import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, BROWN
import random

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.acceleration = 0.9
        self.spd_per_frame_x = speed * random.random()
        self.spd_per_frame_y = speed * random.random()

    def update(self):
        
        self.normalize_speed()
        self.update_position()

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))

    def collide(self, player):
        # use colliderect() to check for collision
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(pygame.Rect(player.x, player.y, player.width, player.height))
   
    def normalize_speed(self):
        # Normalize speed if it exceeds the maximum
        if abs(self.spd_per_frame_x) > self.speed/ (2**0.5) and abs(self.spd_per_frame_y) > self.speed/ (2**0.5):
            self.spd_per_frame_x = self.speed/ 2**0.5 * self.spd_per_frame_x/ abs(self.spd_per_frame_x)
            self.spd_per_frame_y = self.speed/ 2**0.5 * self.spd_per_frame_y/ abs(self.spd_per_frame_y)

    def update_position(self):
        # Update position based on speed
        if 0 <= self.x + self.spd_per_frame_x <= SCREEN_WIDTH - self.width:
            self.x += self.spd_per_frame_x

        if 0 <= self.y + self.spd_per_frame_y <= SCREEN_HEIGHT - self.height:
            self.y += self.spd_per_frame_y

        if self.x + self.spd_per_frame_x < 0 or self.x + self.spd_per_frame_x > SCREEN_WIDTH - self.width:
            self.spd_per_frame_x = -self.spd_per_frame_x

        if self.y + self.spd_per_frame_y < 0 or self.y + self.spd_per_frame_y > SCREEN_HEIGHT - self.height:
            self.spd_per_frame_y = -self.spd_per_frame_y

