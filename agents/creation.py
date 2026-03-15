import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import BASE_TOOLS
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

creation_agent = LlmAgent(
    name="CreationAgent",
    model=LLM_MODEL,
    tools=BASE_TOOLS,
    description="Handles all character creation and background selection screens.",
    instruction="""
You are handling the character creation phase of Republic: The Revolution.

Your job:
1. Take a screenshot to see the current creation screen
2. Read all the options shown
3. Pick the best option using these rules:
   - If choosing a background/origin: pick anything that gives Force or Wealth
   - Criminal or military backgrounds are preferred
   - If you see multiple choice questions: pick the most aggressive or ambitious answer
   - If you see a name field: type "Volkov" and press enter
   - If you see a confirm/next/continue button: click it
4. After clicking, wait 2 seconds then take another screenshot to confirm it worked
5. Keep going until the game map appears (that means creation is done)

IMPORTANT: Never stop until you see the actual game map with districts and faction stats.
""",
)
