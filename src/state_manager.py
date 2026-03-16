import pygame
from .constants import *

class GameState:
    """Abstract base class for all game states."""
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

class StateManager:
    """Manages switching between different game states."""
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.unlocked_levels = {(1, 1)} # Store as (world, stage)

    def unlock_level(self, world, stage):
        self.unlocked_levels.add((world, stage))

    def add_state(self, name, state):
        self.states[name] = state

    def set_state(self, name):
        if name in self.states:
            self.current_state = self.states[name]
        else:
            print(f"Error: State '{name}' not found.")

    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)
