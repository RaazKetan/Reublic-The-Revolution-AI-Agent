import asyncio
import json
import time
import re
import pyautogui
import mss
from dotenv import load_dotenv

# ── ADK bytes-safe telemetry patch ───────────────────────────────────────────
class _BytesSafeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return f"<bytes len={len(obj)}>"
        return super().default(obj)

import google.adk.telemetry as _telemetry_mod
import types as _types
_safe_json = _types.ModuleType("json")
_safe_json.__dict__.update(json.__dict__)
_safe_json.dumps = lambda *a, **kw: json.dumps(
    *a, **{**kw, "cls": _BytesSafeEncoder}
)
_telemetry_mod.json = _safe_json
# ─────────────────────────────────────────────────────────────────────────────

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.orchestrator import orchestrator
import memory

load_dotenv()

GAME_MONITOR = 2  # must match tools.py


def focus_game():
    """Clicks the center of the GAME monitor to give it focus."""
    with mss.mss() as sct:
        monitor = sct.monitors[GAME_MONITOR]
        cx = monitor["left"] + monitor["width"] // 2
        cy = monitor["top"] + monitor["height"] // 2
    print(f"  [Focus] Clicking game monitor center ({cx}, {cy})")
    pyautogui.click(cx, cy)
    time.sleep(0.8)


def print_monitors():
    """Prints all detected monitors so user can verify GAME_MONITOR is correct."""
    with mss.mss() as sct:
        print("\nDetected monitors:")
        for i, m in enumerate(sct.monitors):
            print(f"  Monitor {i}: {m['width']}x{m['height']} at x={m['left']}, y={m['top']}")
        print(f"  Game monitor set to: {GAME_MONITOR}")
        print()


async def run_one_turn(runner, session_service, turn_number):
    session_id = f"session_{turn_number}"
    session_service.create_session(
        app_name="RTRMultiAgent",
        user_id="player",
        session_id=session_id,
    )

    state = memory.load()
    last_actions = state["history"][-3:] if state["history"] else []
    phase = state.get("phase", "unknown")
    context = f"Phase: {phase}. Last actions: {json.dumps(last_actions)}" if last_actions else "Start of game."

    message = types.Content(
        role="user",
        parts=[types.Part(text=f"""
Turn {turn_number}. {context}

STRICT RULES:
1. Call VisionAgent ONCE as your first action
2. Call ONE specialist agent based on what VisionAgent reports  
3. STOP after that - do not call anything else
""")]
    )

    action_count = 0
    MAX_ACTIONS = 5

    async for event in runner.run_async(
        user_id="player",
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        print(f"\n  [RESPONSE] {part.text[:300]}")
        elif hasattr(event, "author"):
            action_count += 1
            author = getattr(event, "author", "?")
            
            # print tool calls so we can see what's happening
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        fc = part.function_call
                        args = dict(fc.args) if fc.args else {}
                        if "screenshot_b64" in args:
                            args["screenshot_b64"] = "<image>"
                        print(f"  [{author}] calling → {fc.name}({json.dumps(args)[:150]})")
                    if hasattr(part, "function_response") and part.function_response:
                        fr = part.function_response
                        resp = dict(fr.response) if fr.response else {}
                        if "screenshot_b64" in resp:
                            resp["screenshot_b64"] = "<image>"
                        print(f"  [{author}] result  → {fr.name}: {json.dumps(resp)[:150]}")

            if action_count >= MAX_ACTIONS:
                print(f"\n  [LIMIT] {MAX_ACTIONS} actions done — ending turn.")
                break


async def run():
    print("=================================================")
    print("  Republic: The Revolution - Multi-Agent System  ")
    print("=================================================")

    print_monitors()

    print(f"Game monitor = {GAME_MONITOR} (change GAME_MONITOR in main.py and tools.py if wrong)")
    print("")
    print("Make sure the game is open and FULLSCREEN on that monitor.")
    print("Starting in 8 seconds...")
    time.sleep(8)

    focus_game()
    time.sleep(1)

    session_service = InMemorySessionService()
    runner = Runner(
        agent=orchestrator,
        app_name="RTRMultiAgent",
        session_service=session_service,
    )

    print("\nAgents are live!\n")
    print("Screenshots being saved to: debug_screenshots/")
    print("Open that folder to see exactly what the agent sees.\n")

    turn = 0

    while True:
        turn += 1
        print(f"\n{'='*50}")
        print(f"TURN {turn}")
        print(f"{'='*50}")

        focus_game()

        try:
            await run_one_turn(runner, session_service, turn)
            time.sleep(3)

        except KeyboardInterrupt:
            print("\nStopped by user.")
            break

        except Exception as e:
            err_str = str(e)

            if "1048575" in err_str or "exceeds the maximum" in err_str:
                print(f"  [TOKEN LIMIT] Resetting session.")
                time.sleep(3)

            elif "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                match = re.search(r"retry in (\d+)", err_str)
                wait = int(match.group(1)) + 5 if match else 65
                print(f"  [RATE LIMIT] Waiting {wait}s...")
                time.sleep(wait)
                turn -= 1

            elif "CancelledError" in err_str:
                print(f"  [NETWORK] Hiccup, retrying in 5s...")
                time.sleep(5)
                turn -= 1

            else:
                print(f"  [ERROR] {err_str[:300]}")
                time.sleep(5)


if __name__ == "__main__":
    asyncio.run(run())