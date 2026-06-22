"""Quick manual tester: send a message to the tool-using agent and print the reply."""

import asyncio
import sys

from supportgenie.graph.agent import build_tool_agent


async def ask(question):
    agent = await build_tool_agent()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    print(f"\nYou: {question}")
    print(f"SupportGenie: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "where is my order 12345?"
    asyncio.run(ask(question))