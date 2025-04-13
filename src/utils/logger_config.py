"""
Logging configuration module providing consistent logging setup across the game.
"""

import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any

# Default log format
DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Log levels and their names
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

class GameLogger:
    """Game logging manager"""
    
    def __init__(self):
        self.loggers: Dict[str, logging.Logger] = {}
        self.log_dir = 'logs'
        self.initialized = False
        
    def initialize(self, log_level: str = 'INFO', 
                  log_to_file: bool = True,
                  log_to_console: bool = True,
                  format_str: Optional[str] = None,
                  date_format: Optional[str] = None) -> None:
        """
        Initialize the logging system
        
        Args:
            log_level: Logging level ('DEBUG', 'INFO', etc.)
            log_to_file: Whether to log to file
            log_to_console: Whether to log to console
            format_str: Optional custom log format
            date_format: Optional custom date format
        """
        if self.initialized:
            return
            
        # Create logs directory if needed
        if log_to_file and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Set up basic configuration
        log_config = {
            'level': LOG_LEVELS.get(log_level.upper(), logging.INFO),
            'format': format_str or DEFAULT_FORMAT,
            'datefmt': date_format or DEFAULT_DATE_FORMAT,
            'handlers': []
        }
        
        # Add console handler if requested
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter(log_config['format'], log_config['datefmt'])
            )
            log_config['handlers'].append(console_handler)
        
        # Add file handler if requested
        if log_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(self.log_dir, f'game_{timestamp}.log')
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter(log_config['format'], log_config['datefmt'])
            )
            log_config['handlers'].append(file_handler)
        
        # Configure logging
        logging.basicConfig(**log_config)
        self.initialized = True
        
        # Log initialization
        logger = self.get_logger('system')
        logger.info("Logging system initialized")
        logger.debug(f"Log configuration: {log_config}")
        
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get or create a logger
        
        Args:
            name: Logger name
            
        Returns:
            Logger: The requested logger
        """
        if not self.initialized:
            self.initialize()
            
        if name not in self.loggers:
            self.loggers[name] = logging.getLogger(name)
        return self.loggers[name]
        
    def set_level(self, level: str, logger_name: Optional[str] = None) -> None:
        """
        Set logging level for specific or all loggers
        
        Args:
            level: Logging level name
            logger_name: Optional specific logger name
        """
        log_level = LOG_LEVELS.get(level.upper())
        if not log_level:
            return
            
        if logger_name:
            if logger_name in self.loggers:
                self.loggers[logger_name].setLevel(log_level)
        else:
            logging.getLogger().setLevel(log_level)
            for logger in self.loggers.values():
                logger.setLevel(log_level)
                
    def add_file_handler(self, filename: str, 
                        level: Optional[str] = None,
                        format_str: Optional[str] = None) -> None:
        """
        Add an additional file handler
        
        Args:
            filename: Log file name
            level: Optional logging level for this handler
            format_str: Optional format string for this handler
        """
        if not self.initialized:
            self.initialize()
            
        filepath = os.path.join(self.log_dir, filename)
        handler = logging.FileHandler(filepath)
        
        if level:
            log_level = LOG_LEVELS.get(level.upper())
            if log_level:
                handler.setLevel(log_level)
                
        handler.setFormatter(
            logging.Formatter(
                format_str or DEFAULT_FORMAT,
                DEFAULT_DATE_FORMAT
            )
        )
        
        logging.getLogger().addHandler(handler)

# Global logger instance
_logger_manager = None

def get_logger_manager() -> GameLogger:
    """Get or create the global logger manager instance"""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = GameLogger()
    return _logger_manager

def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger
    
    Args:
        name: Logger name
        
    Returns:
        Logger: The requested logger
    """
    return get_logger_manager().get_logger(name)

def initialize_logging(config: Dict[str, Any]) -> None:
    """
    Initialize logging system with configuration
    
    Args:
        config: Dictionary of logging configuration options
    """
    get_logger_manager().initialize(**config)