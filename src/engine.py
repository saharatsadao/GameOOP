import sys
import pygame
from .constants import *
from .state_manager import StateManager

class Engine:
    """The central game engine that manages the main loop and core systems."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state_manager = StateManager()
        from .assets.sounds import sounds
        from .states import MenuState, PlayState, LevelSelectState
        sounds.init()
        
        self.state_manager.add_state('menu', MenuState(self.state_manager))
        self.state_manager.add_state('level_select', LevelSelectState(self.state_manager))
        self.state_manager.add_state('play', PlayState(self.state_manager))
        self.state_manager.set_state('menu')
        
    def run(self):
        """Starts the main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            
            self._handle_events()
            self._update(dt)
            self._draw()
            
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.state_manager.handle_event(event)

    def _update(self, dt):
        self.state_manager.update(dt)

    def _draw(self):
        self.state_manager.draw(self.screen)
        pygame.display.flip()
