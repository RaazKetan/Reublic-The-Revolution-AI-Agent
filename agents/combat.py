import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import BASE_TOOLS
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

combat_agent = LlmAgent(
    name="CombatAgent",
    model=LLM_MODEL,
    tools=BASE_TOOLS,
    description="Executes Force-based actions like intimidation and rallies.",
    instruction="""
You handle all Force-based actions in Republic: The Revolution.

When called you will be told what Force action to perform and on whom.
Your job:
1. Take a screenshot to see current screen
2. Find the target character or district on screen
3. Click them to select them
4. Find and click the correct Force action button (Intimidate, Rally, etc.)
5. Confirm the action if a dialog appears
6. Take a screenshot after to verify it worked

Force actions you know how to do:
- Intimidate: click character, click intimidate button
- Organize rally: click district, click rally button  
- Deploy agents: click agent portrait, click deploy

If you cannot find the right button, take a screenshot and look more carefully.
Never give up — try scrolling or clicking different areas of the UI.
""",
)
