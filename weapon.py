import math
import pygame
from bullet import Bullet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, RED, WHITE , GRAY

class Weapon:
    def __init__(self, x, y, width, player):
        self.x = x
        self.y = y
        self.width = width
        self.player = player
        self.bullets = []
        self.cooldown = 0
        self.shape = pygame.Rect(self.x, self.y, self.width, self.width)
        self.angle = 0
        self.is_player = False
        self.is_enemy = False
        self.target = None


    def update(self):
        self.cooldown -= 1
        for i in range(len(self.bullets) - 1, -1, -1):  # Iterate in reverse
            self.bullets[i].update()
            if self.bullets[i].x < 0 or self.bullets[i].x > SCREEN_WIDTH or self.bullets[i].y < 0 or self.bullets[i].y > SCREEN_HEIGHT:
                self.bullets.pop(i)

        # set weapon position as circle around player
        self.x = self.player.x + self.player.width // 2 - self.width // 2 
        self.y = self.player.y + self.player.height // 2 - self.width // 2

        if self.is_player:
            self.angle = self.calculate_angle(self.x + self.width // 2, self.y + self.width // 2,pygame.mouse.get_pos())
        elif self.is_enemy:
            self.angle = self.calculate_angle(self.x + self.width // 2, self.y + self.width // 2, (self.player.target.x + self.player.target.width // 2, self.player.target.y + self.player.target.height // 2))
    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
        self.shape = pygame.Rect(self.x, self.y, self.width, self.width)
        #pygame.draw.rect(screen, GRAY, self.shape)

        # draw line from player to mouse with opacity 0.5
        if self.is_player:
            pygame.draw.line(screen, GRAY, (self.player.x + self.player.width // 2, self.player.y + self.player.height // 2), pygame.mouse.get_pos(), 1)    
 
        weapon_surface = pygame.Surface((self.width, self.width), pygame.SRCALPHA)

        # read Head of weapon
        pygame.draw.rect(weapon_surface, RED, (0, 0, self.width, self.width))

        # rotate weapon image
        rotated_surface = pygame.transform.rotate(weapon_surface, -self.angle)
        # get rect of rotated image
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.width // 2, self.y + self.width // 2))
        # draw rotated image
        screen.blit(rotated_surface, rotated_rect)

        
        tail = pygame.Rect(self.x + self.width // 2 - 5, self.y + self.width // 2 - 5, 10, 10)

        tail_surface = pygame.Surface((10, 90), pygame.SRCALPHA)
        pygame.draw.rect(tail_surface, GRAY,(0, 0, 10, 30) )
        rotated_tail = pygame.transform.rotate(tail_surface, -self.angle - 90)
        rotated_tail_rect = rotated_tail.get_rect(center=(self.x + self.width // 2, self.y + self.width // 2))
        screen.blit(rotated_tail, rotated_tail_rect)

        
    def shoot(self, angle):
        if self.cooldown <= 0:
            bullet = Bullet(self.x + self.width // 2, self.y + self.width // 2, 10, 10, 10, angle)
            if self.is_enemy:
                bullet.isEnemy = True
            self.bullets.append(bullet)
            self.cooldown = 30
    def shoot_from_player(self):
        bullet = Bullet(self.x + self.width // 2, self.y + self.width // 2, 10, 10, 10, self.angle)
        bullet.isPlayer = True
        self.bullets.append(bullet)

    def calculate_angle(self,x,y ,mouse_pos):
        dx = mouse_pos[0] - x
        dy = mouse_pos[1] - y
        return math.degrees(math.atan2(dy, dx))