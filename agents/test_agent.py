from fast import fast
import os
from mcp_agent.core.request_params import RequestParams


@fast.agent(
    name="TestAgent",
    servers=["playwright" , "filesystem"],
    request_params=RequestParams(maxTokens=65536),
    instruction=f"""
You will have a URl and  instruction to a specific elements on page, your job is to scrape and return the HTML of that element and every element within it.
You have access to browser using playwright MCP server. make sure that selector are unique to that element
1. INPUT: URL, instruction.
2. OUTPUT: Scraped HTML for the elements.
3. If you are not able to find the elements, return "I am not able to find the elements".
STEPS : 
You can navigate to url
wait for page to load
detect the element container (or div , or section or whatever its using) so you have a little HTML context as well.
scrape that HTML and write it in a file at {os.getenv("TEMP_DATA_PATH")}/testing/<element_name>/.
""",
)
def test_agent():
    pass
