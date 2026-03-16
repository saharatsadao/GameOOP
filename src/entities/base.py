from abc import ABC, abstractmethod
import pygame

class Entity(pygame.sprite.Sprite, ABC):
    """Abstract base class for all game entities."""
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.alive = True

    @abstractmethod
    def update(self, dt, world):
        """Update entity state. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def draw(self, screen, camera_x):
        """Draw entity to screen. Must be implemented by subclasses."""
        pass

    def apply_physics(self, dt, gravity, max_fall):
        """Common physics application logic."""
        self.vel.y = min(self.vel.y + gravity * dt, max_fall)
        self.pos.y += self.vel.y * dt
        self.rect.y = int(self.pos.y)
