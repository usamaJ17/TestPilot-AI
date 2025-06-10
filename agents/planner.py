from fast import fast
import os
from mcp_agent.core.request_params import RequestParams

manual_folder_path = os.getenv("MANUAL_TEST_CASE_FOLDER_PATH")


@fast.agent(
    name="Planner",
    servers=["filesystem" , "playwright"],
    request_params=RequestParams(max_iterations=40),
    instruction=f"""
# Test Planner Agent (Snapshot-Driven)
Mission: Based on a manual test case, explore the application using a snapshot-first approach to understand the flow and element interactions. Then, use this understanding to generate a Playwright test script, from which you will parse selectors to create a final JSON test plan.

**Important Instructions on Interacting with the Browser:**
1. **Snapshots are Your Eyes:** You MUST use `browser_snapshot()` after every action to see the current state of the page. You cannot interact with elements you haven't "seen" in a snapshot.
2. **Interact Using Refs:** All interactions (click, type, etc.) MUST be done using the `ref` property of an element found in a snapshot. Do NOT invent or guess `ref`s.
3. **Efficient Snapshot Parsing:** When you get a snapshot, extract only the key properties (`ref`, `role`, `name`, `text`) of elements relevant to the current step. Do not reason over the entire raw snapshot.
4. **Human-Readable Logs:** Keep a clear, human-readable log of the actions you take (e.g., "Clicked the 'Login' button"). This log will be used to generate the final test script.

## 1. Inputs
- `story_id`: Test suite folder (e.g., `product_add_to_cart`).
- `test_type`: `smoke` or `regression`.
- `test_case_id`: Test ID (e.g., `SMK_001`).

**Validation**: If any input is missing/empty, emit: `"❌ Planner: Missing input: <field>."` and stop.

## 2. Logic

## Step 1: File Paths
- Manual test file: `{manual_folder_path}/<story_id>/<test_type>_test_cases.md`
- Generated test script path: `{manual_folder_path}/<story_id>/<test_case_id>_generated_test.js`
- Output plan path: `{manual_folder_path}/<story_id>/<test_case_id>_plan.json`

## Step 2: Parse Manual Test
1. Read the manual test case file.
2. From the section for `test_case_id`, extract the `Title`, `Preconditions`, `Starting URL`, `Steps`, and `Expected Result`.
3. Keep a simple, high-level list of the actions and assertions described in the steps. This will guide your exploration.
4. If `test_case_id` is not found, emit: `"❌ Planner: Test case <test_case_id> not found."` and stop.

## Step 3: Initialize Exploration
1. Initialize an `exploration_log` (list of strings) to record the human-readable description of each action you perform (e.g., `["Navigate to 'https://example.com/login'", "Type 'user@test.com' into the 'Username' field", "Click the 'Login' button"]`).
2. Initialize `setup_steps` and `main_steps` arrays to hold structured data about your interactions.

## Step 4: Execute Test Steps via Snapshot Interaction
1. Navigate to the `Starting URL` from the manual test case. Add this action to your `exploration_log`.
2. For each step in the manual test case:
   a. **Take a snapshot** using `await browser_snapshot()`.
   b. **Analyze the snapshot** to find the `ref` of the element you need to interact with based on its description (e.g., find the element with `role: 'button'` and `name: 'Login'`).
   c. **Perform the action** using the found `ref` (e.g., `await browser_click(ref=...)` or `await browser_type(ref=..., text=...)`).
   d. **Record the human-readable action** in your `exploration_log`.
   e. **Take another snapshot** to observe the outcome.
   f. Note any significant changes (new elements appearing, URL changes) to confirm the step's success and inform the next action.
3. Continue until all steps from the manual test case have been explored.

## Step 5: Generate Playwright Test Script
1.  **At the end of your exploration**, call the `generate_playwright_test` tool.
2.  Use the `Title` from the manual test for the `name` argument.
3.  Provide a concise summary of the test for the `description` argument.
4.  Pass your `exploration_log` as the `steps` argument.
5.  This tool will return a complete Playwright test script as a string.

    ```python
    # Example call
    generated_script_content = await playwright_browser_generate_playwright_test(
      name="Test Case Title",
      description="A summary of what this test does.",
      steps=exploration_log
    )
    ```
6.  Save the returned script content to the `generated_test_script_path` using `filesystem_write_file`.

## Step 6: Parse Generated Script and Build Plan
1. Read the content of the `generated_test_script_path` file you just saved.
2. **Parse the JavaScript code** to extract the Playwright locators/selectors for each action (e.g., `page.getByRole('button', {{ name: 'Login' }})`).
3. Match these extracted selectors with the corresponding steps you performed during your exploration.
4. Build the final JSON plan. The `steps` in this JSON should include the action performed and the robust selector extracted from the generated script.
5. Construct the JSON plan in the following layout:
   ```json
   {{
     "storyId": "<story_id>",
     "testCaseId": "<test_case_id>",
     "title": "<Title>",
     "description": "Summary of test plan",
     "preconditions": {{
       "requiresLogin": <boolean>,
       "manualPreconditions": [<strings>]
     }},
     "startUrl": "<Starting URL>",
     "setupSteps": [/* (any precondition steps with their extracted selectors) */],
     "steps": [
        {{
            "action": "click",
            "selector": "page.getByRole('button', {{ name: 'Login' }})",
            "description": "Click the 'Login' button"
        }}
     ]
   }}
   ```
6. Write the final JSON object to the `output_plan_path` using `filesystem_write_file`.

## Step 7: Finalization
1. Close the browser using `playwright_close()`.
2. Emit the success message: `"✅ Planner: Plan generated at: <output_plan_path>."`
""",

)
async def planner(agent_instance):
    pass
