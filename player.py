import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE
from health_bar import Health_Bar
 

class Player:
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

        self.weapon = None

        self.invulnerable_start_time = 0
        self.invulnerable_duration = 2

        self.health_bar = Health_Bar(self)
        self.health_bar.player = self


        self.invulnerable()

        #self.sprite_image = pygame.image.load("assets\\tank\\PNG\\Hulls_Color_A\\Hull_02.png")
        # scale the image to the desired width and height with preserving the aspect ratio
        #self.sprite_image = pygame.transform.scale(self.sprite_image, (self.width, self.height))
    def handle_input(self, keys):
        # Adjust speeds based on key presses
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.spd_per_frame_x <= -self.speed:
                self.spd_per_frame_x = -self.speed
            else:
                self.spd_per_frame_x -= self.acceleration
        elif self.spd_per_frame_x < 0:
            if abs(self.spd_per_frame_x) <= self.acceleration:
                self.spd_per_frame_x = 0
            else:
                self.spd_per_frame_x += self.acceleration

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.spd_per_frame_x >= self.speed:
                self.spd_per_frame_x = self.speed
            else:
                self.spd_per_frame_x += self.acceleration
        elif self.spd_per_frame_x > 0:
            if abs(self.spd_per_frame_x) <= self.acceleration:
                self.spd_per_frame_x = 0
            else:
                self.spd_per_frame_x -= self.acceleration

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.spd_per_frame_y <= -self.speed:
                self.spd_per_frame_y = -self.speed
            else:
                self.spd_per_frame_y -= self.acceleration
        elif self.spd_per_frame_y < 0:
            if abs(self.spd_per_frame_y) <= self.acceleration:
                self.spd_per_frame_y = 0
            else:
                self.spd_per_frame_y += self.acceleration
                
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.spd_per_frame_y >= self.speed:
                self.spd_per_frame_y = self.speed
            else:
                self.spd_per_frame_y += self.acceleration
        elif self.spd_per_frame_y > 0:
            if abs(self.spd_per_frame_y )<= self.acceleration:
                self.spd_per_frame_y = 0
            else:
                self.spd_per_frame_y -= self.acceleration
    def update(self):

        if self.is_invulnerable:
            self.invulnerable()
        self.normalize_speed()
        self.update_position()
        self.check_item_collision()
        self.check_bullet_collision()
        self.health_bar.update()

                
    def setHealth(self, health):
        self.health = health
        self.health_bar.health = health

    def checkHealth(self):
        if self.health <= 0:
            return False
        return True


    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        self.weapon.draw(screen)
        self.health_bar.draw(screen)
        #screen.blit(self.sprite_image, (self.x, self.y))

    def render_speed(self, screen):
        font = pygame.font.Font(None, 36)
        text_x = font.render(f"Speed X: {self.spd_per_frame_x:.2f}", True, (0, 0, 0))
        text_y = font.render(f"Speed Y: {self.spd_per_frame_y:.2f}", True, (0, 0, 0))
        screen.blit(text_x, (10, 10))
        screen.blit(text_y, (10, 40))

    def collide(self, item):
        # use colliderect() to check for collision
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(pygame.Rect(item.x, item.y, item.width, item.height))

    def invulnerable(self):
        if not self.is_invulnerable:
            self.is_invulnerable = True
            self.invulnerable_start_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.invulnerable_start_time >= self.invulnerable_duration * 1000:
            self.is_invulnerable = False

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

    def check_item_collision(self):
        for i in range(len(self.game.items) - 1, -1, -1):  # Iterate in reverse
            if self.collide(self.game.items[i]):
                self.game.items.pop(i)
                self.game.score += 1
                if self.health < self.max_health:
                    self.health += 5
                    if self.health > self.max_health:
                        self.health = self.max_health

    def check_bullet_collision(self):
        for tank_enemy in self.game.tank_enemies:
            for i in range(len(tank_enemy.weapon.bullets) - 1, -1, -1):
                if self.collide(tank_enemy.weapon.bullets[i]):
                    if not self.is_invulnerable:
                        self.setHealth(self.health - 25)
                    tank_enemy.weapon.bullets.pop(i)
                    