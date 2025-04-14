"""Menu management module"""

import os
import pygame
import logging
from pygame import Rect, Surface
from typing import Dict, List, Optional, Tuple, Any

from src.utils.logger_config import get_logger
from src.utils.asset_loader import get_asset_loader
from src.utils.event_handler import get_event_handler, GameEvent
from src.utils.geometry import (
    rect_from_center, point_in_rect, interpolate_points
)
from src.utils.menu_config import (
    MENU_TEXT, BUTTON_REGIONS, LAYER_CONFIG,
    FONTS, COLORS, SYSTEM_FONTS
)

logger = get_logger(__name__)

class MenuManager:
    """Handles menu management and rendering"""
    
    def __init__(self, screen: Surface):
        """Initialize menu manager"""
        self.screen = screen
        self.asset_loader = get_asset_loader()
        self.event_handler = get_event_handler()
        
        # Menu state
        self.current_menu = "main"
        self.active_button = None
        self.hover_button = None
        self.transition_effect = None
        
        # Input state
        self.player_names = ["", "", "", ""]
        self.active_input = 0
        
        # Initialize state flags
        self.initialized = False
        self.debug_mode = False

        # Initialize buttons
        self._init_buttons()

        # Load assets
        self._load_assets()

    def initialize(self) -> None:
        """Initialize menu system"""
        if self.initialized:
            return
            
        try:
            self._load_assets()
            self._init_buttons()
            self._setup_event_handlers()
            self.initialized = True
            logger.info("Menu system initialized")
        except Exception as e:
            logger.error(f"Failed to initialize menu system: {e}")
            raise

    def _load_assets(self) -> None:
        """Load menu assets"""
        logger.info("Starting asset loading...")
        try:
            # Load TMX maps
            logger.info("Loading TMX maps...")
            self.main_menu_map = self.asset_loader.load_tmx("maps/assets_ver1/main_menu.tmx")
            if not self.main_menu_map:
                raise RuntimeError("Failed to load main menu map")
            
            self.sp_menu_map = self.asset_loader.load_tmx("maps/assets_ver1/sp_menu.tmx")
            if not self.sp_menu_map:
                raise RuntimeError("Failed to load sp menu map")
            logger.info("TMX maps loaded successfully")
            
            # Render backgrounds
            logger.info("Rendering backgrounds...")
            self.backgrounds = {}
            main_bg = self._render_tmx(self.main_menu_map)
            sp_bg = self._render_tmx(self.sp_menu_map)
            
            if not main_bg or not sp_bg:
                raise RuntimeError("Failed to render backgrounds")
            
            # Store backgrounds
            self.backgrounds.update({
                'main': main_bg,
                'rules': sp_bg,
                'developers': sp_bg,
                'name_input': sp_bg
            })
            logger.info("Asset loading completed successfully")
            
        except Exception as e:
            logger.error(f"Asset loading failed: {e}")
            self.backgrounds = {}
            raise
    def _init_buttons(self) -> None:
        """Initialize menu buttons"""
        self.buttons = {}
        for menu_name, regions in BUTTON_REGIONS.items():
            self.buttons[menu_name] = [
                {
                    'rect': Rect(*region['rect']),
                    'action': region['action'],
                    'hover': False,
                    'active': False
                }
                for region in regions
            ]

    def _setup_event_handlers(self) -> None:
        """Set up menu event handlers"""
        self.event_handler.add_pygame_handler(
            pygame.MOUSEMOTION,
            self._handle_mouse_motion
        )
        self.event_handler.add_pygame_handler(
            pygame.MOUSEBUTTONDOWN,
            self._handle_mouse_click
        )
        self.event_handler.add_pygame_handler(
            pygame.KEYDOWN,
            self._handle_key_press
        )

    def show_error_screen(self, title: str, error_msg: str,
                         help_messages: Optional[List[str]] = None) -> None:
        """Display error message screen"""
        try:
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            
            # Create semi-transparent overlay
            overlay = Surface((screen_width, screen_height))
            overlay.fill(COLORS['error_bg'])
            overlay.set_alpha(200)
            self.screen.blit(overlay, (0, 0))
            
            # Draw error content
            y = screen_height // 4
            
            # Draw title
            y += self._draw_text(title, y, font_type='title',
                               color=COLORS['error_text'])
            y += 20
            
            # Draw error message
            if error_msg:
                y += self._draw_text(error_msg, y, color=COLORS['error_text'])
                y += 30
            
            # Draw help messages
            if help_messages:
                for msg in help_messages:
                    y += self._draw_text(msg, y, font_type='content')
                    y += 10
            
            pygame.display.flip()
            
            # Wait for input
            self._wait_for_input()
            
        except Exception as e:
            logger.error(f"Error displaying error screen: {e}")

    def _draw_text(self, text: str, y: int, font_type: str = 'menu',
                   color: Optional[Tuple[int, int, int]] = None,
                   x: Optional[int] = None) -> int:
        """
        Draw text at specified position
        
        Args:
            text: Text to draw
            y: Vertical position
            font_type: Font type from FONTS config
            color: Text color (optional)
            x: Horizontal position (optional, will center if not provided)
            
        Returns:
            int: Height of rendered text
        """
        color = color or COLORS['text']
        font = self.asset_loader.load_font(FONTS[font_type]['name'],
                                         FONTS[font_type]['size'])
        text_surface = font.render(text, True, color)
        
        # Center text if x not provided
        actual_x = x if x is not None else (self.screen.get_width() - text_surface.get_width()) // 2
            
        self.screen.blit(text_surface, (actual_x, y))
        return text_surface.get_height()

    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Handle mouse motion events"""
        if not self.initialized:
            return
            
        # Update button hover states
        for button in self.buttons.get(self.current_menu, []):
            was_hover = button['hover']
            is_hover = button['rect'].collidepoint(event.pos)
            
            if is_hover != was_hover:
                button['hover'] = is_hover
                if is_hover:
                    self.hover_button = button
                    self.event_handler.trigger_game_event(
                        GameEvent.SOUND_TOGGLE,
                        sound='hover'
                    )
                elif button == self.hover_button:
                    self.hover_button = None

    def _handle_mouse_click(self, event: pygame.event.Event) -> Optional[Any]:
        """Handle mouse click events"""
        if not self.initialized:
            return None
            
        if event.button == 1:  # Left click
            # Handle menu-specific clicks
            if self.current_menu == "name_input":
                return self._handle_name_input_click(event.pos)
            else:
                return self._handle_menu_click(event.pos)
        return None

    def _handle_menu_click(self, pos: Tuple[int, int]) -> Optional[Any]:
        """Handle menu button clicks"""
        for button in self.buttons.get(self.current_menu, []):
            if button['rect'].collidepoint(pos):
                self.active_button = button
                action = button['action']
                
                self.event_handler.trigger_game_event(
                    GameEvent.SOUND_TOGGLE,
                    sound='click'
                )
                
                if action == "start_game":
                    self.current_menu = "name_input"
                    self.event_handler.trigger_game_event(
                        GameEvent.MENU_CHANGE,
                        screen="name_input"
                    )
                elif action == "exit":
                    return False
                elif action in ["rules", "developers", "main", "start"]:
                    self.current_menu = action
                    self.event_handler.trigger_game_event(
                        GameEvent.MENU_CHANGE,
                        screen=action
                    )
                
                self.draw()
                pygame.display.flip()
                break
        return None

    def _handle_name_input_click(self, pos: Tuple[int, int]) -> Optional[List[str]]:
        """Handle clicks in name input screen"""
        if self.buttons["name_input"][0]["rect"].collidepoint(pos):  # Back
            self.current_menu = "main"
            return None
            
        if self.buttons["name_input"][1]["rect"].collidepoint(pos):  # OK
            if all(name.strip() for name in self.player_names):
                return self.player_names
            return None
            
        # Check input field clicks
        for i, rect in enumerate(self._get_input_rects()):
            if rect.collidepoint(pos):
                self.active_input = i
                break
                
        return None

    def _get_input_rects(self) -> List[Rect]:
        """Get rectangles for input fields"""
        rects = []
        y = 150
        for _ in range(4):
            rects.append(Rect(400, y, 200, 30))
            y += 50
        return rects

    def _handle_key_press(self, event: pygame.event.Event) -> None:
        """Handle keyboard input"""
        if self.current_menu != "name_input":
            return
            
        if event.key == pygame.K_TAB:
            self.active_input = (self.active_input + 1) % 4
        elif event.key == pygame.K_BACKSPACE:
            self.player_names[self.active_input] = \
                self.player_names[self.active_input][:-1]
        elif event.unicode.isprintable():
            if len(self.player_names[self.active_input]) < 15:
                self.player_names[self.active_input] += event.unicode

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle user input events and delegate to specific handlers"""
        if event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
        elif event.type == pygame.KEYDOWN:
            self._handle_key_press(event)

    def update(self) -> None:
        """Update menu state"""
        if not self.initialized:
            return
        
        # Update any animations or transitions
        if self.transition_effect:
            self.transition_effect.update()
            if self.transition_effect.is_complete:
                self.transition_effect = None

    def draw(self) -> None:
        """Draw current menu state"""
        if not self.initialized:
            return
            
        # Draw background
        self._draw_background()
        
        # Draw menu content
        menu_content = MENU_TEXT[self.current_menu]
        
        # Draw title
        title_config = menu_content["title"]
        self._draw_text(
            title_config["text"],
            title_config["pos"][1],
            'title',
            x=title_config["pos"][0]
        )
        
        # Draw content if any
        if "content" in menu_content:
            for item in menu_content["content"]:
                self._draw_text(
                    item["text"],
                    item["pos"][1],
                    'content'
                )
        
        # Draw buttons
        self._draw_buttons()

    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Handle click events on the menu.

        Args:
            pos: The position of the mouse click.

        Returns:
            str or None: The action associated with the clicked button, if any.
        """
        logger.info(f"Handling click at position: {pos}")
        result = self._handle_menu_click(pos)
        if result is not None:
            return result
        
        if self.current_menu == "name_input":
            return self._handle_name_input_click(pos)
        
        return None
        
        # Draw transition effect if active
        if self.transition_effect:
            self.transition_effect.draw(self.screen)

    def _draw_background(self) -> None:
        """Draw menu background"""
        bg = self.backgrounds.get(self.current_menu)
        if bg:
            self.screen.blit(bg, (0, 0))
            pygame.display.flip()

    def _draw_buttons(self) -> None:
        """Draw menu buttons"""
        mouse_pos = pygame.mouse.get_pos()
        menu_content = MENU_TEXT[self.current_menu]
        
        for i, button_config in enumerate(menu_content.get("buttons", [])):
            button = self.buttons[self.current_menu][i]
            
            # Determine button color
            color = COLORS['normal']
            if button['hover']:
                color = COLORS['hover']
            if button == self.active_button:
                color = COLORS['click']
            
            # Draw button text at exact position
            text_pos = button_config["pos"]
            self._draw_text(
                button_config["text"],
                text_pos[1],  # y position
                color=color,
                x=text_pos[0]  # x position
            )
def _render_tmx(self, tmx_map: Any) -> Optional[Surface]:
    """
    Render a TMX map to a surface
    
    Args:
        tmx_map: The TMX map to render
        
    Returns:
        Surface or None: Rendered surface or None if rendering failed
    """
    try:
        if tmx_map is None:
            logger.error("Cannot render None TMX map")
            return None
            
        width = int(float(tmx_map.width) * float(tmx_map.tilewidth))
        height = int(float(tmx_map.height) * float(tmx_map.tileheight))
        surface = Surface((width, height))
        
        # Draw layers in order
        for layer_name in sorted(LAYER_CONFIG,
                              key=lambda x: LAYER_CONFIG[x]['order']):
            if layer_name in tmx_map.layernames:
                self._draw_layer(surface, tmx_map, layer_name)
                
        return surface
        
    except Exception as e:
        logger.error(f"Error rendering TMX map: {e}")
        return None

    def _draw_layer(self, surface: Surface, tmx_map: Any, layer_name: str) -> None:
        """Draw a single TMX layer"""
        try:
            layer = tmx_map.layernames[layer_name]
            config = LAYER_CONFIG[layer_name]
            
            # Calculate offsets
            offset_x = 0
            offset_y = 0
            
            if config.get('use_offset', False):
                # Handle x offset
                if hasattr(layer, 'offsetx'):
                    try:
                        offset_x = int(float(str(layer.offsetx)))
                    except (ValueError, TypeError):
                        offset_x = 0
                
                # Handle y offset
                if hasattr(layer, 'offsety'):
                    try:
                        offset_y = int(float(str(layer.offsety)))
                    except (ValueError, TypeError):
                        offset_y = 0
            
            # Create layer surface
            layer_surface = Surface((surface.get_width(),
                                surface.get_height()),
                                pygame.SRCALPHA)
            
            # Draw tiles
            for x, y, gid in layer:
                if gid:
                    tile = tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        pos_x = x * tmx_map.tilewidth + offset_x
                        pos_y = y * tmx_map.tileheight + offset_y
                        layer_surface.blit(tile, (pos_x, pos_y))
            
            # Apply alpha and blit to main surface
            layer_surface.set_alpha(config['alpha'])
            surface.blit(layer_surface, (0, 0))
            
        except Exception as e:
            logger.error(f"Error drawing layer {layer_name}: {e}")
            logger.error(f"Error drawing layer {layer_name}: {e}")
        surface.blit(layer_surface, (0, 0))

    def _wait_for_input(self, timeout: int = 30000) -> None:
        """
        Wait for user input
        
        Args:
            timeout: Maximum wait time in milliseconds
        """
        start_time = pygame.time.get_ticks()
        waiting = True
        
        while waiting and pygame.time.get_ticks() - start_time < timeout:
            for event in pygame.event.get():
                if event.type in [pygame.QUIT, pygame.KEYDOWN,
                                pygame.MOUSEBUTTONDOWN]:
                    waiting = False
            pygame.time.wait(100)

# Global menu manager instance
_menu_manager = None

def get_menu_manager(screen: Optional[Surface] = None) -> MenuManager:
    """Get or create the global menu manager instance"""
    global _menu_manager
    if _menu_manager is None:
        if screen is None:
            raise ValueError("Screen surface required for menu manager initialization")
        _menu_manager = MenuManager(screen)
    return _menu_manager
