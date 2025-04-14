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
                
            # Parse TMX
            logger.info("Parsing TMX file...")
            tree = ET.parse(full_path)
            root = tree.getroot()
            logger.info("Successfully parsed TMX file")
            
            # Get the TMX directory for path resolution
            tmx_dir = os.path.dirname(full_path)
            logger.info(f"TMX directory: {tmx_dir}")
            
            # Create temp directory
            tmp_dir = tempfile.mkdtemp()
            logger.info(f"Created temp directory: {tmp_dir}")
            
            try:
                # Process tileset sources - convert to absolute paths
                logger.info("Processing tileset paths...")
                for tileset in root.findall(".//tileset[@source]"):
                    source = tileset.get('source')
                    logger.info(f"Found tileset source: {source}")
                    
                    # Convert to absolute path
                    abs_source = os.path.abspath(os.path.join(tmx_dir, source))
                    if os.path.exists(abs_source):
                        # Use absolute path for the tileset
                        logger.info(f"Using absolute tileset path: {abs_source}")
                        tileset.set('source', abs_source)
                    else:
                        logger.warning(f"Tileset file not found: {abs_source}")
                        raise FileNotFoundError(f"Cannot find tileset file: {abs_source}")
                
                # Convert float offsets to integers
                logger.info("Processing layer offsets...")
                for layer in root.findall(".//layer"):
                    for attr in ['offsetx', 'offsety']:
                        if attr in layer.attrib:
                            try:
                                val = float(layer.attrib[attr])
                                layer.attrib[attr] = str(int(val))
                                logger.info(f"Converted {attr} from {val} to {int(val)} for layer {layer.get('name')}")
                            except (ValueError, TypeError):
                                layer.attrib[attr] = '0'
                
                # Save processed TMX to temp directory
                tmp_path = os.path.join(tmp_dir, "processed.tmx")
                tree.write(tmp_path, encoding='utf-8', xml_declaration=True)
                logger.info(f"Saved processed TMX to: {tmp_path}")
                
                # Load processed TMX
                logger.info("Loading processed TMX...")
                tmx_map = pytmx.load_pygame(tmp_path)
                logger.info("Successfully loaded TMX map")
                
                # Cache and return
                self.tmx_cache[path] = tmx_map
                return tmx_map
                
            except Exception as e:
                logger.error(f"Error processing TMX file: {e}")
                import traceback
                logger.error(f"Stack trace: {traceback.format_exc()}")
                return None
                
            finally:
                # Clean up temp directory
                if tmp_dir and os.path.exists(tmp_dir):
                    try:
                        import shutil
                        shutil.rmtree(tmp_dir)
                        logger.info(f"Cleaned up temp directory: {tmp_dir}")
                    except Exception as e:
                        logger.warning(f"Failed to clean up temp directory {tmp_dir}: {e}")
                
        except Exception as e:
            logger.error(f"Error loading TMX {path}: {e}")
            import traceback
            logger.error(f"Stack trace: {traceback.format_exc()}")
            import traceback
            logger.error(f"Stack trace: {traceback.format_exc()}")
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