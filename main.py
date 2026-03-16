from src.engine import Engine
from src.states import MenuState, LevelSelectState, PlayState, GameOverState, LevelClearState

def main():
    engine = Engine()
    
    # Initialize States
    menu_state = MenuState(engine.state_manager)
    play_state = PlayState(engine.state_manager)
    level_select_state = LevelSelectState(engine.state_manager)
    game_over_state = GameOverState(engine.state_manager)
    level_clear_state = LevelClearState(engine.state_manager)
    
    engine.state_manager.add_state('menu', menu_state)
    engine.state_manager.add_state('play', play_state)
    engine.state_manager.add_state('level_select', level_select_state)
    engine.state_manager.add_state('game_over', game_over_state)
    engine.state_manager.add_state('level_clear', level_clear_state)
    
    # Set Initial State
    engine.state_manager.set_state('menu')
    
    engine.run()

if __name__ == "__main__":
    main()
