from fast import fast
from agents import manual_agent
from agents import wdio_agent


@fast.orchestrator(
    name="ManualOrchestrator",
    agents=["ManualTestAgent", "BulkAutomationAgent", "AutoValidateAgent"],
    instruction="""
You are ManualOrchestrator: coordinate manual-case creation, bulk automation, and validation.

1. Ask user for URL and story_id (e.g. story_products_appearance).
2. Call ManualTestAgent with URL & story to draft manual cases.
3. Present generated REG_* IDs and ask: “Reply 'all' to automate all, or list specific IDs.”
4. If user replies 'all', call BulkAutomationAgent with story_id; else for each ID call WDIOAutomationAgent.
5. After automation, call AutoValidateAgent to lint & run the new specs.
6. Summarize results: list of generated spec paths and pass/fail status.
""",
)
def ManualOrchestrator():
    pass


@fast.chain(
    name="BulkAutomationAgent",
    sequence=["WDIOAutomationAgent"],
    instruction="""
You are BulkAutomationAgent.

1. INPUT: story_id.
2. Read /Users/usama.jalal/mcp/mcp_test_1/{story_id}/regression_test_cases.txt and extract all REG_* IDs.
3. For each ID, call WDIOAutomationAgent(story_id, test_id).
4. Collect each agent’s output (file paths) and return list.
""",
)
def BulkAutomationAgent():
    pass


@fast.evaluator_optimizer(
    name="AutoValidateAgent",
    generator="BulkAutomationAgent",
    evaluator="WDIOAutomationAgent",
    min_rating="GOOD",
    max_refinements=2,
)
def AutoValidateAgent():
    pass
