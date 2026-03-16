import pygame
import math
import random
from ..constants import *
from ..assets.sprites import SpriteFactory

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.kind = kind

    def update(self, dt): pass
    def draw(self, screen, camera_x):
        img = SpriteFactory.get_tile(self.kind)
        screen.blit(img, (self.rect.x - camera_x, self.rect.y))

class SolidTile(Tile): pass

class Decoration(pygame.sprite.Sprite):
    """Background elements like clouds, mountains, bushes, flowers, etc."""
    def __init__(self, x, y, kind, parallax=1.0, w=0, h=0, variant=0, **kwargs):
        super().__init__()
        self.x, self.y = x, y
        self.kind = kind
        self.parallax = parallax
        self.w, self.h = w, h
        self.variant = variant
        self.color = kwargs.get('color', (255, 80, 100))
        self.frame = 0
        self.timer = 0
        self._set_image()

    def update(self, dt):
        if self.kind == 'seaweed':
            self.timer += dt
            if self.timer > 0.15:
                self.timer = 0
                self.frame = (self.frame + 1) % 8
                self.image = SpriteFactory.get_seaweed(self.frame)
        elif self.kind == 'fish':
            self.timer += dt
            if self.timer > 0.2:
                self.timer = 0
                self.frame = (self.frame + 1) % 4
                self.image = SpriteFactory.get_fish_silhouette(self.frame)
            self.x -= 40 * dt # Fish swim left
            if self.x < -100: self.x = 2000 # Randomize this later or recycle in level

    def _set_image(self):
        if self.kind == 'cloud': self.image = SpriteFactory.get_cloud(self.w, self.h)
        elif self.kind == 'mountain': self.image = SpriteFactory.get_mountain(self.w, self.h)
        elif self.kind == 'bush': self.image = SpriteFactory.get_bush(self.w, self.h)
        elif self.kind == 'palm': self.image = SpriteFactory.get_palm(self.h)
        elif self.kind == 'flower': self.image = SpriteFactory.get_flower(self.variant)
        elif self.kind == 'cactus': self.image = SpriteFactory.get_cactus(self.h)
        elif self.kind == 'crystal': self.image = SpriteFactory.get_crystal(self.h, self.variant)
        elif self.kind == 'med_tree': self.image = SpriteFactory.get_medieval_tree(self.h)
        elif self.kind == 'house_s': self.image = SpriteFactory.get_house_small()
        elif self.kind == 'house_l': self.image = SpriteFactory.get_house_large()
        elif self.kind == 'well': self.image = SpriteFactory.get_village_well()
        elif self.kind == 'barrel': self.image = SpriteFactory.get_barrel()
        elif self.kind == 'trash_can': self.image = SpriteFactory.get_trash_can()
        elif self.kind == 'coral': self.image = SpriteFactory.get_coral(self.variant)
        elif self.kind == 'seaweed': self.image = SpriteFactory.get_seaweed(0)
        elif self.kind == 'shell': self.image = SpriteFactory.get_sea_shell(self.variant)
        elif self.kind == 'bubble': self.image = SpriteFactory.get_underwater_bubble()
        elif self.kind == 'god_ray': 
             w = self.w if self.w > 0 else 200
             h = self.h if self.h > 0 else 600
             self.image = SpriteFactory.get_god_ray(w, h)
        elif self.kind == 'fish': self.image = SpriteFactory.get_fish_silhouette(0)
        elif self.kind == 'heart': self.image = SpriteFactory.get_heart(TILE)
        elif self.kind == 'med_bush': self.image = SpriteFactory.get_med_bush()
        elif self.kind == 'skyline': self.image = SpriteFactory.get_city_skyline(self.w, self.h)
        elif self.kind == 'building': self.image = SpriteFactory.get_urban_building(self.w, self.h, self.variant)
        elif self.kind == 'lamp': self.image = SpriteFactory.get_street_lamp()
        elif self.kind == 'neon': self.image = SpriteFactory.get_neon_sign(['MARKET','BAR','CAFE'][self.variant % 3])
        elif self.kind == 'forest_bg': self.image = SpriteFactory.get_forest_bg(self.w, self.h)
        elif self.kind == 'god_ray': self.image = SpriteFactory.get_god_ray(self.w, self.h)
        elif self.kind == 'pyramid': self.image = SpriteFactory.get_pyramid(self.w, self.h)
        elif self.kind == 'spooky_tree': self.image = SpriteFactory.get_spooky_tree(self.h)
        elif self.kind == 'spooky_house': self.image = SpriteFactory.get_spooky_house(self.w, self.h)
        elif self.kind == 'tombstone': self.image = SpriteFactory.get_tombstone(self.variant)
        elif self.kind == 'spooky_fence': self.image = SpriteFactory.get_spooky_fence(self.w)
        elif self.kind == 'spooky_moon': self.image = SpriteFactory.get_spooky_moon(self.w, self.h)
        elif self.kind == 'lollipop': 
            self.image = SpriteFactory.get_lollipop(color=self.color, h=self.h)
        elif self.kind == 'candy_cane': self.image = SpriteFactory.get_candy_cane(self.h)
        elif self.kind == 'cupcake': self.image = SpriteFactory.get_cupcake(self.w, self.h)
        elif self.kind == 'marshmallow_cloud': self.image = SpriteFactory.get_marshmallow_cloud(self.w, self.h)
        elif self.kind == 'wafer_pillar': self.image = SpriteFactory.get_wafer_pillar(self.h)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen, camera_x):
        screen.blit(self.image, (int(self.x - camera_x * self.parallax), self.y))

