from .base import Entity
from ..constants import *
from ..assets.sprites import SpriteFactory
import math

class Enemy(Entity):
    def __init__(self, x, y, width, height, speed, style=0):
        super().__init__(x, y, width, height)
        self.vel.x = -speed
        self.style = style
        self.squished = False
        self.squish_t = 0.0

    def update(self, dt, level):
        if self.squished:
            self.squish_t += dt
            return
        if not self.alive: return
        self.apply_physics(dt, GRAVITY, MAX_FALL)
        self.pos.x += self.vel.x * dt
        self.rect.x = int(self.pos.x)
        self._collide_y(level.solid_tiles)
        self._collide_x(level.solid_tiles)

    def _collide_x(self, tiles):
        for t in tiles:
            if self.rect.colliderect(t.rect):
                self.vel.x *= -1
                self.rect.x = t.rect.right if self.vel.x > 0 else t.rect.left - self.rect.width
                self.pos.x = float(self.rect.x)
                break

    def _collide_y(self, tiles):
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.vel.y >= 0:
                    self.rect.bottom = t.rect.top
                    self.vel.y = 0
                else:
                    self.rect.top = t.rect.bottom
                    self.vel.y = 0
                self.pos.y = float(self.rect.y)
                break

    def squish(self):
        self.squished = True
        self.alive = False
        self.vel.x = 0

class Goomba(Enemy):
    def __init__(self, x, y, style=0):
        super().__init__(x, y, E_W, E_H, ENEMY_SPEED, style)
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        super().update(dt, level)
        if not self.squished:
            self.frame_t += dt
            if self.frame_t >= 0.2:
                self.frame_t = 0
                self.frame = (self.frame + 1) % 2

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_goomba(self.frame, self.squished, style=self.style)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class Snail(Enemy):
    def __init__(self, x, y, style=0):
        super().__init__(x, y, 44, 36, 45, style)
        self.shelled = False
        self.shell_t = 0.0
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        if self.shelled:
            self.shell_t += dt
            self.apply_physics(dt, GRAVITY, MAX_FALL)
            self._collide_y(level.solid_tiles)
            if self.shell_t > 4.0:
                self.shelled = False
                self.vel.x = -45
            return
        super().update(dt, level)
        self.frame_t += dt
        if self.frame_t >= 0.3:
            self.frame_t = 0
            self.frame = (self.frame + 1) % 2

    def squish(self):
        if not self.shelled:
            self.shelled = True
            self.shell_t = 0
            self.vel.x = 0
        else:
            super().squish()

    def stomp(self):
        """Standard stomping behavior for Snail: Shell first, then death."""
        if not self.shelled:
            self.shelled = True
            self.shell_t = 0
            self.vel.x = 0
            return False # Not dead yet
        else:
            self.squish()
            return True # Dead

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_snail(self.frame, self.squished or self.shelled, self.vel.x > 0, style=self.style)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class Slime(Enemy):
    def __init__(self, x, y, style=0):
        # Adjusted height for better bouncing collision
        super().__init__(x, y, 34, 28, 50, style)
        self.bounce_v = -320
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        if self.squished:
            self.squish_t += dt
            return
        if not self.alive: return
        
        self.apply_physics(dt, GRAVITY, MAX_FALL)
        self.pos.x += self.vel.x * dt
        self.rect.x = int(self.pos.x)
        
        # Specialized Y collision for Slime (Bouncing)
        for t in level.solid_tiles:
            if self.rect.colliderect(t.rect):
                if self.vel.y >= 0:
                    self.rect.bottom = t.rect.top
                    self.vel.y = self.bounce_v
                else:
                    self.rect.top = t.rect.bottom
                    self.vel.y = 0
                self.pos.y = float(self.rect.y)
                break
        
        self._collide_x(level.solid_tiles)

        self.frame_t += dt
        if self.frame_t >= 0.12:
            self.frame_t = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_slime(self.frame, self.squished)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class Shark(Enemy):
    def __init__(self, x, y, style=0):
        super().__init__(x, y, 52, 36, 80, style)
        self.patrol = (x - 100, x + 100)
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        if self.squished:
            self.squish_t += dt
            return
        self.pos.x += self.vel.x * dt
        if self.pos.x <= self.patrol[0]: self.vel.x = 80
        elif self.pos.x >= self.patrol[1]: self.vel.x = -80
        self.rect.x = int(self.pos.x)
        self.frame_t += dt
        if self.frame_t >= 0.16:
            self.frame_t = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_shark(self.frame, 1 if self.vel.x > 0 else -1)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class Bat(Enemy):
    def __init__(self, x, y, style=0):
        super().__init__(x, y, 32, 20, 100, style)
        self.base_y = float(y)
        self.time = 0.0
        self.patrol = (x - 200, x + 200)
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        if self.squished:
            self.squish_t += dt
            return
        self.time += dt
        self.pos.x += self.vel.x * dt
        if self.pos.x <= self.patrol[0]: self.vel.x = 100
        elif self.pos.x >= self.patrol[1]: self.vel.x = -100
        self.pos.y = self.base_y + math.sin(self.time * 3) * 40
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        self.frame_t += dt
        if self.frame_t >= 0.1:
            self.frame_t = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_bat(self.frame, self.squished, self.vel.x > 0, style=self.style)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class Crab(Enemy):
    def __init__(self, x, y, style=0):
        super().__init__(x, y, 38, 30, 58, style)
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        super().update(dt, level)
        self.frame_t += dt
        if self.frame_t >= 0.18:
            self.frame_t = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_crab(self.frame, self.squished, self.vel.x > 0, style=self.style)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))
