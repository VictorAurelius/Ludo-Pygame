"""
Asset loading utility module providing functions for loading and managing game assets.
"""

import os
import pygame
import pytmx
import logging
from typing import Dict, Optional, Tuple, Union
from pygame.surface import Surface

logger = logging.getLogger(__name__)

class AssetLoader:
    """Handles loading and caching of game assets"""
    
    def __init__(self):
        self.image_cache: Dict[str, Surface] = {}
        self.tmx_cache: Dict[str, pytmx.TiledMap] = {}
        self.font_cache: Dict[Tuple[str, int], pygame.font.Font] = {}
        
    def load_image(self, path: str, alpha: bool = True) -> Optional[Surface]:
        """
        Load an image, with caching
        
        Args:
            path: Path to image file
            alpha: Whether to include alpha channel
            
        Returns:
            Surface or None: Loaded image surface
        """
        if path in self.image_cache:
            return self.image_cache[path]
            
        try:
            full_path = self._resolve_path(path)
            if not os.path.exists(full_path):
                logger.error(f"Image not found: {full_path}")
                return None
                
            image = pygame.image.load(full_path)
            if alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
                
            self.image_cache[path] = image
            return image
            
        except Exception as e:
            logger.error(f"Error loading image {path}: {e}")
            return None

    def load_tmx(self, path: str) -> Optional[pytmx.TiledMap]:
        """
        Load a TMX map file, with caching and float offset handling
        
        Args:
            path: Path to TMX file
            
        Returns:
            TiledMap or None: Loaded TMX map
        """
        if path in self.tmx_cache:
            return self.tmx_cache[path]
            
        try:
            import xml.etree.ElementTree as ET
            import tempfile
            import os
            
            full_path = self._resolve_path(path)
            logger.info(f"Attempting to load TMX file: {full_path}")
            
            if not os.path.exists(full_path):
                logger.error(f"TMX file not found: {full_path}")
                return None
                
            # Parse TMX and fix floating point offsets
            logger.info("Parsing TMX file...")
            tree = ET.parse(full_path)
            root = tree.getroot()
            logger.info("Successfully parsed TMX file")
            
            # Check XML structure
            logger.info(f"TMX Version: {root.get('version')}")
            logger.info(f"Number of layers: {len(root.findall('.//layer'))}")
            
            # Convert all float offsets to integers
            for layer in root.findall(".//layer"):
                for attr in ['offsetx', 'offsety']:
                    if attr in layer.attrib:
                        try:
                            val = float(layer.attrib[attr])
                            layer.attrib[attr] = str(int(val))
                        except (ValueError, TypeError):
                            layer.attrib[attr] = '0'
            
            logger.info("Processing layer offsets...")
            modified = False
            for layer in root.findall(".//layer"):
                logger.info(f"Processing layer: {layer.get('name')}")
                logger.info(f"Original offsets - x: {layer.get('offsetx', '0')}, y: {layer.get('offsety', '0')}")
            
            # Save to temporary file
            tmp_path = None
            logger.info("Saving processed TMX to temp file...")
            try:
                with tempfile.NamedTemporaryFile(suffix='.tmx', delete=False) as tmp:
                    tmp_path = tmp.name
                    tree.write(tmp_path, encoding='utf-8', xml_declaration=True)
                    logger.info(f"Saved to temp file: {tmp_path}")
                
                # Load the processed file
                logger.info("Loading processed TMX with PyTMX...")
                tmx_map = pytmx.load_pygame(tmp_path)
                
                # Cache and return
                self.tmx_cache[path] = tmx_map
                return tmx_map
                
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.unlink(tmp_path)
                    except Exception as e:
                        logger.warning(f"Failed to clean up temp file {tmp_path}: {e}")
            
        except Exception as e:
            logger.error(f"Error loading TMX {path}: {e}")
            return None
            logger.error(f"Error loading TMX {path}: {e}")
            return None

    def load_font(self, name: str, size: int) -> pygame.font.Font:
        """
        Load a font, with caching and fallback options
        
        Args:
            name: Font name or path
            size: Font size in points
            
        Returns:
            Font: Loaded font object
        """
        cache_key = (name, size)
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
            
        try:
            # Try as system font first
            font = pygame.font.SysFont(name, size)
            self.font_cache[cache_key] = font
            return font
            
        except Exception:
            try:
                # Try as file path
                full_path = self._resolve_path(name)
                if os.path.exists(full_path):
                    font = pygame.font.Font(full_path, size)
                    self.font_cache[cache_key] = font
                    return font
            except Exception:
                pass
            
            # Fallback to default font
            logger.warning(f"Using fallback font for {name}")
            font = pygame.font.Font(None, size)
            self.font_cache[cache_key] = font
            return font

    def load_sprite_sheet(self, path: str, tile_size: Tuple[int, int],
                         colorkey: Optional[Tuple[int, int, int]] = None) -> Dict[int, Surface]:
        """
        Load a sprite sheet and split into individual sprites
        
        Args:
            path: Path to sprite sheet image
            tile_size: (width, height) of each sprite
            colorkey: Optional color to use as transparency
            
        Returns:
            Dict[int, Surface]: Dictionary of sprite surfaces indexed by position
        """
        sheet = self.load_image(path, alpha=False)
        if not sheet:
            return {}
            
        sprites = {}
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        tile_width, tile_height = tile_size
        
        for y in range(0, sheet_height, tile_height):
            for x in range(0, sheet_width, tile_width):
                sprite_index = len(sprites)
                sprite = pygame.Surface(tile_size, pygame.SRCALPHA)
                sprite.blit(sheet, (0, 0), (x, y, tile_width, tile_height))
                
                if colorkey is not None:
                    sprite.set_colorkey(colorkey)
                    
                sprites[sprite_index] = sprite
                
        return sprites

    def _resolve_path(self, path: str) -> str:
        """Resolve asset path relative to assets directory"""
        if os.path.isabs(path):
            return path
            
        # Log current working directory
        cwd = os.getcwd()
        logger.info(f"Current working directory: {cwd}")
            
        # Try multiple possible asset directories and log each attempt
        tried_paths = []
        asset_dirs = ['assets', 'assets_ver1', '.', 'e:/a-game/Ludo-Pygame/assets']
        for asset_dir in asset_dirs:
            full_path = os.path.normpath(os.path.join(asset_dir, path))
            tried_paths.append(full_path)
            logger.info(f"Trying path: {full_path}")
            if os.path.exists(full_path):
                logger.info(f"Found file at: {full_path}")
                return full_path
                
        # Log all attempted paths if file not found
        logger.error(f"File not found at any of these locations: {tried_paths}")
        return path

    def clear_cache(self, asset_type: Optional[str] = None) -> None:
        """
        Clear asset cache
        
        Args:
            asset_type: Optional type to clear ('image', 'tmx', 'font', or None for all)
        """
        if asset_type == 'image':
            self.image_cache.clear()
        elif asset_type == 'tmx':
            self.tmx_cache.clear()
        elif asset_type == 'font':
            self.font_cache.clear()
        else:
            self.image_cache.clear()
            self.tmx_cache.clear()
            self.font_cache.clear()

# Global asset loader instance
_asset_loader = None

def get_asset_loader() -> AssetLoader:
    """Get or create the global asset loader instance"""
    global _asset_loader
    if _asset_loader is None:
        _asset_loader = AssetLoader()
    return _asset_loader