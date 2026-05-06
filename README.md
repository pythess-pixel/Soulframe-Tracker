# Soulframe Tracker

A lightweight, non-intrusive, real-time overlay tracker for Soulframe.

This tool passively parses the game's `EE.log` file to track dynamic events, such as when a procedural Arena spawns. It provides a simple click-through UI overlay that automatically resets when entering and exiting dungeons.

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
