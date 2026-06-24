import pygame
import random
import math
from settings import *

class AIGuard:
    def __init__(self):
        # 1. Tentukan sisi asal secara acak
        self.start_side = random.choice(["LEFT", "RIGHT"])
        
        # 2. Posisi awal (X di kiri atau kanan layar, Y di mana saja)
        self.x = 0 if self.start_side == "LEFT" else WIDTH
        self.y = random.randint(50, HEIGHT - 50)
        
        # 3. Kecepatan (Arah ditentukan oleh start_side)
        self.speed = 3 
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def move(self):
        # 4. Bergerak konstan sesuai sisi asal, TANPA menuju tengah
        if self.start_side == "LEFT":
            self.x += self.speed
        else:
            self.x -= self.speed
        
        self.rect.x, self.rect.y = self.x, self.y

    def draw(self, surface):
        pygame.draw.rect(surface, NEON_RED, self.rect)

class Ship:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 30, 30)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.y > 0: self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < HEIGHT - 30: self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.x > 0: self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < WIDTH - 30: self.rect.x += self.speed

    def draw(self, surface, mouse_pos):
        rel_x, rel_y = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        angle = (180 / 3.14159) * -math.atan2(rel_y, rel_x) - 90
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (255, 255, 0), [(20, 0), (40, 40), (0, 40)])
        rotated_surf = pygame.transform.rotate(surf, angle)
        surface.blit(rotated_surf, self.rect.topleft)

class Explosion:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.radius = 5
        self.timer = 15 

    def draw(self, surface):
        if self.timer > 0:
            pygame.draw.circle(surface, (255, 165, 0), (self.x, self.y), self.radius)
            self.radius += 2
            self.timer -= 1