import math
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, RED, BROWN, WHITE, GRAY
from player import Player
from bullet import Bullet
from item import Item
from weapon import Weapon
from enemy import Enemy
from enemy_tank import Enemy_Tank

# Initialize Pygame
pygame.init()
font = pygame.font.Font(None, 40)
# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping Square With ML")




class Game:
    def __init__(self):
        
        self.load_level1()
        self.level_number = 0
        self.is_start_screen = True
        self.running = True
        self.is_game_paused = False

        self.levels = [False, False, False, False, False]

        
    def run(self):
        while self.running:
            self.check_status()
            if not self.is_game_over:
                self.level_up_check()
                self.update()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(f"Mouse Clicked at: {pygame.mouse.get_pos()} (Button {event.button})")
                                
            else:
                self.handle_events()
                self.game_over()

            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.weapon.shoot_from_player()


            


            

        



    def update(self):
        pygame.display.set_caption(f"Jumping Square With ML - FPS: {self.clock.get_fps():.2f}")
        if self.is_game_over:
            self.game_over()
        else:
            if self.running:
                self.handle_events()

                if self.is_start_screen:
                    self.load_level0()
                elif self.is_game_paused:
                    self.pause()
                else:
                    keys = pygame.key.get_pressed()
                    self.player.handle_input(keys)
                    self.player.update()
                    self.collision_checks()
                    self.enemy_updates()
                    self.player.weapon.update()
                    self.level_up_check()
                    
                    self.draw()
                    

            if not self.player.checkHealth():
                self.is_game_over = True

            

    def draw(self):
        screen.fill(WHITE)
        self.player.draw(screen)
        self.player.render_speed(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (650, 20))

        health_text = font.render(f"Health: {self.player.health}", True, (0, 0, 0))
        screen.blit(health_text, (650, 50))

        for i in range(len(self.items)):
            self.items[i].draw(screen)

        for i in range(len(self.enemies)):
            self.enemies[i].draw(screen)

        
        len_enemies = len(self.enemies)
        for i in range(len(self.player.weapon.bullets)):
            self.player.weapon.bullets[i].draw(screen)

        len_tank_enemies = len(self.tank_enemies)
        for i in range(len(self.tank_enemies)):
            self.tank_enemies[i].draw(screen)
  
        pygame.display.flip()

    def draw_start_screen(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Jumping Square With ML", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        pygame.draw.rect(screen, WHITE, self.restart_button)
        text_surf = font.render("Start", True, BLUE)
        text_rect = text_surf.get_rect(center=self.restart_button.center)
        screen.blit(text_surf, text_rect)

        

        pygame.display.flip()

    def game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        start_button = pygame.Rect(300, 300, 200, 50)
        if start_button.collidepoint(pygame.mouse.get_pos()):
            color = GRAY
        else:
            color = WHITE
        

        pygame.draw.rect(screen, color, start_button)

        text_surf = font.render("Restart", True, BLUE)
        text_rect = text_surf.get_rect(center=self.restart_button.center)
        screen.blit(text_surf, text_rect)

        # click event
        mouse_pos = pygame.mouse.get_pos()
        if self.restart_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.is_game_over = False
                self.player.setHealth(100)
                self.enemies = []
                self.items = []
                self.load_level1()
                self.score = 0


        

                    
        pygame.display.flip()

    def check_status(self):
        if not self.player.checkHealth():
            self.is_game_over = True

    def create_items(self, num_items=10):
        for i in range(num_items):
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, SCREEN_HEIGHT - 20)
            self.items.append(Item(x, y, 20, 20))

    def create_enemies(self,num_enemies=10):
        for i in range(num_enemies):
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, SCREEN_HEIGHT - 20)

            enemy = Enemy(x, y, 20, 20, 5)
            self.enemies.append(enemy)

    def create_enemy_tank(self, num_tanks=5):
        for i in range(num_tanks):
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, SCREEN_HEIGHT - 20)
            enemy_tank = Enemy_Tank(x, y, 40, 60, 5, self)
            enemy_tank.weapon = Weapon(x, y, 30, enemy_tank)
            enemy_tank.weapon.is_enemy = True   
            enemy_tank.target = self.player
            self.tank_enemies.append(enemy_tank)

    def load_level0(self):
        # A simple menu that includes 
        # start button, quit button, title,
        # instructions, background image, settings button
        
        self.draw_start_screen()
        # click event
        mouse_pos = pygame.mouse.get_pos()
        if self.restart_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.is_start_screen = False
                self.level_number = 1


    def load_level1(self):
        self.player = Player(400, 300, 60, 60, 10, self)
        weapon = Weapon(400, 300, 30, self.player)
        self.player.weapon = weapon
        self.player.weapon.is_player = True
        self.running = True
        self.clock = pygame.time.Clock()

        self.score = 0

        self.items = []
        self.enemies = []
        self.tank_enemies = []

        self.is_game_over = False
        self.is_game_paused = False

        self.levels = [True, False]

        self.restart_button = pygame.Rect(300, 300, 200, 50)
        text_surf = font.render("Restart", True, BLUE)
        text_rect = text_surf.get_rect(center=self.restart_button.center)
        screen.blit(text_surf, text_rect)


        self.player.setHealth(100)
        self.score = 0
        self.create_items(10)
        # self.create_enemies(5)
        self.create_enemy_tank(3)
 
    def load_level2(self):
        self.player.setHealth(100)
        self.score = 0
        self.create_items(20)
        self.create_enemies(7)

    def load_level3(self):
        self.player.setHealth(100)
        self.score = 0
        self.create_items(20)
        self.create_enemies(7)

    def load_level4(self):
        self.player.setHealth(100)
        self.score = 0
        self.create_items(20)
        self.create_enemies(7)

    def clean(self):
        self.items = []
        self.enemies = []

    def pause(self):
        self.is_game_paused = True

    def put_text(self, text, x, y):
        text_surf = font.render(text, True, BLUE)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    def put_text_with_time(self, text, x, y, time):
        text_surf = font.render(text, True, BLUE)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)
        pygame.display.flip()
        pygame.time.wait(time)

    def collision_checks(self):
        for i in range(len(self.player.weapon.bullets) - 1, -1, -1):  # Iterate in reverse
                self.player.weapon.bullets[i].update()
                for j in range(len(self.enemies) - 1, -1, -1):  # Iterate in reverse
                    if self.player.weapon.bullets[i].collide(self.enemies[j]):
                        self.enemies.pop(j)
                        self.player.weapon.bullets.pop(i)
                        self.score += 1
                        break

    def enemy_updates(self):
        for i in range(len(self.tank_enemies) - 1, -1, -1):
                self.tank_enemies[i].update()
                self.tank_enemies[i].weapon.update()
                if self.tank_enemies[i].collide(self.player):
                    if not self.player.is_invulnerable:
                        self.player.setHealth(self.player.health - 25)
                        self.player.invulnerable()

                for j in range(len(self.player.weapon.bullets) - 1, -1, -1):
                    if self.tank_enemies[i].collide(self.player.weapon.bullets[j]):
                        self.tank_enemies[i].setHealth(self.tank_enemies[i].health - 25)
                        self.player.weapon.bullets.pop(j)
                        if self.tank_enemies[i].health <= 0:
                            self.tank_enemies.pop(i)
                            self.score += 1
                            break
        
    def level_up_check(self):

        if self.level_number == 0 and self.levels[0] == False:
            self.load_level0()
            self.levels[0] = True

        elif self.level_number == 1 and self.levels[1] == False:
            self.load_level1()
            self.levels[1] = True

        elif self.level_number == 2 and self.levels[2] == False:
            self.load_level2()
            self.levels[2] = True

        elif self.level_number == 3 and self.levels[3] == False:
            self.load_level3()
            self.levels[3] = True
            
# Create and run the game
if __name__ == "__main__":
    game = Game()
    game.run()
