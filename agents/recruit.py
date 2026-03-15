import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import BASE_TOOLS
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

recruit_agent = LlmAgent(
    name="RecruitAgent",
    model=LLM_MODEL,
    tools=BASE_TOOLS,
    description="Finds valuable NPCs and recruits them to the faction.",
    instruction="""
You handle all character recruitment in Republic: The Revolution.

When called your job is to find and recruit a new character.
Steps:
1. Take a screenshot to see the current screen
2. Open the characters or contacts panel if not already open
3. Look for characters with these desirable traits:
   - High loyalty score (above 60 is ideal)
   - Skills that complement current faction weaknesses
   - Not already in an enemy faction
4. Click on the best candidate
5. Choose the best recruitment method available (persuade, bribe, etc.)
6. Confirm the action
7. Screenshot to verify they joined

If no good candidates are visible, scroll through the list to find better ones.
Report back who you recruited and their stats.
""",
)
