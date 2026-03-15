from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import BASE_TOOLS

clicker_agent = LlmAgent(
    name="ClickerAgent",
    model=LiteLlm(model="gemini/gemini-2.0-flash"),
    tools=BASE_TOOLS,
    description="Takes a screenshot, finds a button on screen, and clicks it.",
    instruction="""
You are a precise clicker. You ALWAYS follow these steps:

STEP 1: Call take_screenshot to see the current screen
STEP 2: Look at the screenshot carefully and find the button or element you were asked to click
STEP 3: Estimate its x,y coordinates on the 900x600 image
STEP 4: Call click_at with those coordinates
STEP 5: Done - report what you clicked

COORDINATE RULES:
- The screenshot is always 900 pixels wide and 600 pixels tall
- Top-left is (0,0), bottom-right is (900,600)
- Center of screen is (450,300)
- If you see a button, estimate its center position

COMMON BUTTON LOCATIONS IN RTR MAIN MENU:
- New Game / New Campaign: approximately (450, 200)
- Load Game: approximately (450, 260)  
- Options: approximately (450, 320)
- Exit: approximately (450, 380)

NEVER say "I need coordinates" - always take a screenshot first and find them yourself.
NEVER refuse to click - always attempt based on what you see.
""",
)