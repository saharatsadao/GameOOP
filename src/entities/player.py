import pygame
from .base import Entity
from ..constants import *
from ..assets.sprites import SpriteFactory

class Player(Entity):
    """The main player character."""
    def __init__(self, x, y):
        super().__init__(x, y, P_W, P_H)
        self.on_ground = False
        self.direction = 1
        self.state = 'idle'
        self.frame = 0
        self.frame_t = 0
        self.jumps_left = 2
        self.health = 3
        self.max_health = 3
        self.inv_timer = 0 # Invincibility timer
        self.hit_flash = 0 # Visual flash timer
        self.dead = False

    def handle_input(self):
        if self.dead: return
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -WALK_SPEED
            self.direction = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = WALK_SPEED
            self.direction = 1
            
        # Ground state handled in _animate

    def jump(self):
        from ..assets.sounds import sounds
        if self.on_ground or self.jumps_left > 0:
            self.vel.y = JUMP_FORCE_1 if self.on_ground else JUMP_FORCE_2
            self.on_ground = False
            self.jumps_left -= 1
            sounds.play('jump')

    def update(self, dt, level):
        if self.dead:
            # Gravity only, no collisions
            self.vel.y = min(self.vel.y + GRAVITY * dt, MAX_FALL)
            self.pos += self.vel * dt
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
            return

        if self.inv_timer > 0:
            self.inv_timer -= dt
        if self.hit_flash > 0:
            self.hit_flash -= dt

        self.handle_input()
        
        # Physics (Vertical)
        self.vel.y = min(self.vel.y + GRAVITY * dt, MAX_FALL)
        self.pos.y += self.vel.y * dt
        self.rect.y = int(self.pos.y)
        self._check_collisions(level.solid_tiles, horizontal=False)
        
        # Horizontal movement
        self.pos.x += self.vel.x * dt
        self.rect.x = int(self.pos.x)
        self._check_collisions(level.solid_tiles, horizontal=True)
        
        # Animation
        self._animate(dt)

    def _check_collisions(self, tiles, horizontal):
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if horizontal:
                    if self.vel.x > 0: self.rect.right = tile.rect.left
                    elif self.vel.x < 0: self.rect.left = tile.rect.right
                    self.pos.x = float(self.rect.x)
                else:
                    if self.vel.y > 0:
                        self.rect.bottom = tile.rect.top
                        self.vel.y = 0
                        self.on_ground = True
                        self.jumps_left = 2 # Double jump reset
                    elif self.vel.y < 0:
                        self.rect.top = tile.rect.bottom
                        self.vel.y = 0
                        if hasattr(tile, 'bump'):
                            reward = tile.bump()
                            if reward:
                                if not hasattr(self, 'pending_rewards'): self.pending_rewards = []
                                self.pending_rewards.append({'reward': reward, 'pos': (tile.rect.x, tile.rect.y)})
                    self.pos.y = float(self.rect.y)

    def _animate(self, dt):
        # Determine state
        if self.inv_timer > 1.5: # First 0.5s of hit
            self.state = 'hit'
        elif not self.on_ground:
            self.state = 'jump'
        elif self.vel.x != 0:
            self.state = 'walk'
        else:
            self.state = 'idle'

        # Update frames
        if self.state == 'walk':
            self.frame_t += dt
            if self.frame_t >= 0.1: # Slightly faster walk
                self.frame_t = 0
                self.frame = (self.frame + 1) % 4
        elif self.state == 'jump':
            self.frame = 0 # Static jump pose
        else:
            self.frame = 0

    def draw(self, screen, camera_x):
        # Flicker when invincible
        if self.inv_timer > 0 and int(self.inv_timer * 20) % 2 == 0:
            return
            
        state = 'hit' if self.dead else self.state
        img = SpriteFactory.get_mario(state, self.direction, self.frame)
        
        # Hit Flash (Strong visual feedback)
        if self.hit_flash > 0:
            flash = img.copy()
            flash.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_ADD)
            img = flash
            
        screen.blit(img, (self.rect.x - camera_x, self.rect.y))

    def take_damage(self):
        if self.inv_timer <= 0:
            from ..assets.sounds import sounds
            self.health -= 1
            self.inv_timer = 2.0 # 2 seconds of invincibility
            self.hit_flash = 0.4 # Strong flash
            sounds.play('dead') 
            if self.health <= 0:
                self.die()
                return True # Should die
        return False

    def die(self):
        if not self.dead:
            from ..assets.sounds import sounds
            self.dead = True
            self.vel.y = -600
            self.vel.x = 0
            self.on_ground = False
            sounds.play('dead')
