import time
import os
import winsound
import tkinter as tk
import ctypes
import ctypes.wintypes
import threading
import queue
import re

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pass # Will be installed by pip

LOG_FILE_PATH = os.path.join(os.getenv('LOCALAPPDATA'), 'Soulframe', 'EE.log')
SEARCH_TERMS = ["/Layer8/Prefab7/"]

# Regex patterns for new features
REGEX_RESET = re.compile(r"StreamTrigger: Streaming started on level /SF/Levels/Procs/")
REGEX_EXIT = re.compile(r"STATS EXIT_LEVEL")

def set_clickthrough(hwnd):
    # Windows API Constants for transparent and click-through window
    WS_EX_LAYERED = 0x00080000
    WS_EX_TRANSPARENT = 0x00000020
    GWL_EXSTYLE = -20
    user32 = ctypes.windll.user32
    ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

def listen_for_exit():
    user32 = ctypes.windll.user32
    # Register Ctrl+Shift+Q (MOD_CONTROL=0x0002, MOD_SHIFT=0x0004, Q=0x51)
    if not user32.RegisterHotKey(None, 1, 0x0002 | 0x0004, 0x51):
        print("Failed to register hotkey")
        return
    
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        if msg.message == 0x0312: # WM_HOTKEY
            os._exit(0)

def create_image():
    # Generate an image for the tray icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(18, 18, 18))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, width - 16, height - 16), fill=(0, 255, 204))
    return image

def quit_action(icon, item):
    icon.stop()
    os._exit(0)

def setup_tray():
    image = create_image()
    menu = pystray.Menu(pystray.MenuItem('Exit Tracker', quit_action))
    icon = pystray.Icon("SoulframeTracker", image, "Soulframe Tracker", menu)
    icon.run()

def monitor_log(msg_queue):
    print(f"Monitoring {LOG_FILE_PATH} in real-time...")
    print(f"Looking for Arena: {SEARCH_TERMS}")
    print("\nKeep this console window open while you play.")
    print("-" * 60)
    
    # Wait for the log file to exist if the game isn't running yet
    if not os.path.exists(LOG_FILE_PATH):
        print(f"Waiting for game to start... (Log file not found)")
        msg_queue.put(("STATUS", "Waiting..."))
        while not os.path.exists(LOG_FILE_PATH):
            time.sleep(1)
            
    print("Log file found. Monitoring started...")
    msg_queue.put(("STATUS", "Active"))

    with open(LOG_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as file:
        # Move to the end of the file to only read new logs generated while playing
        file.seek(0, 2)
        
        while True:
            line = file.readline()
            if not line:
                # No new line, wait a bit before checking again
                time.sleep(0.5)
                continue
            
            # 1. Check for level enter (Auto-Reset)
            if REGEX_RESET.search(line):
                print("\n[INFO] Entered new procedural level. Resetting tracker...")
                msg_queue.put(("RESET", ""))
                continue

            # Check for level exit
            if REGEX_EXIT.search(line):
                print("\n[INFO] Exited level. Clearing tracker...")
                msg_queue.put(("EXIT", ""))
                continue

            # 2. Check for Arena
            if any(term in line for term in SEARCH_TERMS):
                print("\n" + "="*60)
                print("🚨 ARENA SPAWNED! 🚨")
                print(f"Log matched: {line.strip()}")
                print("="*60 + "\n")
                
                msg_queue.put(("ARENA", "Found!"))
                
                # Play an alert sound (3 beeps)
                for _ in range(3):
                    winsound.Beep(1000, 400)
                    time.sleep(0.1)
                continue

class OverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Soulframe Tracker")
        self.root.overrideredirect(True) # Remove window borders
        self.root.attributes("-topmost", True) # Always on top
        self.root.attributes("-alpha", 0.85) # Semi-transparent dark background
        
        bg_color = "#121212"
        self.root.config(bg=bg_color)
        
        # Position the overlay at the top left of the screen
        x = 20
        y = 50 
        self.root.geometry(f"240x110+{x}+{y}")
        
        # UI Layout
        frame = tk.Frame(root, bg=bg_color, padx=15, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(frame, text="Soulframe Tracker", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg=bg_color, anchor="w")
        title.pack(fill=tk.X, pady=(0, 10))
        
        # Arena State
        arena_frame = tk.Frame(frame, bg=bg_color)
        arena_frame.pack(fill=tk.X, pady=2)
        tk.Label(arena_frame, text="Arena:", font=("Segoe UI", 11), fg="#cccccc", bg=bg_color).pack(side=tk.LEFT)
        self.arena_val = tk.Label(arena_frame, text="Waiting...", font=("Segoe UI", 11, "bold"), fg="#ffcc00", bg=bg_color)
        self.arena_val.pack(side=tk.RIGHT)
        
        # Hint text
        hint = tk.Label(frame, text="Ctrl+Shift+Q to exit", font=("Segoe UI", 8), fg="#666666", bg=bg_color, anchor="e")
        hint.pack(fill=tk.X, pady=(5, 0))
        
        self.root.update()
        
        # Make the window click-through so it doesn't interfere with the game
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        set_clickthrough(hwnd)
        
        self.msg_queue = queue.Queue()
        
        # Start monitoring in a separate thread so it doesn't block the GUI
        self.monitor_thread = threading.Thread(target=monitor_log, args=(self.msg_queue,), daemon=True)
        self.monitor_thread.start()
        
        # Start checking the queue for messages from the monitor thread
        self.check_queue()

    def check_queue(self):
        try:
            while True:
                msg_type, msg_val = self.msg_queue.get_nowait()
                if msg_type == "STATUS":
                    if "Active" in msg_val:
                        self.arena_val.config(text="None", fg="#ff4444")
                    else:
                        self.arena_val.config(text="Waiting...", fg="#ffcc00")
                elif msg_type == "ARENA":
                    self.arena_val.config(text="Found!", fg="#00ff00")
                elif msg_type == "RESET":
                    # When entering a new dungeon
                    self.arena_val.config(text="None", fg="#ff4444")
                elif msg_type == "EXIT":
                    # When exiting back to open world/hub
                    self.arena_val.config(text="Waiting...", fg="#ffcc00")
        except queue.Empty:
            pass
        finally:
            # Check again in 100ms
            self.root.after(100, self.check_queue)

if __name__ == "__main__":
    # Start the hotkey listener in a background thread
    hotkey_thread = threading.Thread(target=listen_for_exit, daemon=True)
    hotkey_thread.start()

    # Start the system tray icon in a background thread
    try:
        tray_thread = threading.Thread(target=setup_tray, daemon=True)
        tray_thread.start()
    except Exception as e:
        print(f"Tray icon failed to start: {e}")

    root = tk.Tk()
    app = OverlayApp(root)
    try:
        # Start the GUI main loop
        root.mainloop()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
