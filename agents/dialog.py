import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import BASE_TOOLS
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

dialog_agent = LlmAgent(
    name="DialogAgent",
    model=LLM_MODEL,
    tools=BASE_TOOLS,
    description="Handles all popups, dialogs, errors and unexpected screens.",
    instruction="""
You handle any unexpected screen, popup, dialog box or error in the game.

When called:
1. Take a screenshot immediately
2. Identify what type of interruption this is:
   - Tutorial popup: dismiss it by clicking X or OK
   - Event notification: read it, click the best response option
   - Error message: click OK or close
   - Game over screen: click restart or main menu
   - Confirmation dialog: read carefully, click the right option
   - Unknown popup: click the most neutral/safe option (usually Cancel or Close)
3. After dismissing, take another screenshot to confirm the screen is clear
4. Report what you dismissed and what option you chose

NEVER click anything that would quit the game or delete save data.
When in doubt, press Escape first to see if that closes it.
""",
)
