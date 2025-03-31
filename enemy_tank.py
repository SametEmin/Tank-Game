import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE


class Enemy_Tank:
    def __init__(self, x, y, width, height, speed, game, weapon=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.acceleration = 0.9
        self.spd_per_frame_x = 0
        self.spd_per_frame_y = 0
        self.health = 100
        self.max_health = self.health
        self.game = game
        self.is_invulnerable = False

        self.movement_durations = [random.randint(1, 5) for i in range(4)]

        self.movement_start_times = [0 for i in range(4)]
        self.target = None

        self.weapon = None

        self.last_shoot_time = 0


    def update(self):
        self.handle_movement()
        self.weapon.update()
        self.shoot()

        self.move()

    def handle_movement(self):
        self.go_left()
        self.go_right()
        self.go_up()
        self.go_down()
        self.normalize_speed()
        self.check_collision_wall()


        # Adjust speeds based on key presses
        

    def go_left(self):
        if self.movement_start_times[0] == 0:
            self.movement_start_times[0] = pygame.time.get_ticks()/1000

        if pygame.time.get_ticks()/1000 - self.movement_start_times[0] >= self.movement_durations[0]:
            self.movement_start_times[0] = 0
            return

        if self.spd_per_frame_x <= -self.speed:
            self.spd_per_frame_x = -self.speed
        else:
            self.spd_per_frame_x -= self.acceleration

        

    def go_right(self):
        if self.movement_start_times[1] == 0:
            self.movement_start_times[1] = pygame.time.get_ticks()/1000

        if pygame.time.get_ticks()/1000 - self.movement_start_times[1] >= self.movement_durations[1]:
            self.movement_start_times[1] = 0
            return

        if self.spd_per_frame_x >= self.speed:
            self.spd_per_frame_x = self.speed
        else:
            self.spd_per_frame_x += self.acceleration
    
    def go_up(self):
        if self.movement_start_times[2] == 0:
            self.movement_start_times[2] = pygame.time.get_ticks()/1000
        
        if pygame.time.get_ticks()/1000 - self.movement_start_times[2] >= self.movement_durations[2]:
            self.movement_start_times[2] = 0
            return

        if self.spd_per_frame_y <= -self.speed:
            self.spd_per_frame_y = -self.speed
        else:
            self.spd_per_frame_y -= self.acceleration

    def go_down(self):
        if self.movement_start_times[3] == 0:
            self.movement_start_times[3] = pygame.time.get_ticks()/1000

        if pygame.time.get_ticks()/1000 - self.movement_start_times[3] >= self.movement_durations[3]:
            self.movement_start_times[3] = 0
            return

        if self.spd_per_frame_y >= self.speed:
            self.spd_per_frame_y = self.speed
        else:
            self.spd_per_frame_y += self.acceleration

    def normalize_speed(self):
        if abs(self.spd_per_frame_x) > self.speed/ (2**0.5) and abs(self.spd_per_frame_y) > self.speed/ (2**0.5):
            self.spd_per_frame_x = self.speed/ 2**0.5 * self.spd_per_frame_x/ abs(self.spd_per_frame_x)
            self.spd_per_frame_y = self.speed/ 2**0.5 * self.spd_per_frame_y/ abs(self.spd_per_frame_y)

    def move(self):
        if 0 <= self.x + self.spd_per_frame_x <= SCREEN_WIDTH - self.width:
            self.x += self.spd_per_frame_x

        if 0 <= self.y + self.spd_per_frame_y <= SCREEN_HEIGHT - self.height:
            self.y += self.spd_per_frame_y

    def check_collision_wall(self):
        
        if self.x + self.spd_per_frame_x < 0 or self.x + self.spd_per_frame_x > SCREEN_WIDTH - self.width:
            self.spd_per_frame_x *=-1

        if self.y + self.spd_per_frame_y < 0 or self.y + self.spd_per_frame_y > SCREEN_HEIGHT - self.height:
            self.spd_per_frame_y *= -1


    def setHealth(self, health):
        self.health = health

    def checkHealth(self):
        if self.health <= 0:
            return False
        return True
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        self.weapon.draw(screen)

    def collide(self, bullet):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(bullet.x, bullet.y, bullet.width, bullet.height)

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shoot_time >= random.randint(2000, 5000):
            self.last_shoot_time = now
            self.weapon.shoot(self.weapon.angle)