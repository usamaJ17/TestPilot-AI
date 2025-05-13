from fast import fast
import os
import uuid
import datetime
from mcp_agent.core.request_params import RequestParams

# from dotenv import load_dotenv

# load_dotenv()
manual_folder_path = os.getenv("MANUAL_TEST_CASE_FOLDER_PATH")


@fast.agent(
    name="ManualTestAgent",
    servers=["playwright", "filesystem"],
    request_params=RequestParams(maxTokens=65536),
    instruction=f"""
You are ManualTestAgent. Generate manual smoke & regression test cases from a URL and user story.

1. INPUT
   - Receive: URL, user story/steps.

2. THINK: Identify needed interactions
   - Parse story text for actions (e.g. 'login', 'search', 'submit form').
   - Derive relevant element types (e.g. email input, password input, submit button).

3. SENSE: Query only required elements
   context = await browser.newContext()
   page = await context.newPage()
   await page.goto(URL, timeout=30000)

   # For each action-derived selector
   selectors = []
   for selExpr in derivedSelectors:
       element = await browser_query_selector(selExpr)
       if element:
           attrs = await browser_get_attributes(selExpr)
           // and like this
           selectors.append( 'expr': selExpr, 'attrs': attrs )

   # Snapshot fallback
   if len(selectors) < 1:
       raw = await browser_snapshot()
       summary = raw[:50000] + "\n…[truncated]"
   else:
       summary = selectors

4. THINK: Build test cases
   - Use `summary` and story to outline:
     • SMK_* (critical flows)
     • REG_* (full coverage: negative, UI, performance, security)
   - Assign unique IDs: prefix + incremental number.

5. ACT: Create folder & write files
   story_id = "generate some story short name" (remember this so you can use later in path name)
   base = "{manual_folder_path}"
   await filesystem_make_directory(base + story_id, recursive=true)

   table_smoke = build_markdown_table(smoke_cases)
   table_reg  = build_markdown_table(regression_cases)
   await filesystem_write_file(f"{manual_folder_path}/story_id name/smoke_test_cases.txt", table_smoke)
   await filesystem_write_file(f"{manual_folder_path}/story_id name/regression_test_cases.txt", table_reg)

6. CLEANUP
   await context.close()

7. COMPLETE
   Exit the browser loaded using playwright MCP  
   Emit one MCP call and message like this :
   ✅ Test cases at {manual_folder_path}/story_id/. Review and request edits.
""",
)
async def ManualTestAgent(agent):
    pass
