import pygame
from pygame.locals import *
import pytmx
import os
from pytmx.util_pygame import load_pygame

# Import from restructured modules
from src.entities.Pawns import *
from src.entities.Players import *
from src.entities.States import *
from src.entities.Stars import stars
from src.core.main_board import MainBoard
from src.ui.alert_manager import AlertManager
from src.ui.menu_manager import MenuManager
from src.ui.sound_manager import get_sound_manager
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    GAME_STATE_MENU, GAME_STATE_PLAYING,
    WHITE, BLACK, GRAY,
    ROLL_BUTTON, TITLE_BUTTON, SOUND_BUTTON,
    YES_BUTTON, NO_BUTTON,
    DICE_IMAGES, MAP_PATH
)

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ludo Game")
        
        # Initialize managers
        self.alert_manager = AlertManager()
        self.menu_manager = None
        self.sound_manager = get_sound_manager()
        self.statekpr = None
        
        # Game state
        self.current_game_state = GAME_STATE_MENU
        
        # Game UI Elements
        self.roll_button = pygame.Rect(*ROLL_BUTTON)
        self.title_button = pygame.Rect(*TITLE_BUTTON)
        self.yes_button = pygame.Rect(*YES_BUTTON)
        self.no_button = pygame.Rect(*NO_BUTTON)
        self.sound_button = pygame.Rect(*SOUND_BUTTON)
        
        # Game variables
        self.dice_images = []
        self.bgBoard = None
        self.current_dice1 = None
        self.current_dice2 = None
        self.dice_num1 = 1
        self.dice_num2 = 1
        self.roll_button_enabled = True
        self.can_move = False
        self.dice_animating = False
        self.showing_dialog = False
        self.finished_players = []

    def draw_sound_button(self):
        """Draw sound control button"""
        is_enabled = self.sound_manager.enabled and self.sound_manager.initialized
        mouse_hover = self.sound_button.collidepoint(pygame.mouse.get_pos())
        button_color = GRAY if is_enabled else BLACK
        if mouse_hover:
            button_color = (min(button_color[0] + 30, 255),
                          min(button_color[1] + 30, 255),
                          min(button_color[2] + 30, 255))
        
        pygame.draw.rect(self.win, button_color, self.sound_button)
        pygame.draw.polygon(self.win, WHITE, [
            (self.sound_button.x + 10, self.sound_button.y + 15),
            (self.sound_button.x + 20, self.sound_button.y + 10),
            (self.sound_button.x + 20, self.sound_button.y + 30),
            (self.sound_button.x + 10, self.sound_button.y + 25)
        ])
        
        if not is_enabled:
            pygame.draw.line(self.win, WHITE,
                           (self.sound_button.x + 10, self.sound_button.y + 10),
                           (self.sound_button.x + 30, self.sound_button.y + 30), 2)

    def load_game_assets(self):
        """Load all game assets"""
        try:
            # Load dice images
            self.dice_images = [pygame.image.load(path) for path in DICE_IMAGES]
            # Load game board
            self.bgBoard = self.load_map()
            return True
        except Exception as e:
            print(f"Error loading assets: {e}")
            return False

    def load_map(self):
        """Load and render the game map"""
        map_surface = pygame.Surface((725, 725))
        game_map = load_pygame(MAP_PATH)
        for layer in game_map.visible_layers:
            for x, y, gid in layer:
                tile = game_map.get_tile_image_by_gid(gid)
                if tile:
                    map_surface.blit(tile, (x * game_map.tilewidth, y * game_map.tileheight))
        return map_surface

    def init_game_variables(self):
        """Initialize or reset all game variables"""
        self.roll_button_enabled = True
        self.can_move = False
        self.dice_animating = False
        self.showing_dialog = False
        self.finished_players = []
        
        if self.dice_images:
            self.current_dice1 = self.dice_images[0]
            self.current_dice2 = self.dice_images[0]
        self.dice_num1 = 1
        self.dice_num2 = 1
        
        self.statekpr = Statekeep()

    def draw_dialog(self):
        """Draw dialog box asking to return to title"""
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.set_alpha(128)
        s.fill(BLACK)
        self.win.blit(s, (0, 0))
        
        dialog_rect = pygame.Rect(400, 200, 230, 100)
        pygame.draw.rect(self.win, WHITE, dialog_rect)
        pygame.draw.rect(self.win, BLACK, dialog_rect, 2)
        
        vn_font = pygame.font.SysFont("segoeui", 24)
        text = vn_font.render(u"Bạn có muốn trở về", True, BLACK)
        text2 = vn_font.render(u"trang tiêu đề không?", True, BLACK)
        self.win.blit(text, (410, 200))
        self.win.blit(text2, (410, 220))
        
        mouse_pos = pygame.mouse.get_pos()
        yes_color = GRAY if self.yes_button.collidepoint(mouse_pos) else BLACK
        no_color = GRAY if self.no_button.collidepoint(mouse_pos) else BLACK
        
        pygame.draw.rect(self.win, yes_color, self.yes_button, 2)
        pygame.draw.rect(self.win, no_color, self.no_button, 2)
        
        yes_text = vn_font.render(u"Có", True, yes_color)
        no_text = vn_font.render(u"Không", True, no_color)
        self.win.blit(yes_text, (425, 255))
        self.win.blit(no_text, (540, 255))

    def handle_menu(self):
        """Handle menu state"""
        if self.menu_manager is None:
            self.menu_manager = MenuManager(self.win)
            self.menu_manager.initialize()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == MOUSEBUTTONDOWN:
                if self.sound_button.collidepoint(event.pos):
                    self.sound_manager.toggle()
                    self.sound_manager.play_sound('click')
                else:
                    action = self.menu_manager.handle_click(event.pos)
                    if action == "start_game":
                        self.init_game_variables()
                        return action
                    elif action == "exit":
                        return False
        
        self.menu_manager.draw()
        self.draw_sound_button()
        return True

    def handle_game_events(self):
        """Handle game state events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == MOUSEBUTTONDOWN:
                if self.showing_dialog:
                    if self.yes_button.collidepoint(event.pos):
                        return "menu"
                    elif self.no_button.collidepoint(event.pos):
                        self.showing_dialog = False
                    self.sound_manager.play_sound('click')
                else:
                    if self.title_button.collidepoint(event.pos):
                        self.showing_dialog = True
                        self.sound_manager.play_sound('click')
                    elif self.sound_button.collidepoint(event.pos):
                        self.sound_manager.toggle()
                        self.sound_manager.play_sound('click')
        
        return True

    def handle_game(self):
        """Handle game state"""
        self.win.blit(self.bgBoard, (0, 0))
        
        if self.statekpr:
            self.statekpr.update()
        
        result = self.handle_game_events()
        if result != True:
            return result
        
        self.draw_sound_button()
        
        if self.showing_dialog:
            self.draw_dialog()
        
        return True

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            clock.tick(60)
            
            if self.current_game_state == GAME_STATE_MENU:
                result = self.handle_menu()
                if result == "start_game":
                    self.current_game_state = GAME_STATE_PLAYING
                elif not result:
                    running = False
            
            elif self.current_game_state == GAME_STATE_PLAYING:
                result = self.handle_game()
                if result == "menu":
                    self.current_game_state = GAME_STATE_MENU
                elif not result:
                    running = False
            
            pygame.display.flip()

def main():
    game = Game()
    if not game.load_game_assets():
        print("Failed to load game assets!")
        pygame.quit()
        return
    
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()