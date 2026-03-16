import pygame, random
import math
from .tiles import Tile, SolidTile, InteractableTile, Decoration, CoinTile, LavaTile
from .level_data import MAP_DATA
from ..constants import *
from ..assets.sprites import SpriteFactory
from ..entities.enemies import Goomba, Snail, Shark, Bat, Slime, Crab, Ghost, Pumpkin, Spider, GingerbreadMan, CandyMonster, FlyingSweet
from ..entities.flag import Flag

class Level:
    def __init__(self, world, stage):
        self.world = world
        self.stage = stage
        self.map_data = MAP_DATA.get((world, stage), MAP_DATA[(1,1)])
        
        self.tiles = pygame.sprite.Group()
        self.solid_tiles = pygame.sprite.Group()
        self.interactable_tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.lava_tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.decorations = []
        self.flag = None
        
        if stage == 1: self.sky_color = (135, 206, 235) # Bright Ocean Surface Blue
        elif stage == 2: self.sky_color = (15, 0, 30) # Halloween Deep Purple
        elif stage == 3: self.sky_color = (255, 200, 230) # Candy Land Pink
        elif stage == 4: self.sky_color = (15, 15, 25) # Deep Urban Night

        self.water_timer = 0.0
        self.particles = []
        self.items = pygame.sprite.Group()
        self.spooky_moon = None
        
        # Calculate safe spawn point
        self.player_start = self._calculate_spawn_point()
        
        self._parse_map()
        self._generate_backgrounds()

    def _calculate_spawn_point(self):
        # Default spawn
        spawn_x, spawn_y = 100, SCREEN_H - TILE * 3
        
        # Find the first ground tile height in the first 5 columns
        for x_col in range(2, 6):
            for y_row in range(len(self.map_data)-1, -1, -1):
                char = self.map_data[y_row][x_col] if x_col < len(self.map_data[y_row]) else ' '
                if char in ('G', 'B', 'D'):
                    spawn_x = x_col * TILE
                    spawn_y = y_row * TILE - P_H - 4
                    return (spawn_x, spawn_y)
        return (spawn_x, spawn_y)

    def _parse_map(self):
        spawn_idx = self.player_start[0] // TILE
        for y, row in enumerate(self.map_data):
            for x_idx, char in enumerate(row):
                x, y_pos = x_idx * TILE, y * TILE
                
                # Avoid spawning enemies on top of player
                if char in ('E', 'S', 'M', 'R') and abs(x_idx - spawn_idx) < 3:
                    x += TILE * 4 # Move enemy further away
                if char == 'G' or char == 'D':
                    kind = 'ground_ocean' if self.stage == 1 else 'ground'
                    if self.stage == 2: kind = 'ground_spooky'
                    if self.stage == 3: kind = 'ground_candy'
                    if self.stage == 4: kind = 'ground_urban'
                    tile = SolidTile(x, y_pos, kind)
                    self.tiles.add(tile); self.solid_tiles.add(tile)
                elif char == 'B':
                    kind = 'brick'
                    if self.stage == 1: kind = 'brick_ocean'
                    elif self.stage == 2: kind = 'brick_spooky'
                    elif self.stage == 3: kind = 'brick_candy'
                    elif self.stage == 4: kind = 'brick_urban'
                    tile = SolidTile(x, y_pos, kind)
                    self.tiles.add(tile); self.solid_tiles.add(tile)
                elif char == 'Q':
                    reward = 'coin' if random.random() < 0.8 else 'heart'
                    kind = 'qblock'
                    if self.stage == 1: kind = 'qblock_ocean'
                    elif self.stage == 2: kind = 'qblock_spooky'
                    elif self.stage == 3: kind = 'qblock_candy'
                    elif self.stage == 4: kind = 'qblock_urban'
                    tile = InteractableTile(x, y_pos, kind, reward)
                    self.tiles.add(tile); self.solid_tiles.add(tile); self.interactable_tiles.add(tile)
                elif char == 'E':
                    if self.stage == 2:
                        self.enemies.add(Ghost(x, y_pos))
                    elif self.stage == 3:
                        self.enemies.add(GingerbreadMan(x, y_pos))
                    else:
                        self.enemies.add(Goomba(x, y_pos, style=self.stage))
                elif char == 'S':
                    if self.stage == 2:
                        self.enemies.add(Pumpkin(x, y_pos))
                    elif self.stage == 3:
                        self.enemies.add(CandyMonster(x, y_pos))
                    else:
                        self.enemies.add(Snail(x, y_pos, style=self.stage))
                elif char == 'M':
                    if self.stage == 2:
                        self.enemies.add(Spider(x, y_pos))
                    elif self.stage == 3:
                        self.enemies.add(FlyingSweet(x, y_pos))
                    else:
                        self.enemies.add(Slime(x, y_pos, style=self.stage))
                elif char == 'R':
                    if self.stage == 2:
                        # Maybe a crawling spider or something else
                        self.enemies.add(Spider(x, y_pos))
                    else:
                        self.enemies.add(Crab(x, y_pos, style=self.stage))
                elif char == 'C':
                    self.coins.add(CoinTile(x, y_pos))
                elif char == 'L':
                    # Lava removed per user request
                    pass
                elif char == 'F':
                    # Search down for ground in map_data starting from current column, then neighbors
                    found_y = -1
                    for check_x in [x_idx, x_idx - 1, x_idx + 1]:
                        if check_x < 0 or check_x >= len(row): continue
                        gate_y_idx = y
                        while gate_y_idx < len(self.map_data):
                            char_below = self.map_data[gate_y_idx][check_x]
                            if char_below in ('G', 'B', 'P', 'D'):
                                found_y = gate_y_idx * TILE
                                break
                            gate_y_idx += 1
                        if found_y != -1: break
                    
                    # Fallback to map bottom if still not found
                    if found_y == -1: found_y = len(self.map_data) * TILE
                    self.flag = Flag(x, found_y)
                elif char == 'H':
                    # Spooky House decoration
                    self.decorations.append(Decoration(x, y_pos - 310, 'spooky_house', 1.0, 300, 350))
                elif char == 'P':
                    kind_t = 'pipe_t'
                    if self.stage == 3: kind_t = 'pipe_candy_t'
                    tile = SolidTile(x, y_pos, kind_t)
                    self.tiles.add(tile); self.solid_tiles.add(tile)

    def _generate_backgrounds(self):
        # Multi-layered Parallax
        world_map_width = len(self.map_data[0]) * TILE
        
        # Layer 0: Foreground / Atmosphere (Realism)
        if self.stage == 1:
            # Slower, deeper sky gradient handled in draw
            pass

        # Layer 1: Deep Ocean & God Rays (0.1x - 0.2x speed)
        for i in range(0, world_map_width, 400):
            if self.stage == 1: # Underwater Background
                # Distant Rocks
                self.decorations.append(Decoration(i, SCREEN_H - 300, 'mountain', 0.1, 400, 200))
                # God Rays (Large, slow parallax)
                self.decorations.append(Decoration(i + 100, 0, 'god_ray', 0.15))
                # Fish Silhouettes
                for _ in range(3):
                    self.decorations.append(Decoration(i + random.randint(0, 400), random.randint(200, 500), 'fish', 0.2))
                # Distant bubbles
                for _ in range(5):
                    self.decorations.append(Decoration(i + random.randint(0, 400), random.randint(100, 500), 'bubble', 0.15))
            elif self.stage == 2: # Spooky Theme
                # Spooky Moon (Fixed in background)
                if i == 0:
                    self.decorations.append(Decoration(SCREEN_W - 150, 50, 'spooky_moon', 0.05, 100, 100))
                
                # Spooky Houses in far distance
                if i % 800 == 0:
                     self.decorations.append(Decoration(i + 200, SCREEN_H - 100 - 350, 'spooky_house', 0.1, 300, 350))
                # Distant twisted trees
                self.decorations.append(Decoration(i + 100, SCREEN_H - 120 - 150, 'spooky_tree', 0.2, h=150))
            elif self.stage == 3: # Candy Land
                # Pastel Mountains/Marshmallows in distance
                self.decorations.append(Decoration(i, SCREEN_H - 120 - 60, 'marshmallow_cloud', 0.1, 120, 60))
                self.decorations.append(Decoration(i + 200, SCREEN_H - 140 - 80, 'marshmallow_cloud', 0.1, 180, 90))
                self.decorations.append(Decoration(i + 400, SCREEN_H - 110 - 70, 'marshmallow_cloud', 0.1, 140, 60))
                if i % 300 == 0:
                     self.decorations.append(Decoration(i + 150, SCREEN_H - 120 - 100, 'cupcake', 0.2, 80, 100))
            elif self.stage == 4: # Urban Night
                self.decorations.append(Decoration(i, SCREEN_H - 300, 'skyline', 0.1, 800, 300))

        # Layer 2: Mid-ground Reef (0.4x speed)
        for i in range(0, world_map_width, 400):
            if self.stage == 1: # Ocean Mid-ground
                # Denser Mid-ground
                self.decorations.append(Decoration(i + 50, SCREEN_H - TILE - 120, 'coral', 0.4, variant=i//400))
                self.decorations.append(Decoration(i + 250, SCREEN_H - TILE - 100, 'seaweed', 0.4))
                if i % 800 == 0:
                     self.decorations.append(Decoration(i + 600, 0, 'god_ray', 0.4)) # Stronger closer rays
            elif self.stage == 2: # Spooky Theme
                # Mid-ground trees and fences
                self.decorations.append(Decoration(i + 50, SCREEN_H - TILE - 200, 'spooky_tree', 0.5, h=200))
                self.decorations.append(Decoration(i + 250, SCREEN_H - TILE - 48, 'spooky_fence', 0.5))
            elif self.stage == 3: # Candy Land
                # Mid-ground Lollipop trees and candy canes
                self.decorations.append(Decoration(i + 50, SCREEN_H - TILE - 150, 'lollipop', 0.5, h=150))
                self.decorations.append(Decoration(i + 150, SCREEN_H - TILE - 120, 'lollipop', 0.5, h=120, color=(100, 255, 150)))
                self.decorations.append(Decoration(i + 300, SCREEN_H - TILE - 130, 'lollipop', 0.5, h=130, color=(150, 200, 255)))
                self.decorations.append(Decoration(i + 450, SCREEN_H - TILE - 180, 'wafer_pillar', 0.5, h=250))
            elif self.stage == 4: # Big Buildings
                self.decorations.append(Decoration(i + 50, SCREEN_H - TILE - 350, 'building', 0.5, 250, 350, variant=i//600))
                self.decorations.append(Decoration(i + 350, SCREEN_H - TILE - 400, 'building', 0.6, 200, 400, variant=i//400+1))

        # Layer 3: Foreground Reef Details (1.0x speed)
        for i in range(0, world_map_width, 300):
            if self.stage == 1: # Near Reef - Very Dense
                self.decorations.append(Decoration(i + random.randint(0, 100), SCREEN_H - TILE - 80, 'coral', 1.0, variant=i//300))
                self.decorations.append(Decoration(i + random.randint(150, 250), SCREEN_H - TILE - 100, 'seaweed', 1.0))
                if i % 600 == 0:
                    self.decorations.append(Decoration(i + 50, SCREEN_H - TILE - 20, 'shell', 1.0, variant=i//600))
            elif self.stage == 2:
                # Tombstones, Fences, and Drifting Ghosts
                self.decorations.append(Decoration(i + random.randint(0, 100), SCREEN_H - TILE - 48, 'tombstone', 1.0, variant=i//300))
                if i % 400 == 0:
                     self.decorations.append(Decoration(i + random.randint(50, 350), random.randint(50, 200), 'bubble', 0.8)) # "Spooky Orbs" reuse bubble
                if i % 600 == 0:
                     self.decorations.append(Decoration(i + 400, SCREEN_H - TILE - 250, 'spooky_tree', 1.0, h=250))
            elif self.stage == 3:
                # Foreground candy canes and sweets
                self.decorations.append(Decoration(i + 20, SCREEN_H - TILE - 60, 'candy_cane', 1.0))
                self.decorations.append(Decoration(i + 240, SCREEN_H - TILE - 80, 'candy_cane', 1.0, h=80))
                if i % 400 == 0:
                     self.decorations.append(Decoration(i + 150, SCREEN_H - TILE - 150, 'lollipop', 1.0, h=150))
            elif self.stage == 4: # Street Level Details
                # Fix lamp Y (Lamp is 240, TILE is 40)
                self.decorations.append(Decoration(i + 200, SCREEN_H - TILE - 240, 'lamp', 1.0))
                self.decorations.append(Decoration(i + 500, SCREEN_H - TILE - 50, 'neon', 1.0, variant=i//800))
                self.decorations.append(Decoration(i + 50, SCREEN_H - TILE - 40, 'trash_can', 1.0))
                self.decorations.append(Decoration(i + 350, SCREEN_H - TILE - 40, 'barrel', 1.0))

    def update(self, dt):
        for t in self.tiles: t.update(dt)
        for e in self.enemies: e.update(dt, self)
        for d in self.decorations: d.update(dt)
        self.items.update(dt)
        if self.flag: self.flag.update(dt)
        
        # Atmospheric Particles
        self.water_timer += dt
        self._update_particles(dt)

    def _update_particles(self, dt):
        # Spawn particles
        if self.stage == 1: # Bubbles
            if random.random() < 0.2:
                self.particles.append({'pos': [random.randint(0, SCREEN_W), SCREEN_H], 'vel': [random.uniform(-10, 10), random.uniform(-60, -30)], 'life': 6.0, 'col': (200, 230, 255)})
        elif self.stage == 2: # Embers
            if random.random() < 0.3:
                self.particles.append({'pos': [random.randint(0, SCREEN_W), SCREEN_H], 'vel': [random.uniform(-20, 20), random.uniform(-100, -50)], 'life': 2.0, 'col': (255, 150, 50)})
        elif self.stage == 3: # Fireflies
            if len(self.particles) < 30:
                self.particles.append({'pos': [random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)], 'vel': [random.uniform(-10, 10), random.uniform(-10, 10)], 'life': 5.0, 'col': (200, 255, 100)})
        elif self.stage == 4: # Sand
            if random.random() < 0.5:
                self.particles.append({'pos': [SCREEN_W, random.randint(0, SCREEN_H)], 'vel': [random.uniform(-200, -100), random.uniform(20, 50)], 'life': 1.5, 'col': (220, 180, 100)})

        for p in self.particles[:]:
            p['pos'][0] += p['vel'][0] * dt
            p['pos'][1] += p['vel'][1] * dt
            p['life'] -= dt
            if p['life'] <= 0: self.particles.remove(p)

    def draw(self, screen, camera_x):
        # Sky Gradient
        self._draw_sky_gradient(screen)
        
        # Distant Decorations
        for d in self.decorations:
            if d.parallax < 0.5: d.draw(screen, camera_x)
        
        # Mid Decorations
        for d in self.decorations:
            if 0.5 <= d.parallax < 1.0: d.draw(screen, camera_x)

        for t in self.tiles: t.draw(screen, camera_x)
        
        # Near Decorations
        for d in self.decorations:
            if d.parallax >= 1.0: d.draw(screen, camera_x)
            
        for c in self.coins: c.draw(screen, camera_x)
        for e in self.enemies: e.draw(screen, camera_x)
        if self.flag: self.flag.draw(screen, camera_x)
        
        for i in self.items: i.draw(screen, camera_x)

        # Underwater Tint (Overlay)
        if self.stage == 1:
            tint = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            tint.fill((20, 100, 200, 40)) # Light blue tint
            screen.blit(tint, (0, 0))

        # Particles
        for p in self.particles:
            max_life = 2.0
            if self.stage == 1: max_life = 6.0
            elif self.stage == 3: max_life = 5.0
            elif self.stage == 4: max_life = 1.5
            
            alpha = max(0, min(255, int(255 * (p['life'] / max_life))))
            s = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p['col'], alpha), (2, 2), 2)
            screen.blit(s, (p['pos'][0], p['pos'][1]))

    def _draw_sky_gradient(self, screen):
        if self.stage == 1: # Premium Ocean Surface + Sky
            # Draw Sky (Top 120px)
            sky_col = (135, 206, 235)
            pygame.draw.rect(screen, sky_col, (0, 0, SCREEN_W, 120))
            # Surface Waves (More detailed)
            wave_y = 120
            for x in range(-20, SCREEN_W + 20, 20):
                off = int(8 * math.sin(x * 0.04 + self.water_timer * 2.5))
                pygame.draw.circle(screen, (255, 255, 255, 180), (x, wave_y + off + 5), 15) # Foam
                pygame.draw.rect(screen, (0, 160, 180), (x-10, wave_y + off, 22, SCREEN_H - wave_y))
            # Underwater Gradient (Deep Blue)
            c1 = (0, 100, 150)
            c2 = (0, 20, 40) # Even darker deeps
            for y in range(wave_y + 10, SCREEN_H, 4):
                f = (y - wave_y) / (SCREEN_H - wave_y)
                col = [int(c1[i]*(1-f) + c2[i]*f) for i in range(3)]
                pygame.draw.rect(screen, col, (0, y, SCREEN_W, 4))
            
            # Surface Refraction Shimmer (Fullscreen)
            shimmer = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            for y in range(wave_y, SCREEN_H, 40):
                s_off = int(20 * math.sin(y * 0.01 + self.water_timer))
                pygame.draw.rect(shimmer, (255, 255, 255, 15), (0, y + s_off, SCREEN_W, 2))
            screen.blit(shimmer, (0, 0))
        elif self.stage == 3: # Candy Land Peach-Pink Gradient
            for y in range(SCREEN_H):
                t = y / SCREEN_H
                # Peach (255, 200, 150) to Pink (255, 200, 230)
                r = 255
                g = 200
                b = int(150 + 80 * t)
                pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_W, y))
        else:
            c1 = self.sky_color
            c2 = (min(255, c1[0]+40), min(255, c1[1]+40), min(255, c1[2]+40))
            for y in range(0, SCREEN_H, 4):
                f = y / SCREEN_H
                col = [int(c1[i]*(1-f) + c2[i]*f) for i in range(3)]
                pygame.draw.rect(screen, col, (0, y, SCREEN_W, 4))
