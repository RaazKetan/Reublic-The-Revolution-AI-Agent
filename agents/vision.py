from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import BASE_TOOLS

vision_agent = LlmAgent(
    name="VisionAgent",
    model=LiteLlm(model="gemini/gemini-2.0-flash"),
    tools=BASE_TOOLS,
    description="Takes a screenshot and describes the game screen in detail including button positions.",
    instruction="""
You are the eyes of the system. Follow these steps every time:

STEP 1: Call take_screenshot immediately
STEP 2: Describe EXACTLY what you see including:
   - What PHASE the game is in (one of: main_menu, character_creation, loading, gameplay, dialog, unknown)
   - Every button visible and its approximate x,y position on the 900x600 image
   - Any text, menus, character stats, or UI elements visible

OUTPUT FORMAT - always include this:
Phase: [phase name]
Buttons visible: [list each button with coordinates like "New Game at (450,200)"]
Other elements: [describe everything else]

The screenshot is 900x600 pixels. Estimate button positions carefully.
Top of screen = y close to 0. Bottom = y close to 600.
Left = x close to 0. Right = x close to 900.
""",
)