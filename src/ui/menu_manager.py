"""
Menu management module handling game menus and UI interactions.
"""

import os
import pygame
import pytmx
from pygame import Rect

from src.utils.menu_config import (
    MENU_TEXT, BUTTON_REGIONS, LAYER_CONFIG,
    FONTS, COLORS, SYSTEM_FONTS
)

class MenuManager:
    """
    Manages game menus, including rendering and interaction handling.
    Supports multiple menu screens with TMX-based layouts.
    """
    
    def __init__(self, screen):
        """
        Initialize menu manager
        
        Args:
            screen: Pygame surface to draw menus on
        """
        self.screen = screen
        self.current_menu = "main"
        self.active_button = None
        self.debug_mode = False
        
        # Load TMX maps and initialize fonts
        self._load_tmx_maps()
        self._init_fonts()
        
        # Initialize buttons with pygame Rects
        self.buttons = self._init_buttons()
        
        # Get sorted layer order
        self.layer_order = sorted(
            LAYER_CONFIG.keys(),
            key=lambda x: LAYER_CONFIG[x]['order']
        )

    def _load_tmx_maps(self):
        """Load and verify TMX map files"""
        try:
            self.main_menu_map = self._load_tmx_file("main_menu.tmx")
            self.sp_menu_map = self._load_tmx_file("sp_menu.tmx")
            
            if self.debug_mode:
                print("Successfully loaded TMX files")
                print(f"Main menu layers: {list(self.main_menu_map.layernames.keys())}")
                print(f"SP menu layers: {list(self.sp_menu_map.layernames.keys())}")
                
        except Exception as e:
            print(f"Error loading TMX files: {e}")
            raise

    def _load_tmx_file(self, filename):
        """Load a single TMX file"""
        tmx_path = os.path.join("assets", "UI", filename)
        if not os.path.exists(tmx_path):
            raise FileNotFoundError(f"Could not find {tmx_path}")
        return pytmx.load_pygame(tmx_path)

    def _init_fonts(self):
        """Initialize fonts with Vietnamese support"""
        self.fonts = {}
        font_loaded = False
        
        for font_name in SYSTEM_FONTS:
            try:
                # Test font with Vietnamese text
                test_font = pygame.font.SysFont(font_name, FONTS['title']['size'])
                test_render = test_font.render("Tiếng Việt", True, (0,0,0))
                
                if test_render:
                    # Initialize all font sizes
                    self.fonts['title'] = pygame.font.SysFont(
                        font_name, FONTS['title']['size']
                    )
                    self.fonts['menu'] = pygame.font.SysFont(
                        font_name, FONTS['menu']['size']
                    )
                    self.fonts['content'] = pygame.font.SysFont(
                        font_name, FONTS['content']['size']
                    )
                    
                    if self.debug_mode:
                        print(f"Using system font: {font_name}")
                    font_loaded = True
                    break
            except:
                continue
        
        if not font_loaded:
            self._init_fallback_fonts()

    def _init_fallback_fonts(self):
        """Initialize fallback fonts if no system fonts work"""
        print("No suitable Vietnamese font found, using default")
        for font_type, config in FONTS.items():
            self.fonts[font_type] = pygame.font.Font(None, config['size'])

    def _init_buttons(self):
        """Initialize button rectangles for all menus"""
        buttons = {}
        for menu_name, button_list in BUTTON_REGIONS.items():
            buttons[menu_name] = [
                {
                    "rect": Rect(*button["rect"]),
                    "action": button["action"],
                    "hover": False
                }
                for button in button_list
            ]
        return buttons

    def draw_layer(self, tmx_map, layer_name):
        """
        Draw a specific TMX layer
        
        Args:
            tmx_map: TMX map object containing the layer
            layer_name: Name of the layer to draw
        """
        if layer_name not in tmx_map.layernames:
            if self.debug_mode:
                print(f"Layer '{layer_name}' not found in map")
            return

        layer = tmx_map.layernames[layer_name]
        config = LAYER_CONFIG[layer_name]
        
        # Get layer offset
        offset_x = layer.offsetx if hasattr(layer, 'offsetx') and config['use_offset'] else 0
        offset_y = layer.offsety if hasattr(layer, 'offsety') and config['use_offset'] else 0
        
        if self.debug_mode:
            print(f"Drawing layer '{layer_name}' with offset ({offset_x}, {offset_y})")
        
        # Create layer surface
        layer_surface = pygame.Surface((925, 725), pygame.SRCALPHA)
        
        # Draw tiles
        for x, y, gid in layer:
            if gid:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    pos_x = x * tmx_map.tilewidth + offset_x
                    pos_y = y * tmx_map.tileheight + offset_y
                    layer_surface.blit(tile, (pos_x, pos_y))
        
        # Apply alpha and draw
        layer_surface.set_alpha(config['alpha'])
        self.screen.blit(layer_surface, (0, 0))

    def draw_text(self, text, pos, font_type='menu', color=None):
        """
        Draw centered text
        
        Args:
            text: Text to draw
            pos: Position tuple (x, y)
            font_type: Type of font to use ('title', 'menu', or 'content')
            color: Text color tuple (r,g,b)
        """
        if color is None:
            color = COLORS['normal']
            
        text_surface = self.fonts[font_type].render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        """Draw current menu screen"""
        # Clear screen
        self.screen.fill(COLORS['background'])
        
        # Select appropriate map
        tmx_map = self.main_menu_map if self.current_menu == "main" else self.sp_menu_map
        
        if self.debug_mode:
            print(f"\nDrawing {self.current_menu} menu")
        
        # Draw layers
        for layer_name in self.layer_order:
            if not (layer_name == "bong" and self.current_menu == "main"):
                self.draw_layer(tmx_map, layer_name)
        
        # Draw menu content
        self._draw_menu_content()

    def _draw_menu_content(self):
        """Draw menu text and buttons"""
        menu_content = MENU_TEXT[self.current_menu]
        
        # Draw title
        self.draw_text(
            menu_content["title"]["text"],
            menu_content["title"]["pos"],
            'title'
        )
        
        # Draw content if available
        if "content" in menu_content:
            for content_item in menu_content["content"]:
                self.draw_text(
                    content_item["text"],
                    content_item["pos"],
                    'content'
                )
        
        # Draw buttons with hover effects
        self._draw_buttons(menu_content)

    def _draw_buttons(self, menu_content):
        """Draw menu buttons with hover effects"""
        mouse_pos = pygame.mouse.get_pos()
        
        for i, button in enumerate(menu_content["buttons"]):
            button_info = self.buttons[self.current_menu][i]
            
            # Determine button color based on state
            color = COLORS['normal']
            if button_info["rect"].collidepoint(mouse_pos):
                color = COLORS['hover']
            if self.active_button == button_info:
                color = COLORS['click']
            
            self.draw_text(button["text"], button["pos"], 'menu', color)

    def handle_click(self, pos):
        """
        Handle mouse click events
        
        Args:
            pos: Mouse position tuple (x, y)
            
        Returns:
            str or None: Action to take ('start_game', 'exit', or None)
        """
        buttons = self.buttons[self.current_menu]
        
        for button in buttons:
            if button["rect"].collidepoint(pos):
                self.active_button = button
                action = button["action"]
                
                if action == "start_game":
                    return "start_game"
                elif action == "exit":
                    return "exit"
                elif action in ["rules", "developers", "main"]:
                    if self.debug_mode:
                        print(f"Switching to {action} menu")
                    self.current_menu = action
                break
        
        return None

    def set_debug(self, enabled):
        """Enable or disable debug mode"""
        self.debug_mode = enabled
