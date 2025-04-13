"""Main board module for managing game board and menus"""

import pygame
import sys
import pytmx
import os
import logging
import traceback
from pygame.locals import *
from pytmx.util_pygame import load_pygame

from src.utils.constants import (
    COLORS, TMX_CONFIG, BUTTON_POSITIONS,
    BUTTON_TEXT, GAME_RULES
)

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class MainBoard:
    """Main board class handling game menus and initialization"""
    
    @staticmethod
    def resolve_path(path, base=None):
        """Resolve file path, handling both absolute and relative paths"""
        if os.path.isabs(path):
            return path
        if base is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.normpath(os.path.join(base, path))

    def verify_tileset(self, tmx_path, tileset_source):
        """Verify a single tileset exists"""
        tileset_path = self.resolve_path(tileset_source, os.path.dirname(tmx_path))
        if not os.path.exists(tileset_path):
            raise FileNotFoundError(f"Tileset not found: {tileset_source} (looking in {tileset_path})")
        logger.debug(f"✓ Found tileset: {tileset_source}")
        return tileset_path

    def _create_font(self, size, font_name="tahoma"):
        """Create a font with fallback"""
        try:
            return pygame.font.SysFont(font_name, size)
        except pygame.error:
            return pygame.font.Font(None, size)

    def _render_text_with_shadow(self, text, font, color, surface, pos, shadow_color=None, shadow_offset=1):
        """Render text with a shadow effect"""
        if shadow_color is None:
            if isinstance(color, (tuple, list)) and len(color) >= 3:
                shadow_color = (*color[:3], 128)
            else:
                shadow_color = COLORS['error_detail'][:3] + (128,)

        shadow = font.render(text, True, shadow_color)
        text_surface = font.render(text, True, color)

        surface.blit(shadow, (pos[0] + shadow_offset, pos[1] + shadow_offset))
        surface.blit(text_surface, pos)
        
        return text_surface.get_height()

    def _draw_error_pattern(self, surface, color, spacing=20, alpha=30):
        """Draw a diagonal error pattern on a surface"""
        pattern_color = (*color[:3], alpha)
        width, height = surface.get_size()
        
        for i in range(0, width + height, spacing):
            start_pos = (max(0, i - height), min(i, height))
            end_pos = (min(i, width), max(0, i - width))
            pygame.draw.line(surface, pattern_color, start_pos, end_pos)

    def show_error_screen(self, title, error_msg, help_messages=None):
        """Display an error screen with the given message"""
        try:
            screen = pygame.display.set_mode((800, 400))
            pygame.display.set_caption("Ludo Game - Error")
            screen.fill(COLORS['error_bg'])
            
            font = self._create_font(20)
            font_bold = self._create_font(24, bold=True)
            
            # Draw title
            title_shadow = font_bold.render(title, True, COLORS['error_detail'])
            title_surface = font_bold.render(title, True, COLORS['error_text'])
            
            title_x = 400 - title_surface.get_width() // 2
            title_y = 50
            screen.blit(title_shadow, (title_x + 2, title_y + 2))
            screen.blit(title_surface, (title_x, title_y))
            
            # Prepare messages
            messages = []
            if error_msg:
                messages.extend([error_msg, ""])
            if help_messages:
                messages.extend(help_messages)
            messages.extend(["", "Press any key to exit"])
            
            # Draw messages
            y = 120
            for msg in messages:
                if not msg:
                    y += 15
                    continue
                
                text = font.render(msg, True, COLORS['text'])
                x = 400 - text.get_width() // 2 if not msg[0].isspace() else 50
                screen.blit(text, (x, y))
                y += 30
            
            pygame.display.flip()
            
            # Wait for input
            start_time = pygame.time.get_ticks()
            waiting = True
            while waiting and pygame.time.get_ticks() - start_time < 30000:
                for event in pygame.event.get():
                    if event.type in [QUIT, KEYDOWN]:
                        waiting = False
                pygame.time.wait(100)
                
        except Exception as e:
            logger.error(f"Failed to show error screen: {e}")
            print("\n" + "="*60)
            print(f"ERROR: {title}")
            print("-"*60)
            print(f"Details: {error_msg}")
            if help_messages:
                print("\nHelp:")
                for msg in help_messages:
                    print(msg)
            print("="*60 + "\n")
        
        pygame.quit()
        sys.exit(1)

    def __init__(self):
        """Initialize the main board"""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Ludo King - Cờ Cá Ngựa")
        
        # Initialize main variables
        self.tmx_data = {}
        self.backgrounds = {}
        self.buttons = {name: pygame.Rect(*rect) for name, rect in BUTTON_POSITIONS.items()}
        self.player_names = ["", "", "", ""]
        self.show_name_input = False
        self.show_rules = False
        self.show_developers = False
        self.active_input = 0
        
        try:
            self._init_tmx()
            self._init_fonts()
        except Exception as e:
            self._handle_init_error(e)

    def _init_tmx(self):
        """Initialize TMX maps and backgrounds"""
        logger.info("Starting TMX initialization")
        
        # Monkey patch pytmx to handle float values
        self._patch_pytmx_types()
        
        # Process TMX files
        for name, config in TMX_CONFIG.items():
            path = self.resolve_path(config['path'])
            logger.info(f"Processing {name}.tmx...")
            
            self._verify_and_load_tmx(name, path, config)
        
        logger.info("TMX initialization complete")

    def _patch_pytmx_types(self):
        """Patch pytmx types to handle float values"""
        import pytmx.pytmx
        
        def safe_int(value):
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return 0

        pytmx.pytmx.types.update({
            'x': float, 'y': float,
            'width': safe_int, 'height': safe_int,
            'tilewidth': safe_int, 'tileheight': safe_int,
            'spacing': safe_int, 'margin': safe_int,
            'repeatx': safe_int, 'repeaty': safe_int,
            'gid': safe_int, 'firstgid': safe_int,
            'id': safe_int, 'version': str,
            'tiledversion': str, 'orientation': str,
            'renderorder': str, 'compressionlevel': safe_int,
            'infinite': bool, 'nextlayerid': safe_int,
            'nextobjectid': safe_int, 'parallaxx': float,
            'parallaxy': float, 'offsetx': float,
            'offsety': float, 'opacity': float,
        })

    def _verify_and_load_tmx(self, name, path, config):
        """Verify and load a TMX file"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"TMX file not found: {path}")
        
        # Verify tileset paths
        self._verify_tileset_paths(path)
        
        # Load TMX
        tmx = pytmx.load_pygame(path)
        
        # Verify required layers
        found_layers = {l.name for l in tmx.visible_layers if hasattr(l, 'name')}
        required_layers = set(config['required_layers'])
        missing = required_layers - found_layers
        if missing:
            raise ValueError(f"Missing required layers in {name}.tmx: {missing}")
        
        # Store TMX data and create background
        self.tmx_data[name] = tmx
        self.backgrounds[name] = self.render_tmx(tmx)
        
        # Set up references for backward compatibility
        if name == 'main_menu':
            self.main_menu_tmx = tmx
            self.main_menu_bg = self.backgrounds[name]
        elif name == 'sp_menu':
            self.sp_menu_tmx = tmx
            self.sp_menu_bg = self.backgrounds[name]

    def _init_fonts(self):
        """Initialize fonts with Vietnamese support"""
        system_fonts = [
            "arial", "segoeui", "tahoma", "calibri",
            "notosans", "roboto", "times new roman"
        ]
        
        font_loaded = False
        for font_name in system_fonts:
            try:
                self.font = pygame.font.SysFont(font_name, 74)
                test_render = self.font.render("Tiếng Việt", True, (0,0,0))
                if test_render:
                    self.small_font = pygame.font.SysFont(font_name, 36)
                    self.content_font = pygame.font.SysFont(font_name, 28)
                    logger.info(f"Using system font: {font_name}")
                    font_loaded = True
                    break
            except:
                continue
        
        if not font_loaded:
            logger.warning("No suitable Vietnamese font found, using default")
            self.font = pygame.font.Font(None, 74)
            self.small_font = pygame.font.Font(None, 36)
            self.content_font = pygame.font.Font(None, 28)
        
        self.error_font = pygame.font.SysFont("arial", 24, bold=True)

    def _handle_init_error(self, error):
        """Handle initialization errors"""
        if isinstance(error, FileNotFoundError):
            self.show_error_screen(
                "Missing Game Resources",
                str(error),
                [
                    "Missing game resources. Please check:",
                    "",
                    "1. Game installation directory structure:",
                    f"   - {os.path.dirname(TMX_CONFIG['main_menu']['path'])} folder exists",
                    "   - All TMX files are present",
                    "   - All tileset images are in place",
                    "",
                    "Try reinstalling the game if the issue persists."
                ]
            )
        elif isinstance(error, ValueError):
            self.show_error_screen(
                "Invalid Resource Format",
                "Game resource files are invalid or corrupted",
                [f"Error: {str(error)}", "", "Please verify game files or reinstall."]
            )
        else:
            self.show_error_screen(
                "System Error",
                "Game initialization failed",
                [f"Error: {str(error)}", "", "Please check the game log for details."]
            )

    def draw_main_menu(self):
        """Draw the main menu screen"""
        self.screen.blit(self.main_menu_bg, (0, 0))
        
        # Draw title
        title = self.font.render("LUDO", True, COLORS['text'])
        title_x = 420 - title.get_width() // 2
        title_y = 60
        self.screen.blit(title, (title_x, title_y))
        
        # Draw buttons
        for btn_name, btn_rect in self.buttons.items():
            if btn_name not in ["ok", "back"]:
                text = self.small_font.render(BUTTON_TEXT[btn_name], True, COLORS['text'])
                text_x = btn_rect.centerx - text.get_width() // 2
                text_y = btn_rect.centery - text.get_height() // 2
                self.screen.blit(text, (text_x, text_y))

    def draw_developers(self):
        """Draw the developers screen"""
        self.screen.blit(self.sp_menu_bg, (0, 0))
        
        title = self.font.render("Nhà phát triển", True, COLORS['text'])
        self.screen.blit(title, (400 - title.get_width() // 2, 50))
        
        members = [
            "Phạm Bạch Phúc Long - Leader",
            "Nguyễn Trọng Nhân - Developer",
            "Trần Khánh Duy - Developer",
            "Phạm Duy Phúc - Developer",
            "Nguyễn Hoàng Vinh - Developer"
        ]
        
        y = 150
        for member in members:
            text = self.content_font.render(member, True, COLORS['text'])
            self.screen.blit(text, (400 - text.get_width() // 2, y))
            y += 50
        
        self._draw_back_button()

    def draw_name_input(self):
        """Draw the name input screen"""
        self.screen.blit(self.sp_menu_bg, (0, 0))
        
        title = self.font.render("Nhập tên người chơi", True, COLORS['text'])
        self.screen.blit(title, (400 - title.get_width() // 2, 50))
        
        y = 150
        for i, name in enumerate(self.player_names):
            text = self.content_font.render(f"Người chơi {i + 1}:", True, COLORS['text'])
            self.screen.blit(text, (200, y))
            
            input_rect = pygame.Rect(400, y, 200, 30)
            color = COLORS['active_input'] if i == self.active_input else COLORS['text']
            pygame.draw.rect(self.screen, color, input_rect, 2)
            
            name_text = self.content_font.render(name, True, COLORS['text'])
            self.screen.blit(name_text, (410, y + 2))
            
            y += 50
        
        self._draw_back_button()
        self._draw_ok_button()

    def draw_rules(self):
        """Draw the rules screen"""
        self.screen.blit(self.sp_menu_bg, (0, 0))
        
        title = self.font.render("Luật chơi", True, COLORS['text'])
        self.screen.blit(title, (400 - title.get_width() // 2, 50))
        
        y = 150
        for rule in GAME_RULES:
            if rule:
                text = self.content_font.render(rule, True, COLORS['text'])
                self.screen.blit(text, (50, y))
            y += 30
        
        self._draw_back_button()

    def _draw_back_button(self):
        """Draw the back button"""
        text = self.small_font.render(BUTTON_TEXT["back"], True, COLORS['text'])
        btn = self.buttons["back"]
        self.screen.blit(text, (btn.centerx - text.get_width() // 2,
                               btn.centery - text.get_height() // 2))

    def _draw_ok_button(self):
        """Draw the OK button"""
        text = self.small_font.render(BUTTON_TEXT["ok"], True, COLORS['text'])
        btn = self.buttons["ok"]
        self.screen.blit(text, (btn.centerx - text.get_width() // 2,
                               btn.centery - text.get_height() // 2))

    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            
            if event.type == MOUSEBUTTONDOWN:
                if self.show_name_input:
                    return self._handle_name_input_click(event.pos)
                elif self.show_rules:
                    return self._handle_rules_click(event.pos)
                elif self.show_developers:
                    return self._handle_developers_click(event.pos)
                else:
                    return self._handle_main_menu_click(event.pos)
            
            elif event.type == KEYDOWN and self.show_name_input:
                return self._handle_name_input_key(event)
        
        return True

    def _handle_name_input_click(self, pos):
        """Handle clicks in the name input screen"""
        if self.buttons["back"].collidepoint(pos):
            self.show_name_input = False
            return True
        
        if self.buttons["ok"].collidepoint(pos):
            if all(name.strip() for name in self.player_names):
                return self.player_names
            return True
        
        # Check input field clicks
        y = 150
        for i in range(4):
            input_rect = pygame.Rect(400, y, 200, 30)
            if input_rect.collidepoint(pos):
                self.active_input = i
                return True
            y += 50
        
        return True

    def _handle_rules_click(self, pos):
        """Handle clicks in the rules screen"""
        if self.buttons["back"].collidepoint(pos):
            self.show_rules = False
        return True

    def _handle_developers_click(self, pos):
        """Handle clicks in the developers screen"""
        if self.buttons["back"].collidepoint(pos):
            self.show_developers = False
        return True

    def _handle_main_menu_click(self, pos):
        """Handle clicks in the main menu"""
        if self.buttons["play"].collidepoint(pos):
            self.show_name_input = True
        elif self.buttons["rules"].collidepoint(pos):
            self.show_rules = True
        elif self.buttons["developers"].collidepoint(pos):
            self.show_developers = True
        elif self.buttons["quit"].collidepoint(pos):
            return None
        return True

    def _handle_name_input_key(self, event):
        """Handle keyboard input for player names"""
        if event.key == K_TAB:
            self.active_input = (self.active_input + 1) % 4
        elif event.key == K_BACKSPACE:
            self.player_names[self.active_input] = self.player_names[self.active_input][:-1]
        elif event.unicode.isprintable():
            if len(self.player_names[self.active_input]) < 15:
                self.player_names[self.active_input] += event.unicode
        return True

    def render_tmx(self, tmx_data):
        """Render a TMX map to a surface"""
        # Create surface
        mapwidth = tmx_data.width * tmx_data.tilewidth
        mapheight = tmx_data.height * tmx_data.tileheight
        surface = pygame.Surface((mapwidth, mapheight))
        surface.fill((255, 255, 255))  # White background
        
        # Draw each visible layer
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):  # Layer with tiles
                for x, y, image in layer.tiles():
                    if image:
                        surface.blit(image, (x * tmx_data.tilewidth, y * tmx_data.tileheight))
        
        return surface

    def run(self):
        """Main loop for the board"""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            clock.tick(60)
            
            if self.show_name_input:
                self.draw_name_input()
            elif self.show_rules:
                self.draw_rules()
            elif self.show_developers:
                self.draw_developers()
            else:
                self.draw_main_menu()
            
            pygame.display.flip()
            
            result = self.handle_events()
            if result is None:
                running = False
            elif isinstance(result, list):
                return result
        
        return None
