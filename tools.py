import pyautogui
import base64
import time
import os
from io import BytesIO
from PIL import Image
import mss
from google.adk.tools import FunctionTool

pyautogui.FAILSAFE = True

# ── find the game monitor ─────────────────────────────────────────────────────
# mss lists all monitors. Index 0 = all screens combined, 1 = first monitor, 2 = second, etc.
# Change GAME_MONITOR = 1 if game is on monitor 1, or 2 if on monitor 2
GAME_MONITOR = 2  # <-- SET THIS: 1 = laptop screen (first monitor)
 
# screenshot save folder so you can see what the agent sees
SCREENSHOT_DIR = "debug_screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
screenshot_counter = [0]

def take_screenshot() -> dict:
    """Takes a screenshot of the game monitor only."""
    with mss.mss() as sct:
        # grab only the game monitor
        monitor = sct.monitors[GAME_MONITOR]
        print(f"  [Vision] Capturing monitor {GAME_MONITOR}: "
              f"{monitor['width']}x{monitor['height']} "
              f"at x={monitor['left']}, y={monitor['top']}")
        
        raw = sct.grab(monitor)
        img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
        
        # shrink to save tokens
        img = img.resize((900, 600), Image.LANCZOS)
        
        # save for debugging so you can see what agent sees
        screenshot_counter[0] += 1
        save_path = os.path.join(SCREENSHOT_DIR, f"shot_{screenshot_counter[0]:04d}.jpg")
        img.save(save_path, format="JPEG", quality=60)
        print(f"  [Vision] Saved screenshot → {save_path}")
        
        # encode for API
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=60)
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        kb = len(buffer.getvalue()) // 1024
        print(f"  [Vision] Screenshot size: {kb}KB")
        
        return {"screenshot_b64": b64, "media_type": "image/jpeg"}


def click_at(x: int, y: int) -> dict:
    """Clicks at x, y ON THE GAME MONITOR.
    Args:
        x: horizontal pixel position on the game monitor
        y: vertical pixel position on the game monitor
    """
    with mss.mss() as sct:
        monitor = sct.monitors[GAME_MONITOR]
        # offset click by the monitor's top-left position
        real_x = monitor["left"] + x
        real_y = monitor["top"] + y
    
    print(f"  [Click] Game coords ({x},{y}) → Screen coords ({real_x},{real_y})")
    pyautogui.moveTo(real_x, real_y, duration=0.4)
    pyautogui.click()
    time.sleep(1.5)
    return {"status": "clicked", "x": x, "y": y}


def double_click_at(x: int, y: int) -> dict:
    """Double clicks at x, y on the game monitor.
    Args:
        x: horizontal pixel position on the game monitor
        y: vertical pixel position on the game monitor
    """
    with mss.mss() as sct:
        monitor = sct.monitors[GAME_MONITOR]
        real_x = monitor["left"] + x
        real_y = monitor["top"] + y
    
    print(f"  [DblClick] ({x},{y}) → ({real_x},{real_y})")
    pyautogui.moveTo(real_x, real_y, duration=0.4)
    pyautogui.doubleClick()
    time.sleep(1.5)
    return {"status": "double_clicked"}


def press_key(key: str) -> dict:
    """Presses a keyboard key.
    Args:
        key: key name e.g. enter, escape, space, tab, up, down
    """
    print(f"  [Key] Pressing: {key}")
    pyautogui.press(key)
    time.sleep(1)
    return {"status": "pressed", "key": key}


def wait(seconds: int) -> dict:
    """Waits for the game to respond.
    Args:
        seconds: how long to wait
    """
    print(f"  [Wait] Waiting {seconds}s...")
    time.sleep(seconds)
    return {"status": "waited", "seconds": seconds}


def scroll_down() -> dict:
    """Scrolls down on the game screen."""
    with mss.mss() as sct:
        monitor = sct.monitors[GAME_MONITOR]
        cx = monitor["left"] + monitor["width"] // 2
        cy = monitor["top"] + monitor["height"] // 2
    pyautogui.moveTo(cx, cy)
    pyautogui.scroll(-3)
    time.sleep(0.5)
    return {"status": "scrolled"}


screenshot_tool  = FunctionTool(take_screenshot)
click_tool       = FunctionTool(click_at)
dbl_click_tool   = FunctionTool(double_click_at)
key_tool         = FunctionTool(press_key)
wait_tool        = FunctionTool(wait)
scroll_tool      = FunctionTool(scroll_down)

BASE_TOOLS = [screenshot_tool, click_tool, dbl_click_tool, key_tool, wait_tool, scroll_tool]