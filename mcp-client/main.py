import asyncio
import sys
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.ollama import Ollama
import os
from langchain.prompts import PromptTemplate

# Flight search prompt template with detailed formatting guidelines
BRAVE_SEARCH_PROMPT = PromptTemplate.from_template(
    """You are a helpful filesystem managing assistant.

{tools}

Use the following format for your reasoning process:
Question: {input}
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: """
)

# Configuration variables
MCP_URL = os.environ.get("MCP_URL", "http://localhost:8000/sse")
MODEL_NAME = os.environ.get("LLM_MODEL", "gemma3:27b")
TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0.7"))

async def setup_agent():
    """Setup and return the filesystem managing agent"""
    try:
        # Connect to MCP server
        print(f"Connecting to MCP server at {MCP_URL}")
        mcp_client = BasicMCPClient(MCP_URL)

        # Get tools list
        print("Fetching available tools...")
        tools = await McpToolSpec(client=mcp_client).to_tool_list_async()
        print(f"Found {len(tools)} tools")

        # Initialize Ollama LLM
        print(f"Initializing Ollama with model {MODEL_NAME}...")
        llm = Ollama(model=MODEL_NAME, temperature=TEMPERATURE)

        # Create agent with flight search prompt
        system_prompt = BRAVE_SEARCH_PROMPT.template.replace("{tools}", "").replace("{tool_names}", "").replace("{input}", "")
        agent = ReActAgent(
            name="BraveSearchAgent",
            llm=llm,
            tools=tools,
            system_prompt=system_prompt,
        )

        return agent
    except Exception as e:
        print(f"Error setting up agent: {str(e)}")
        raise

async def main():
    """Main function to run the filesystem managing application"""
    print("\n🔍 Natural Language File System managing Agent 🔍")
    print("-" * 50)
    print("Ask me anything using natural language!")
    print("Examples:")
    print("  How many files are in the directory?")
    print("  Can you tell me the content of the file that has the biggest size?")
    print("\nType 'exit' or 'quit' to end the session.")
    print("-" * 50)

    print("Make sure the filesystem-mcp-server is running with: sse")

    try:
        # Set up the agent
        agent = await setup_agent()
        print("Ready to help you!")

        # Start conversation loop
        while True:
            user_query = input("\n🔍 Your command: ")

            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using the FileSystem Managing Assistant. Goodbye!")
                break

            if user_query.strip():
                print("Operating...")
                try:
                    response = await agent.run(user_query)
                    print(f"\n{response}")
                except Exception as e:
                    print(f"Error processing query: {e}")

    except Exception as e:
        print(f"Error: {e}")
        print(f"Make sure the server is running at {MCP_URL}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
