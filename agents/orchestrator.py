from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from tools import BASE_TOOLS

from agents.vision    import vision_agent
from agents.creation  import creation_agent
from agents.strategy  import strategy_agent
from agents.combat    import combat_agent
from agents.economy   import economy_agent
from agents.recruit   import recruit_agent
from agents.dialog    import dialog_agent
from agents.clicker   import clicker_agent

vision_tool   = AgentTool(agent=vision_agent)
creation_tool = AgentTool(agent=creation_agent)
strategy_tool = AgentTool(agent=strategy_agent)
combat_tool   = AgentTool(agent=combat_agent)
economy_tool  = AgentTool(agent=economy_agent)
recruit_tool  = AgentTool(agent=recruit_agent)
dialog_tool   = AgentTool(agent=dialog_agent)
clicker_tool  = AgentTool(agent=clicker_agent)

orchestrator = LlmAgent(
    name="Orchestrator",
    model=LiteLlm(model="gemini/gemini-2.0-flash"),
    tools=[
        *BASE_TOOLS,
        vision_tool,
        creation_tool,
        strategy_tool,
        combat_tool,
        economy_tool,
        recruit_tool,
        dialog_tool,
        clicker_tool,
    ],
    description="Master controller that sees the game and takes action.",
    instruction="""
You control a game called Republic: The Revolution autonomously.

EVERY TURN follow these exact steps:

STEP 1: Call VisionAgent with request "describe screen with button coordinates"
        VisionAgent will return the phase and button positions.

STEP 2: Based on the phase VisionAgent reports:

  Phase = "main_menu":
    → Call ClickerAgent with request "take a screenshot and click the New Game or New Campaign button"

  Phase = "character_creation":
    → Call CreationAgent with request "take a screenshot and handle the current character creation screen"

  Phase = "loading":
    → Call wait tool for 4 seconds. Done.

  Phase = "dialog" or popup visible:
    → Call DialogAgent with request "take a screenshot and dismiss the popup"

  Phase = "gameplay":
    → Call StrategyAgent with request "take a screenshot, read the game state, and execute the best action by clicking"

  Phase = "unknown":
    → Call ClickerAgent with request "take a screenshot, press Escape key, then describe what you see"

STEP 3: STOP. Do not call any more agents. Just say what happened.

CRITICAL:
- You MUST call VisionAgent first every single turn
- You MUST call exactly one specialist after VisionAgent
- STOP after that one specialist call
- Do NOT call click_at yourself - always delegate to ClickerAgent
- Do NOT take screenshots yourself - VisionAgent does that
""",
)