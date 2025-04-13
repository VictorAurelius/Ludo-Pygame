# Troubleshooting Guide

This guide helps you diagnose and fix common issues in the Ludo game.

## Table of Contents

1. [Game Won't Start](#game-wont-start)
2. [Performance Issues](#performance-issues)
3. [Graphics Problems](#graphics-problems)
4. [Sound Issues](#sound-issues)
5. [Input Problems](#input-problems)
6. [Asset Loading Errors](#asset-loading-errors)
7. [Common Error Messages](#common-error-messages)

## Game Won't Start

### Symptoms:
- Game crashes immediately
- Black screen appears
- No window opens

### Solutions:

1. **Check Python Version**
```bash
python --version  # Should be 3.8 or higher
```

2. **Verify Dependencies**
```bash
pip install -r requirements.txt --force-reinstall
```

3. **Check Log Files**
- Look in `logs/` directory
- Check for error messages

4. **Clear Cache**
```bash
# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -r {} +
```

## Performance Issues

### Symptoms:
- Game runs slowly
- Animations stutter
- High CPU usage

### Solutions:

1. **Check System Resources**
```bash
# Windows (Task Manager)
taskmgr

# Linux
top
```

2. **Enable Debug Logging**
```python
# Set environment variable
export LUDO_DEBUG=1
```

3. **Optimize Graphics**
- Reduce window size in constants.py
- Disable unnecessary animations
- Close background applications

4. **Profile Code**
```bash
python -m cProfile -o profile.stats main.py
```

## Graphics Problems

### Symptoms:
- Missing textures
- Graphical glitches
- Wrong colors

### Solutions:

1. **Update Graphics Drivers**

2. **Verify Asset Files**
```bash
# Check asset structure
tree assets/
```

3. **Check OpenGL Support**
```python
import pygame
pygame.init()
print(pygame.display.get_driver())
```

4. **Reset Display Settings**
```python
# In constants.py
WINDOW_WIDTH = 925
WINDOW_HEIGHT = 725
```

## Sound Issues

### Symptoms:
- No sound
- Sound distortion
- Wrong sound effects

### Solutions:

1. **Check Audio Device**
```python
import pygame.mixer
pygame.mixer.init()
print(pygame.mixer.get_init())
```

2. **Verify Sound Files**
```bash
# Check sound files exist
ls assets/sounds/
```

3. **Reset Sound Settings**
```python
# In sound_manager.py
pygame.mixer.init(44100, -16, 2, 2048)
```

4. **Test System Audio**
```bash
# Windows
control mmsys.cpl

# Linux
pavucontrol
```

## Input Problems

### Symptoms:
- Unresponsive controls
- Stuck keys
- Wrong input detection

### Solutions:

1. **Check Event Queue**
```python
# Debug event handling
pygame.event.pump()
print(pygame.event.get())
```

2. **Reset Input State**
```python
pygame.event.clear()
pygame.key.set_repeat(0)
```

3. **Verify Input Devices**
```python
# List joysticks
pygame.joystick.init()
print([pygame.joystick.Joystick(x).get_name() for x in range(pygame.joystick.get_count())])
```

## Asset Loading Errors

### Symptoms:
- Missing images
- File not found errors
- Asset loading failures

### Solutions:

1. **Check File Permissions**
```bash
# Linux/macOS
ls -l assets/

# Windows
icacls assets
```

2. **Verify File Paths**
```python
# Debug asset loading
logger.setLevel(logging.DEBUG)
```

3. **Reset Asset Cache**
```python
asset_loader = get_asset_loader()
asset_loader.clear_cache()
```

## Common Error Messages

### "ModuleNotFoundError: No module named 'pygame'"
```bash
pip install pygame --upgrade
```

### "SDL_Init: No available video device"
1. Check display connection
2. Update graphics drivers
3. Run with basic video driver:
```python
os.environ["SDL_VIDEODRIVER"] = "dummy"
```

### "Resource not found"
1. Verify asset paths
2. Check working directory
3. Update asset loader configuration

### "Permission denied"
1. Check file permissions
2. Run as administrator/sudo
3. Check antivirus settings

## Debug Mode

Enable debug mode for detailed logging:

```python
# In main.py
from src.utils.logger_config import get_logger
logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)
```

## Collecting Debug Information

When reporting issues, include:

1. **System Information**
```python
import sys
import pygame
print(f"Python: {sys.version}")
print(f"Pygame: {pygame.version.ver}")
print(f"OS: {sys.platform}")
```

2. **Log Files**
- Check `logs/` directory
- Include relevant error messages

3. **Screenshots**
- Capture any visual issues
- Include error dialogs

4. **Steps to Reproduce**
- Detailed reproduction steps
- Game configuration
- Input sequence

## Getting Help

If issues persist:

1. Check GitHub Issues
2. Join Discord Community
3. Contact Support Team
4. Create Detailed Bug Report

## Performance Tuning

### Memory Usage
```python
# Monitor memory
import psutil
process = psutil.Process()
print(process.memory_info().rss)
```

### CPU Profiling
```bash
python -m cProfile -o profile.stats main.py
python -c "import pstats; p=pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(30)"
```

### Graphics Profiling
```python
# Enable FPS counter
clock = pygame.time.Clock()
clock.tick()
print(clock.get_fps())
```

## Clean Installation

If all else fails:

1. Uninstall completely:
```bash
pip uninstall -r requirements.txt -y
```

2. Remove all files:
```bash
rm -rf * .*
```

3. Fresh clone:
```bash
git clone https://github.com/yourusername/ludo-game.git
```

4. Reinstall:
```bash
pip install -r requirements.txt