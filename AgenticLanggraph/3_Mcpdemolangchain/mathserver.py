# =====================================================================
# 1. WHAT THE CODE IS ABOUT:
# This code defines and runs a Model Context Protocol (MCP) server
# named "MathServer". It exposes mathematical tools ("add" and
# "multiply") that can be dynamically called by MCP-compliant LLMs 
# (like Claude Desktop, LangChain MCP adapters, or custom LLM agents) 
# to perform calculations.
#
# 2. WHAT IS FASTMCP:
# FastMCP is a high-level, developer-friendly Python framework (provided 
# by the official 'mcp' library) that simplifies building MCP servers. 
# Similar to FastAPI or Flask, it uses decorators (like @mcp.tool) to 
# automatically handle JSON-RPC message passing, client-server handshake, 
# input/output validation, and schema generation for tools.
# =====================================================================


from mcp.server.fastmcp import FastMCP

# Initialize the MCP server instance, naming it "MathServer". 
# This instance will manage and register all our tools, resources, and prompts.
mcp = FastMCP("MathServer")

# Register the following Python function as an MCP Tool.
# The @mcp.tool() decorator tells FastMCP to expose this function to clients.
# FastMCP uses the function name, arguments, type hints (a: int, b: int), 
# return type (-> int), and the docstring to generate a schema for the client LLM.
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together. Use this tool when you need to sum or add two integers."""
    # Return the sum of the two inputs.
    return a + b
# Register the "multiply" function as a second MCP Tool.
# The docstring below tells the LLM exactly what this tool does and when to call it.
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together. Use this tool when you need the product of two integers."""
    return a * b

# Ensure that the server runs only when this specific script is executed directly (not when imported).
if __name__ == "__main__":
    # Start the MCP server and establish standard input/output (stdio) as the transport channel.
    # Use standard input/output (stdin and stdout) to send and recieve messages to the client.
    # The client parent process (e.g., LangChain or Claude Desktop) will spawn this server as a
    # subprocess and read/write to its standard output and input streams to exchange messages.
    mcp.run(transport="stdio")

#this type of server can be used for testing locally 
#but not for production. For production we use streamable-http transport 