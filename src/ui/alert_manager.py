"""
Alert management module handling in-game notifications and messages.
"""

import pygame
from src.utils.constants import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT

class Alert:
    """Individual alert message with its properties"""
    def __init__(self, message, duration, style=None):
        self.message = message
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.style = style or {}
        
    @property
    def time_left(self):
        """Get remaining display time in milliseconds"""
        return self.duration - (pygame.time.get_ticks() - self.start_time)
    
    @property
    def is_expired(self):
        """Check if alert has expired"""
        return self.time_left <= 0

class AlertManager:
    """
    Manages and displays alert messages in the game.
    Supports multiple simultaneous alerts with customizable styles.
    """
    
    DEFAULT_STYLE = {
        'font_name': 'segoeui',
        'font_size': 24,
        'bg_color': (0, 0, 0),
        'text_color': (255, 255, 255),
        'bg_alpha': 200,
        'width': 400,
        'height': 50,
        'spacing': 60,
        'fadeout_time': 500,
        'y_offset': 50
    }
    
    def __init__(self):
        """Initialize the alert manager"""
        self.alerts = []  # List of active alerts
        self.max_alerts = 5  # Maximum number of simultaneous alerts
        self._font = None
        self._init_font()

    def _init_font(self):
        """Initialize font with fallback options"""
        try:
            self._font = pygame.font.SysFont(
                self.DEFAULT_STYLE['font_name'],
                self.DEFAULT_STYLE['font_size']
            )
        except pygame.error:
            try:
                # Try system default font as fallback
                self._font = pygame.font.Font(None, self.DEFAULT_STYLE['font_size'])
            except pygame.error as e:
                print(f"Error initializing font: {e}")
                # Create a minimal font as last resort
                self._font = pygame.font.Font(None, self.DEFAULT_STYLE['font_size'])

    def add_alert(self, message, duration=2000, style=None):
        """
        Add a new alert message
        
        Args:
            message (str): Alert message to display
            duration (int): Display duration in milliseconds
            style (dict): Custom style overrides for this alert
        """
        if not isinstance(message, str):
            message = str(message)
        
        alert = Alert(message, duration, style)
        self.alerts.append(alert)
        
        # Remove oldest alert if limit exceeded
        if len(self.alerts) > self.max_alerts:
            self.alerts.pop(0)

    def update(self):
        """Update alert states and remove expired alerts"""
        self.alerts = [alert for alert in self.alerts if not alert.is_expired]

    def draw(self, screen):
        """
        Draw all active alerts
        
        Args:
            screen: Pygame surface to draw on
        """
        if not self.alerts:
            return
            
        for i, alert in enumerate(self.alerts):
            self._draw_alert(screen, alert, i)

    def _draw_alert(self, screen, alert, index):
        """Draw a single alert"""
        style = {**self.DEFAULT_STYLE, **(alert.style or {})}
        
        # Calculate position
        y_position = style['y_offset'] + index * style['spacing']
        x_position = (screen.get_width() - style['width']) // 2
        
        # Create and draw background
        alert_bg = self._create_alert_background(style)
        screen.blit(alert_bg, (x_position, y_position))
        
        # Create and draw text
        text_surface = self._create_text_surface(alert, style)
        text_rect = text_surface.get_rect(
            center=(screen.get_width() // 2, y_position + style['height'] // 2)
        )
        
        # Apply fadeout effect if needed
        if alert.time_left < style['fadeout_time']:
            alpha = int(alert.time_left / style['fadeout_time'] * 255)
            text_surface.set_alpha(alpha)
        
        screen.blit(text_surface, text_rect)

    def _create_alert_background(self, style):
        """Create semi-transparent background surface for alert"""
        bg = pygame.Surface((style['width'], style['height']))
        bg.set_alpha(style['bg_alpha'])
        bg.fill(style['bg_color'])
        return bg

    def _create_text_surface(self, alert, style):
        """Create text surface for alert message"""
        try:
            return self._font.render(
                alert.message,
                True,
                style['text_color']
            )
        except pygame.error as e:
            print(f"Error rendering text: {e}")
            # Return empty surface as fallback
            return pygame.Surface((1, 1))

    def clear(self):
        """Clear all active alerts"""
        self.alerts.clear()

    @property
    def active_count(self):
        """Get number of currently active alerts"""
        return len(self.alerts)

# Add a function to return an instance of AlertManager
def get_alert_manager():
    """Return a singleton instance of AlertManager"""
    if not hasattr(get_alert_manager, "_instance"):
        get_alert_manager._instance = AlertManager()
    return get_alert_manager._instance