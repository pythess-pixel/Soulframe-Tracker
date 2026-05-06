# Soulframe Tracker

A lightweight, non-intrusive, real-time overlay tracker for Soulframe.

This tool passively parses the game's `EE.log` file to track dynamic events, such as when a procedural Arena spawns. It provides a simple click-through UI overlay that automatically resets when entering and exiting dungeons.

## Features
- **Real-Time Log Parsing**: Passively reads `EE.log` without interacting with the game's memory (TOS friendly).
- **Arena Detection**: Visual and audio alerts when a procedural Arena (`/Layer8/Prefab7/`) spawns.
- **Auto-Reset**: Automatically shows and hides the overlay when transitioning between the Hub and Dungeons.
- **Click-Through UI**: Semi-transparent, always-on-top overlay that does not block mouse clicks in-game.
- **System Tray Support**: Hide or close the tracker quietly via the system tray.
- **Global Hotkey**: Press `Ctrl+Shift+Q` to quickly exit the tracker at any time.

## Usage
1. Run `monitor.py` or the compiled `SoulframeTracker.exe` before or during a Soulframe session.
2. Enter a dungeon and the overlay will appear in the top-left corner.
3. Wait for the "Found!" text and beep sound when an Arena spawns.
4. To close, right-click the green system tray icon and select "Exit Tracker", or press `Ctrl+Shift+Q`.

## Compiling from source
Requirements:
```bash
pip install pystray pillow pyinstaller
```

Build command:
```bash
pyinstaller --noconsole --onefile --name "SoulframeTracker" monitor.py
```
