from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv

load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "mathserver":{
                "command":"python",
                "args":[
                    "mathserver.py"
                ],   # ensure correct absolute path of the mcp server
                "transport":"stdio"
            },
            "weather":{
                "url":"http://localhost:8000/mcp", # ensure server is running here
                # NOTE: here the FastMCP server exposes its API on the /mcp endpoint, 
                # not at the root (/). 
                # thats why we have used: http://localhost:8000/mcp 
                # instead of http://localhost:8000/
                "transport":"streamable-http"
            }
        }
    )
    
    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
    
    tools=await client.get_tools()
    model=ChatGroq(
        model="qwen/qwen3-32b"
    )
    agent=create_react_agent(model,tools)
    
    
    math_response=await agent.ainvoke(
        {
            "messages":[
                {"role":"user","content":"What's (3+2)*10"}
            ]
        }
    )
    
    weather_response=await agent.ainvoke(
        {
            "messages":[
                {"role":"user","content":"What is the weather in Bangalore?"}
            ]
        }
    )
    
    print("\n\n\n================ math response")
    print(math_response['messages'][-1].content)
    print("\n\n\n================ weather response")
    print(weather_response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())

