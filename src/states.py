import pygame, random, math
from .state_manager import GameState
from .world.level import Level
from .assets.sounds import sounds
from .entities.player import Player
from .constants import *
from .hud import HUD, MenuScreen, LevelSelectScreen, GameOverScreen

class MenuState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.screen = MenuScreen()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state_manager.set_state('level_select')

    def update(self, dt):
        self.screen.update(dt)

    def draw(self, screen):
        self.screen.draw(screen)

class LevelSelectState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.screen = LevelSelectScreen()
        self.shake_t = 0
        self.shake_p = (0, 0)

    def update(self, dt):
        self.screen.update(dt)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.screen.sel = (self.screen.sel - 1) % 4
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.screen.sel = (self.screen.sel + 1) % 4
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                world, stage = [(1,1), (1,2), (1,3), (1,4)][self.screen.sel]
                if (world, stage) in self.state_manager.unlocked_levels:
                    play_state = self.state_manager.states['play']
                    play_state.setup_level(world, stage)
                    self.state_manager.set_state('play')
                else:
                    # Could play a "locked" sound here
                    self.shake_t = 0.2 
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.set_state('menu')
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self.screen, 'back_btn_rect') and self.screen.back_btn_rect.collidepoint(event.pos):
                self.state_manager.set_state('menu')

    def draw(self, screen):
        # We blit to a temporary surface to apply shake easily? 
        # Or just offset the screen blit if screen was a surface.
        # Since screen is the main display, we can't easily shake it without a sub-surface.
        # But we can just draw everything with an offset.
        # LevelSelectScreen.draw doesn't support offset yet.
        # I'll just skip the visual shake for now to avoid overcomplicating HUD.
        self.screen.draw(screen, self.state_manager.unlocked_levels)