class Ghost(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 40, 60)
        self.base_y = float(y)
        self.time = 0.0
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        if self.squished:
            self.squish_t += dt
            return
        self.time += dt
        self.pos.x += self.vel.x * dt
        # Floats up and down
        self.pos.y = self.base_y + math.sin(self.time * 2) * 50
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        
        # Screen wrap or bounce? Let's just bounce in a range for now if no walls
        # Actually, let's just let it fly.
        
        self.frame_t += dt
        if self.frame_t >= 0.15:
            self.frame_t = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_halloween_ghost(self.frame, self.squished)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class Pumpkin(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 70)
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        super().update(dt, level)
        if not self.squished:
            self.frame_t += dt
            if self.frame_t >= 0.2:
                self.frame_t = 0
                self.frame = (self.frame + 1) % 2

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_halloween_pumpkin(self.frame, self.squished)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class Spider(Enemy):
    def __init__(self, x, y):
        # Spider hangs from ceiling or moves on floor?
        # Let's make it a ceiling dropper or wall walker.
        # Simple walker for now.
        super().__init__(x, y, 36, 30, 90)
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        super().update(dt, level)
        if not self.squished:
            self.frame_t += dt
            if self.frame_t >= 0.1:
                self.frame_t = 0
                self.frame = (self.frame + 1) % 4

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_halloween_spider(self.frame, self.squished)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))
class GingerbreadMan(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 34, 40, 75)
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        super().update(dt, level)
        if not self.squished:
            self.frame_t += dt
            if self.frame_t >= 0.15:
                self.frame_t = 0
                self.frame = (self.frame + 1) % 2

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_gingerbread_man(self.frame, self.squished)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class CandyMonster(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 44, 44, 50)
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        super().update(dt, level)
        if not self.squished:
            self.frame_t += dt
            if self.frame_t >= 0.12:
                self.frame_t = 0
                self.frame = (self.frame + 1) % 4

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_candy_monster(self.frame, self.squished)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class FlyingSweet(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 36, 24, 110)
        self.base_y = float(y)
        self.time = 0.0
        self.frame = 0
        self.frame_t = 0

    def update(self, dt, level):
        if self.squished:
            self.squish_t += dt
            return
        self.time += dt
        self.pos.x += self.vel.x * dt
        self.pos.y = self.base_y + math.sin(self.time * 4) * 30
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        
        self.frame_t += dt
        if self.frame_t >= 0.08:
            self.frame_t = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen, cam_x):
        if self.squished and self.squish_t > 0.5: return
        img = SpriteFactory.get_flying_sweet(self.frame)
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))
