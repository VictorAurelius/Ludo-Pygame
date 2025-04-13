"""
Sound management module handling game audio playback and control.
"""

import os
import logging
import pygame
from typing import Dict, Optional

from src.utils.sound_config import (
    SOUND_FILES, SOUND_DIRS, SOUND_CATEGORIES,
    DEFAULT_VOLUME, MAX_VOLUME, MIN_VOLUME,
    FALLBACK_SOUNDS
)

logger = logging.getLogger(__name__)

class Sound:
    """Wrapper for pygame Sound with additional functionality"""
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.sound: Optional[pygame.mixer.Sound] = None
        self.volume = DEFAULT_VOLUME
        self._load()
    
    def _load(self) -> bool:
        """Load the sound file"""
        try:
            self.sound = pygame.mixer.Sound(self.filepath)
            self.sound.set_volume(self.volume)
            return True
        except Exception as e:
            logger.warning(f"Failed to load sound {self.filepath}: {e}")
            return False
            
    def play(self) -> bool:
        """Play the sound"""
        if self.sound:
            try:
                self.sound.play()
                return True
            except Exception as e:
                logger.error(f"Error playing sound {self.filepath}: {e}")
        return False
        
    def stop(self) -> bool:
        """Stop the sound"""
        if self.sound:
            try:
                self.sound.stop()
                return True
            except Exception as e:
                logger.error(f"Error stopping sound {self.filepath}: {e}")
        return False
        
    def set_volume(self, volume: float) -> None:
        """Set sound volume"""
        self.volume = max(MIN_VOLUME, min(MAX_VOLUME, volume))
        if self.sound:
            self.sound.set_volume(self.volume)

class SoundManager:
    """Manages game audio playback and settings"""
    
    def __init__(self):
        """Initialize the sound manager"""
        self.enabled = True
        self.initialized = False
        self.sounds: Dict[str, Sound] = {}
        self.category_volumes = {cat: DEFAULT_VOLUME for cat in SOUND_CATEGORIES}
        self.master_volume = DEFAULT_VOLUME
        
        self._initialize_mixer()
        if self.initialized:
            self._load_sounds()

    def _initialize_mixer(self) -> None:
        """Initialize pygame mixer"""
        try:
            pygame.mixer.init()
            self.initialized = True
            logger.info("Sound system initialized successfully")
        except Exception as e:
            logger.error(f"Sound system initialization failed: {e}")
            logger.info("Game will continue without sound")

    def _load_sounds(self) -> None:
        """Load all configured sound files"""
        for sound_name, filename in SOUND_FILES.items():
            sound_loaded = False
            
            # Try each sound directory
            for sound_dir in SOUND_DIRS:
                if sound_loaded:
                    break
                    
                filepath = os.path.join(sound_dir, filename)
                if os.path.exists(filepath):
                    try:
                        self.sounds[sound_name] = Sound(filepath)
                        sound_loaded = True
                        logger.debug(f"Loaded sound: {sound_name} from {filepath}")
                    except Exception as e:
                        logger.warning(f"Failed to load {filepath}: {e}")

            if not sound_loaded:
                logger.warning(f"Could not load sound: {sound_name}")

    def play_sound(self, sound_name: str) -> bool:
        """
        Play a sound by name
        
        Args:
            sound_name: Name of sound to play
            
        Returns:
            bool: True if sound played successfully
        """
        if not (self.enabled and self.initialized):
            return False
            
        # Try primary sound
        if sound_name in self.sounds:
            if self.sounds[sound_name].play():
                return True
                
        # Try fallback sound
        if sound_name in FALLBACK_SOUNDS:
            fallback = FALLBACK_SOUNDS[sound_name]
            if fallback in self.sounds:
                if self.sounds[fallback].play():
                    return True
                    
        return False

    def stop_sound(self, sound_name: str) -> bool:
        """
        Stop a specific sound
        
        Args:
            sound_name: Name of sound to stop
            
        Returns:
            bool: True if sound was stopped
        """
        if not self.initialized:
            return False
            
        if sound_name in self.sounds:
            return self.sounds[sound_name].stop()
        return False

    def stop_category(self, category: str) -> None:
        """Stop all sounds in a category"""
        if category in SOUND_CATEGORIES:
            for sound_name in SOUND_CATEGORIES[category]:
                self.stop_sound(sound_name)

    def stop_all(self) -> None:
        """Stop all sounds"""
        if self.initialized:
            try:
                pygame.mixer.stop()
            except Exception as e:
                logger.error(f"Error stopping all sounds: {e}")

    def set_volume(self, volume: float) -> None:
        """Set master volume level"""
        self.master_volume = max(MIN_VOLUME, min(MAX_VOLUME, volume))
        self._update_volumes()

    def set_category_volume(self, category: str, volume: float) -> None:
        """Set volume for a sound category"""
        if category in SOUND_CATEGORIES:
            self.category_volumes[category] = max(MIN_VOLUME, min(MAX_VOLUME, volume))
            self._update_volumes()

    def _update_volumes(self) -> None:
        """Update volumes for all sounds based on master and category volumes"""
        for sound_name, sound in self.sounds.items():
            # Find which category the sound belongs to
            category = next(
                (cat for cat, sounds in SOUND_CATEGORIES.items() 
                 if sound_name in sounds),
                None
            )
            
            # Calculate final volume
            if category:
                volume = self.master_volume * self.category_volumes[category]
            else:
                volume = self.master_volume
                
            sound.set_volume(volume)

    def toggle(self) -> None:
        """Toggle sound on/off"""
        if self.initialized:
            self.enabled = not self.enabled
            if not self.enabled:
                self.stop_all()

    @property
    def has_sounds(self) -> bool:
        """Check if any sounds are loaded"""
        return bool(self.sounds)

# Global sound manager instance
_sound_manager = None

def get_sound_manager() -> SoundManager:
    """Get or create the global sound manager instance"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager