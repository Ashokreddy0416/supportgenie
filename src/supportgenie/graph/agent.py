import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

MODEL = "openai/gpt-oss-120b"


def build_mcp_config():
    return {
        "supportgenie-tools": {
            "command": sys.executable,
            "args": [str(Path("scripts/mcp_server.py").resolve())],
            "transport": "stdio",
        }
    }


async def build_tool_agent():
    client = MultiServerMCPClient(build_mcp_config())
    tools = await client.get_tools()

    llm = ChatGroq(model=MODEL, api_key=os.environ["GROQ_API_KEY"])
    agent = create_react_agent(llm, tools)
    return agent