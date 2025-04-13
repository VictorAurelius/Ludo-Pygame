# Installation Guide

This guide will help you install and set up the Ludo game on your system.

## System Requirements

- Python 3.8 or higher
- 500MB free disk space
- Graphics card supporting OpenGL 2.0 or higher
- Operating System:
  - Windows 10/11
  - macOS 10.14 or higher
  - Linux (Ubuntu 20.04 or equivalent)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ludo-game.git
cd ludo-game
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Platform-Specific Dependencies

#### Windows
No additional steps required.

#### macOS
Install SDL2 dependencies:
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev \
    libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev
```

### 5. Verify Installation

```bash
python -m pytest tests/
```

### 6. Run the Game

```bash
python main.py
```

## Optional Components

### Development Tools

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Documentation Tools

Install documentation tools:
```bash
pip install -r requirements-docs.txt
```

## Common Installation Issues

### 1. Pygame Installation Fails

#### Windows
- Ensure Microsoft Visual C++ Build Tools are installed
- Try installing a pre-built wheel:
  ```bash
  pip install --only-binary :all: pygame
  ```

#### macOS
- If SDL2 error occurs:
  ```bash
  brew reinstall sdl2 sdl2_image sdl2_mixer sdl2_ttf
  ```

#### Linux
- If missing dependencies:
  ```bash
  sudo apt-get install -y python3-pygame
  ```

### 2. Asset Loading Issues

Ensure correct directory structure:
```
ludo-game/
├── assets/
│   ├── images/
│   ├── sounds/
│   └── maps/
├── src/
└── ...
```

### 3. Font Issues

If default fonts don't work:
1. Install additional system fonts:
   ```bash
   # Linux
   sudo apt-get install fonts-freefont-ttf
   
   # macOS
   brew install font-freefont
   ```
2. Or use bundled fonts in `assets/fonts/`

### 4. Performance Issues

- Update graphics drivers
- Check Python version is 3.8+
- Ensure virtual environment is active
- Monitor CPU/memory usage

## Upgrading

To upgrade to the latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Development Setup

For development, install additional tools:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Install documentation tools
pip install -r requirements-docs.txt
```

## Environment Variables

Optional environment variables for configuration:

```bash
# Windows (PowerShell)
$env:LUDO_DEBUG = "1"
$env:LUDO_ASSETS = "path/to/assets"

# Linux/macOS
export LUDO_DEBUG=1
export LUDO_ASSETS=path/to/assets
```

## Build Documentation

Generate documentation:

```bash
# Generate API docs
pdoc --html --output-dir docs/api src/

# Build MkDocs site
mkdocs build
```

## Uninstallation

1. Deactivate virtual environment:
   ```bash
   deactivate
   ```

2. Remove project directory:
   ```bash
   # Windows
   rmdir /s /q ludo-game
   
   # Linux/macOS
   rm -rf ludo-game
   ```

## Getting Help

If you encounter issues:

1. Check the troubleshooting guide (TROUBLESHOOTING.md)
2. Search existing issues on GitHub
3. Join our Discord community
4. Open a new issue with:
   - System information
   - Error messages
   - Steps to reproduce