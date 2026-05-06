# Soulframe Tracker

A lightweight, non-intrusive, real-time overlay tracker for Soulframe.

This tool passively parses the game's `EE.log` file to track dynamic events, such as when a procedural Arena spawns. It provides a simple click-through UI overlay that automatically resets when entering and exiting dungeons.

## Usage
1. Run `monitor.py` or the compiled `SoulframeTracker.exe` before or during a Soulframe session.
2. Enter a dungeon and the overlay will appear in the top-left corner.
3. Wait for the "Found!" text and beep sound when an Arena spawns.
4. To close, right-click the green system tray icon and select "Exit Tracker", or press `Ctrl+Shift+Q`.

## Compiling from source (for beginners)

If you want to build the `.exe` file yourself instead of downloading it, follow these simple steps:

1. **Install Python**: Download and install [Python](https://www.python.org/downloads/). During installation, make sure to check the box that says **"Add Python to PATH"**.
2. **Download this code**: Click the green "Code" button at the top of this GitHub page and select "Download ZIP". Extract the folder to your computer.
3. **Open Command Prompt**: Open the extracted folder, click on the address bar at the top of the file explorer, type `cmd`, and press **Enter**. This will open a black command window.
4. **Install required libraries**: Copy the following command, paste it into the command window, and press Enter:
   ```cmd
   pip install pystray pillow pyinstaller
   ```
5. **Compile the program**: Finally, copy and paste this command and press Enter:
   ```cmd
   pyinstaller --noconsole --onefile --name "SoulframeTracker" monitor.py
   ```
6. **Find your `.exe`**: Once it finishes, a new folder named `dist` will appear. Inside it, you will find your ready-to-use `SoulframeTracker.exe`!
