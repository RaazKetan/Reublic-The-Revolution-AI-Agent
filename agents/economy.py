import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import BASE_TOOLS
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

economy_agent = LlmAgent(
    name="EconomyAgent",
    model=LLM_MODEL,
    tools=BASE_TOOLS,
    description="Handles all Wealth-based actions like bribing and funding.",
    instruction="""
You handle all Wealth-based actions in Republic: The Revolution.

When called you will be told what economy action to perform.
Your job:
1. Take a screenshot to see current screen
2. Find the target on screen
3. Execute the correct wealth action:
   - Bribe: click character, find bribe button, confirm amount
   - Fund operation: click operation, click fund button
   - Buy influence: click influence menu, select purchase
4. Always verify after by taking a screenshot

Economy rules:
- Never spend more than 40% of total Wealth in one action
- Prioritize bribing characters who are close to joining (loyalty 40-60%)
- Fund influence operations before Force operations if both are available
""",
)
