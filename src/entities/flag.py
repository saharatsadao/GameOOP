import pygame, math, random
from ..constants import *

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y_bottom):
        super().__init__()
        # Even taller rect to ensure ground overlap
        self.rect = pygame.Rect(x - 30, y_bottom - 120, 140, 140)
        self.touched = False
        self.time = 0

    def draw(self, screen, cx):
        self.time += 0.05
        sx = self.rect.x - cx
        sy = self.rect.y
        
        # 1. Outer Glow (Pulsing blue)
        glow_size = int(10 + 8 * math.sin(self.time * 4))
        glow_rect = (sx - glow_size, sy - glow_size, 80 + glow_size*2, 120 + glow_size*2)
        pygame.draw.rect(screen, (100, 150, 255, 40), glow_rect, border_radius=15)

        # 2. Door Frame (Magical Stone/Metal)
        # Frame Base
        pygame.draw.rect(screen, (40, 45, 60), (sx, sy, 80, 120), border_radius=10)
        # Bevel/Details
        pygame.draw.rect(screen, (120, 130, 160), (sx, sy, 80, 120), 6, border_radius=10)
        pygame.draw.rect(screen, (200, 220, 255), (sx + 4, sy + 4, 72, 112), 2, border_radius=8)
        
        # 3. Inner Portal (The "Event Horizon")
        inner_rect = (sx + 8, sy + 8, 64, 104)
        # Gradient/Pattern inside
        color = (0, 100, 255) if not self.touched else (255, 255, 255)
        inner_surf = pygame.Surface((64, 104), pygame.SRCALPHA)
        alpha = int(140 + 60 * math.sin(self.time * 4))
        pygame.draw.rect(inner_surf, (*color, alpha), (0, 0, 64, 104), border_radius=5)
        
        # Energy swirls
        for i in range(3):
            angle = self.time * 2 + i * 2
            px = 32 + math.cos(angle) * 20
            py = 52 + math.sin(angle * 1.5) * 35
            pygame.draw.circle(inner_surf, (255, 255, 255, 180), (int(px), int(py)), 3)
            
        screen.blit(inner_surf, (sx + 8, sy + 8))

        # 4. Particles floating around
        for i in range(8):
            t = self.time * 0.5 + i
            px = sx + 40 + math.cos(t * 2) * 45
            py = sy + 60 + math.sin(t * 3) * 65
            if 0 < py - sy < 120: # Keep within height for coolness
                size = random.randint(1, 3)
                pygame.draw.circle(screen, (150, 200, 255), (int(px), int(py)), size)

    def update(self, dt):
        pass