class InteractableTile(Tile):
    def __init__(self, x, y, kind, reward=None):
        super().__init__(x, y, kind)
        self.reward = reward
        self.used = False
        self.bump_off = 0
        self.bump_t = 0
        self.anim_f = 0
        self.anim_t = 0

    def bump(self):
        from ..assets.sounds import sounds
        if not self.used:
            self.used = True
            self.bump_t = 0.3
            sounds.play('block')
            return self.reward
        return None

    def update(self, dt):
        if self.bump_t > 0:
            self.bump_t -= dt
            self.bump_off = int(8 * self.bump_t / 0.3)
        else: self.bump_off = 0
        
        if not self.used:
            self.anim_t += dt
            if self.anim_t >= 0.15:
                self.anim_t = 0
                self.anim_f = (self.anim_f + 1) % 4

    def draw(self, screen, camera_x):
        img = SpriteFactory.get_tile(self.kind, frame=self.anim_f, used=self.used)
        screen.blit(img, (self.rect.x - camera_x, self.rect.y - self.bump_off))

class CoinTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x + (TILE-C_R*2)//2, y + (TILE-C_R*2)//2, C_R*2, C_R*2)
        self.frame = 0
        self.ft = 0

    def update(self, dt):
        self.ft += dt
        if self.ft >= 0.1:
            self.ft = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen, cx):
        img = SpriteFactory.get_coin(self.frame)
        screen.blit(img, (self.rect.x - cx, self.rect.y))

class LavaTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, 'lava')
        self.frame = 0
        self.ft = 0

    def update(self, dt):
        self.ft += dt
        if self.ft >= 0.1:
            self.ft = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen, cx):
        pygame.draw.rect(screen, (255, 60, 20), (self.rect.x - cx, self.rect.y, TILE, TILE))
        pygame.draw.rect(screen, (220, 100, 40), (self.rect.x - cx + 2, self.rect.y + self.frame*2, TILE-4, 4))

class HeartItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x + 8, y + 8, 32, 32)
        self.pos = pygame.Vector2(x + 8, y + 8)
        self.start_y = y + 8
        self.vel = pygame.Vector2(0, -150) # Pop straight up
        self.gravity = 400
        self.stationary = False

    def update(self, dt):
        if not self.stationary:
            self.vel.y += self.gravity * dt
            self.pos += self.vel * dt
            # Stop falling when back near start or a bit above
            if self.vel.y > 0 and self.pos.y >= self.start_y - 40:
                self.pos.y = self.start_y - 48 # Rest on top of the block
                self.stationary = True
                self.vel.y = 0
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, screen, cx):
        # Pulsing effect
        scale = 32 + int(4 * math.sin(pygame.time.get_ticks() * 0.01))
        img = SpriteFactory.get_heart(scale)
        screen.blit(img, (self.rect.x - cx - (scale-32)//2, self.rect.y - (scale-32)//2))

class VisualCoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        from ..assets.sprites import C_R
        self.pos = pygame.Vector2(x + (TILE-C_R*2)//2, y)
        self.start_y = y
        self.vel = pygame.Vector2(0, -300) # Popping speed
        self.gravity = 800
        self.frame = 0
        self.anim_timer = 0
        self.rect = pygame.Rect(self.pos.x, self.pos.y, C_R*2, C_R*2)

    def update(self, dt):
        self.vel.y += self.gravity * dt
        self.pos += self.vel * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        
        self.anim_timer += dt
        if self.anim_timer > 0.05:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % 4
            
        # Kill the visual coin once it falls back near the block
        if self.vel.y > 0 and self.pos.y >= self.start_y - 10:
            self.kill()

    def draw(self, screen, cx):
        img = SpriteFactory.get_coin(self.frame)
        screen.blit(img, (self.rect.x - cx, self.rect.y))
