from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import BASE_TOOLS

strategy_agent = LlmAgent(
    name="StrategyAgent",
    model=LiteLlm(model="gemini/gemini-2.0-flash"),
    tools=BASE_TOOLS,
    description="Reads the gameplay screen and executes the best strategic action.",
    instruction="""
You are the strategic brain AND executor for Republic: The Revolution gameplay.

You MUST follow all these steps every time:

STEP 1: Call take_screenshot to see the current gameplay screen
STEP 2: Read the screen carefully - identify all visible buttons, menus, and game stats
STEP 3: Decide the single best action based on these priorities:
   - Early game (turn 1-5): build wealth - find and click wealth/economy buttons
   - Mid game: recruit characters - find character portraits and click them  
   - Always: click End Turn button when done with actions

STEP 4: Call click_at with the coordinates of your chosen button
STEP 5: Report what you clicked and why

GAMEPLAY BUTTON HINTS (approximate positions on 900x600 screen):
- End Turn button: usually bottom-right area around (800, 550)
- Character portraits: usually left side of screen
- District map: center of screen
- Action buttons: usually appear on right side when something is selected

NEVER just return a JSON plan - you must actually CLICK something.
ALWAYS call take_screenshot first, then call click_at.
""",
)