# TestPilot-AI

**TestPilot-AI** is an AI-powered QA co-pilot that transforms user stories into production-ready test suites. From generating manual test cases to converting them into automated WDIO specs, it handles the full testing pipeline intelligently—guided by Model Context Protocol (MCP) and LLMs.

---

## Features

* **Story to Spec**: Input a URL and user story, get detailed smoke & regression test cases.
* **Manual Test Generation**: Creates markdown-based test case files with clear formatting.
* **Bulk Automation**: Converts all test cases in a story folder into TypeScript WDIO specs using clean Page Object Model.
* **Selector-Aware**: Learns real selectors during test execution—no brittle XPath or guesswork.

---

## How It Works

1. **ManualTestAgent**

   * Input: a URL and user story
   * Output: smoke & regression test case files in Markdown table format


2. **WDIOAutomationAgent**

   * Input: story folder + test type (`regression` or `smoke`) + test case ID
   * Reads test steps, performs them in browser using Playwright MCP
   * Extracts real selectors and builds maintainable test code
   * Output: automated `.spec.ts` files + page objects written to the WDIO project


---

## Requirements

* Python 3.13+
* Node.js (for MCP servers like Playwright & filesystem)
* [Playwright MCP](https://www.npmjs.com/package/@playwright/mcp) & [filesystem MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)installed

---

## Setting Up

### Clone the repo

```bash
git clone https://github.com/usamaJ17/TestPilot-AI.git
cd TestPilot-AI
```

### Setting enviroment variables

- rename .env.example with .env  
- Add your API keys value in env variables   
- Absolute path to your manual folder (in which all manual test cases files will be generated)
- Path to your  WDIO folder (make sure that thisfolder has WDIO project already setup , Can setup new WDIO by  following instructions [HERE](https://webdriver.io/docs/gettingstarted#initiate-a-webdriverio-setup))

### Installing

Create a .venv folder and install dependencies isolation
```bash
uv venv
```

Activating it 
```bash
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```

Installing dependencies
```bash
uv pip install -r requirements.txt
```

Staring application
```bash
uv run main.py
```

## Testing Agents 
Manual agent and WDIO automation agent can be switched by pressing '@' and then selecting required agent.

### ManualTestAgent
Correct way of prompt is :
navigate to URL : (add your page URL) , make  manual test cases for (section you want to test)

Example : 
navigate to URL : bing.com , make  manual test cases for searchbox 

Output:
This will create a new folder and name it an appropriate story_id in  your manual test folder, smoke  and regression test cases files will be present in this folder\

### WDIOAutomationAgent
Correct way of prompt is :
story_id is (story_id folder name, which manual test agent generated), I  wanted to create automated test spec for (regression or smoke , which  you want) test with ID (add your test ID)

Example : 
story_id is bing_search, I  wanted to create automated test spec for regression test with ID : REG_001

Output:
This will create new files in your specified WDIO directory. 


---

## Tech Stack

* [Python uv](https://docs.astral.sh/uv/)
* [FastAgent Framework](https://fast-agent.ai)
* [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)

---

## License

MIT License — use freely, modify, and contribute.