# Ludo Game API Documentation

## Core Package

### GameController

The main controller managing game flow and state transitions.

```python
class GameController:
    def __init__():
        """Initialize the game controller"""
    
    def run_game() -> None:
        """Main game control loop"""
```

### MainBoard

Handles game board management and menu transitions.

```python
class MainBoard:
    def __init__():
        """Initialize the game board"""
    
    def run() -> Optional[List[str]]:
        """Run the board and return player names or None if quit"""
```

## Entities Package

### Pawn

Represents a game piece with movement and animation.

```python
class Pawn(pygame.sprite.Sprite):
    def __init__(surface: Surface, path_positions: Dict[int, Tuple[int, int]],
                start_pos: Tuple[int, int], number: int):
        """Initialize a pawn"""
    
    def move(dice: int, statekeeper: Statekeep) -> None:
        """Move pawn according to dice roll"""
    
    def update_animation() -> None:
        """Update pawn animation state"""
```

### Player

Manages player state and actions.

```python
class Player:
    def __init__(name: str, color: str, pawns: List[Pawn]):
        """Initialize a player"""
    
    def turn() -> None:
        """Handle player's turn"""
    
    def dice_roll() -> int:
        """Roll dice and return total"""
```

### Star

Special board items providing effects.

```python
class Star(pygame.sprite.Sprite):
    def __init__(position: Tuple[int, int]):
        """Initialize a star"""
    
    def apply_effect(pawn: Pawn, statekeeper: Statekeep) -> str:
        """Apply effect to pawn"""
```

### Statekeep

Central game state manager.

```python
class Statekeep:
    def __init__():
        """Initialize game state"""
    
    def update() -> None:
        """Update all game state components"""
```

## UI Package

### AlertManager

Manages in-game notifications.

```python
class AlertManager:
    def add_alert(message: str, duration: int = 2000) -> None:
        """Add a new alert"""
    
    def update() -> None:
        """Update alert states"""
```

### MenuManager

Handles game menus and navigation.

```python
class MenuManager:
    def __init__(screen: Surface):
        """Initialize menu manager"""
    
    def draw() -> None:
        """Draw current menu state"""
```

### SoundManager

Controls game audio.

```python
class SoundManager:
    def play_sound(sound_name: str) -> bool:
        """Play a sound by name"""
    
    def set_volume(volume: float) -> None:
        """Set master volume level"""
```

## Utils Package

### AssetLoader

Manages game assets.

```python
class AssetLoader:
    def load_image(path: str, alpha: bool = True) -> Optional[Surface]:
        """Load an image with caching"""
    
    def load_sprite_sheet(path: str, tile_size: Tuple[int, int],
                         colorkey: Optional[Tuple[int, int, int]] = None) -> Dict[int, Surface]:
        """Load a sprite sheet"""
```

### EventHandler

Manages game events.

```python
class EventHandler:
    def add_game_handler(event_type: GameEvent, handler: Callable) -> None:
        """Add a game event handler"""
    
    def trigger_game_event(event_type: GameEvent, **kwargs: Any) -> None:
        """Trigger a game event"""
```

### GameLogger

Configures logging.

```python
class GameLogger:
    def initialize(log_level: str = 'INFO',
                  log_to_file: bool = True,
                  log_to_console: bool = True) -> None:
        """Initialize logging system"""
```

## Events

Game events used for communication between components:

```python
class GameEvent(Enum):
    GAME_START = auto()
    GAME_PAUSE = auto()
    GAME_RESUME = auto()
    GAME_QUIT = auto()
    TURN_START = auto()
    TURN_END = auto()
    PAWN_MOVE = auto()
    PAWN_CAPTURE = auto()
    DICE_ROLL = auto()
    PLAYER_WIN = auto()
    STAR_EFFECT = auto()
    MENU_CHANGE = auto()
    SOUND_TOGGLE = auto()
```

## Usage Examples

### Starting the Game

```python
from src.core.game_controller import GameController

def main():
    controller = GameController()
    controller.run_game()
```

### Handling Events

```python
from src.utils.event_handler import get_event_handler, GameEvent

def on_pawn_move(pawn, distance):
    print(f"Pawn moved {distance} spaces")

event_handler = get_event_handler()
event_handler.add_game_handler(GameEvent.PAWN_MOVE, on_pawn_move)
```

### Loading Assets

```python
from src.utils.asset_loader import get_asset_loader

asset_loader = get_asset_loader()
image = asset_loader.load_image('assets/pawn.png')
animations = asset_loader.load_sprite_sheet('assets/animations.png', (32, 32))
```

### Playing Sounds

```python
from src.ui.sound_manager import get_sound_manager

sound_manager = get_sound_manager()
sound_manager.play_sound('dice_roll')
```

### Showing Alerts

```python
from src.ui.alert_manager import get_alert_manager

alert_manager = get_alert_manager()
alert_manager.add_alert("Player 1's turn", duration=2000)
```

## Best Practices

1. Always use the singleton getters (`get_*`) to access managers
2. Handle errors appropriately using try/except
3. Use type hints for better code clarity
4. Log important events and errors
5. Use constants from `constants.py` instead of hard-coded values
6. Follow the event-driven pattern for component communication
7. Clean up resources when done using them