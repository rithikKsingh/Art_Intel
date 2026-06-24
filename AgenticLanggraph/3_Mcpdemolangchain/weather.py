from mcp.server.fastmcp import FastMCP

mcp=FastMCP("WeatherServer")

@mcp.tool()
async def get_weather(location:str)->str:
    """Get the weather location"""
    return f"The weather at {location} is sunny."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
    


# 1. Starts a Web Server
# Instead of communicating via local standard input/output (stdio), 
# the server launches a lightweight HTTP web server (using Uvicorn/Starlette 
# under the hood) that binds by default to http://127.0.0.1:8000.

# 2. Establishes SSE (Server-Sent Events) Transport
# It handles communication using a hybrid HTTP transport pattern:

# Client-to-Server (Requests): The client (like an LLM agent or client application) 
# sends tool-execution requests to the server via standard HTTP POST requests.

# Server-to-Client (Responses & Events): The server sends responses, status updates, 
# and notifications back to the client using Server-Sent Events (SSE) over a 
# single, persistent HTTP connection.

# 3. Enables Network Access
# Unlike stdio (which requires the client to spawn the server locally as a subprocess), 
# the streamable-http transport allows the MCP server to run as a standalone network 
# service. Any client on the network can connect to it remotely via its HTTP address.

# It basically acts as an API endpoint