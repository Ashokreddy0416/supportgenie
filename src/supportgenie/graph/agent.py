"""An agent that can call MCP tools to take real actions."""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def build_mcp_config():
    return {
        "supportgenie-tools": {
            "command": "uv",
            "args": ["run", "python", "scripts/mcp_server.py"],
            "transport": "stdio",
        }
    }


async def build_tool_agent():
    client = MultiServerMCPClient(build_mcp_config())
    tools = await client.get_tools()

    llm = ChatGroq(model=MODEL, api_key=os.environ["GROQ_API_KEY"])
    agent = create_react_agent(llm, tools)
    return agent