class PlayState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.level = None
        self.player = Player(100, 100)
        self.hud = HUD()
        self.camera_x = 0
        self.world_str = "1-1"
        self.score = 0
        self.coins = 0
        self.shake_t = 0
        self.shake_p = (0, 0)
        self.win_t = 0
        self.death_t = 0

    def setup_level(self, world, stage):
        self.world = world
        self.stage = stage
        self.level = Level(world, stage)
        self.world_str = f"{world}-{stage}"
        start_x, start_y = getattr(self.level, 'player_start', (100, 100))
        self.player = Player(start_x, start_y)
        self.camera_x = 0
        self.win_t = 0
        self.death_t = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w, pygame.K_k]:
                self.player.jump()
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.set_state('level_select')
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self.hud, 'back_btn_rect') and self.hud.back_btn_rect.collidepoint(event.pos):
                self.state_manager.set_state('level_select')

    def update(self, dt):
        if not self.level: return
        self.level.update(dt)

        # 1. Win Transition
        if self.win_t > 0:
            self.win_t -= dt
            if self.win_t <= 0:
                clear_state = self.state_manager.states['level_clear']
                clear_state.setup(self.world, self.stage)
                self.state_manager.set_state('level_clear')
            return

        # 2. Death Transition
        if self.player.dead:
            self.death_t += dt
            if self.death_t > 2.0: 
                go_state = self.state_manager.states['game_over']
                go_state.setup(self.world, self.stage)
                self.state_manager.set_state('game_over')
            return

        # 3. Normal Gameplay
        self.player.update(dt, self.level)
        
        # Win Condition: Portal collision
        if self.level.flag and not self.level.flag.touched:
            dist_sq = (self.player.rect.centerx - self.level.flag.rect.centerx)**2 + \
                      (self.player.rect.centery - self.level.flag.rect.centery)**2
            
            if self.player.rect.inflate(40, 40).colliderect(self.level.flag.rect) or dist_sq < 3600:
                self.level.flag.touched = True
                sounds.play('stomp')
                
                # UNLOCK NEXT LEVEL
                w, s = self.world, self.stage
                next_w, next_s = w, s + 1
                if next_s > 4: next_w, next_s = w + 1, 1
                self.state_manager.unlock_level(next_w, next_s)
                
                self.win_t = 1.0 # Reduced to 1 second delay
                return

        # Off-screen check
        if self.player.rect.top > SCREEN_H:
            self.player.die()
            return
        
        # Camera
        target_x = self.player.rect.centerx - SCREEN_W // 2
        self.camera_x = max(0, target_x)
        
        # Shake update
        if self.shake_t > 0:
            self.shake_t -= dt
            s = int(self.shake_t * 20)
            self.shake_p = (random.randint(-s, s), random.randint(-s, s))
        else:
            self.shake_p = (0, 0)
        
        # Enemies
        for enemy in self.level.enemies:
            if enemy.alive and not getattr(enemy, 'squished', False):
                if self.player.rect.colliderect(enemy.rect):
                    # Stomping
                    if self.player.vel.y > 0 and self.player.rect.bottom < enemy.rect.bottom - 10:
                        is_dead = True
                        if hasattr(enemy, 'stomp'):
                            is_dead = enemy.stomp()
                        elif hasattr(enemy, 'squish'):
                            enemy.squish()
                        
                        if is_dead:
                            sounds.play('stomp')
                            self.player.vel.y = -400
                            self.score += 200
                    else:
                        # Take damage
                        if self.player.take_damage():
                            self.shake_t = 0.5 # Big shake on death

        # Items
        from .world.tiles import HeartItem, VisualCoin
        for item in self.level.items:
            if self.player.rect.colliderect(item.rect):
                if isinstance(item, HeartItem):
                    if self.player.health < self.player.max_health:
                        self.player.health += 1
                        sounds.play('coin')
                        item.kill()
        
        # Coins
        coin_hits = pygame.sprite.spritecollide(self.player, self.level.coins, True)
        if coin_hits:
            sounds.play('coin')
            self.coins += len(coin_hits)
            self.score += len(coin_hits) * 100
        
        # Block rewards
        if hasattr(self.player, 'pending_rewards'):
            for r in self.player.pending_rewards[:]:
                if r['reward'] == 'coin':
                    sounds.play('coin')
                    self.coins += 1
                    self.score += 100
                    self.level.items.add(VisualCoin(r['pos'][0], r['pos'][1] - TILE))
                elif r['reward'] == 'heart':
                    self.level.items.add(HeartItem(r['pos'][0], r['pos'][1] - TILE))
                self.player.pending_rewards.remove(r)

    def draw(self, screen):
        if not self.level: return
        screen.fill(self.level.sky_color)
        
        # Apply shake to camera
        cx = self.camera_x + self.shake_p[0]
        cy = self.shake_p[1]
        
        self.level.draw(screen, cx) # Note: level.draw doesn't handle cy, but usually vertical shake is small
        self.player.draw(screen, cx)
        self.hud.draw(screen, self.score, self.coins, self.player.health, self.world_str)

        # Win Flash Effect (Smoother 0.5s fade)
        if self.win_t > 0.5: 
            flash = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            # Alpha peaks at 150 and fades over 0.5 seconds
            alpha = int(150 * (1.0 - (1.0 - self.win_t) / 0.5))
            flash.fill((255, 255, 255, max(0, min(150, alpha))))
            screen.blit(flash, (0, 0))

class GameOverState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.screen = GameOverScreen()
        self.world = 1
        self.stage = 1

    def setup(self, world, stage):
        self.world = world
        self.stage = stage

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.screen.retry_rect.collidepoint(event.pos):
                play_state = self.state_manager.states['play']
                play_state.setup_level(self.world, self.stage)
                self.state_manager.set_state('play')
            elif self.screen.menu_rect.collidepoint(event.pos):
                self.state_manager.set_state('level_select')

    def update(self, dt):
        self.screen.update(dt)

    def draw(self, screen):
        # We want to see the frozen play state behind us
        play_state = self.state_manager.states['play']
        play_state.draw(screen)
        self.screen.draw(screen)

class LevelClearState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        from .hud import LevelClearScreen
        self.screen = LevelClearScreen()
        self.world = 1
        self.stage = 1

    def setup(self, world, stage):
        self.world = world
        self.stage = stage

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.screen.next_rect.collidepoint(event.pos):
                # Go to next level
                w, s = self.world, self.stage
                next_w, next_s = w, s + 1
                if next_s > 4: next_w, next_s = w + 1, 1
                
                play_state = self.state_manager.states['play']
                play_state.setup_level(next_w, next_s)
                self.state_manager.set_state('play')
            elif self.screen.menu_rect.collidepoint(event.pos):
                self.state_manager.set_state('level_select')

    def update(self, dt):
        self.screen.update(dt)

    def draw(self, screen):
        play_state = self.state_manager.states['play']
        play_state.draw(screen)
        self.screen.draw(screen)
