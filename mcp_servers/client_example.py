"""
FastMCP Client Example - Book Tools

Demonstrates how to connect to and use the Book Tools MCP server.
This client shows:
- Connecting to an MCP server (both stdio and HTTP)
- Calling tools with arguments
- Handling responses
"""

import asyncio
from fastmcp import Client


async def main():
    """Example client demonstrating book tools server."""
    
    print("=" * 60)
    print("Book Tools MCP Server Client Example")
    print("=" * 60)
    
    # For stdio transport (uncomment and run the server with: python book_tools_server.py)
    # async with Client("stdio", ["python", "book_tools_server.py"]) as client:
    
    # For HTTP transport (run server first with: python book_tools_server.py --transport http --port 8000)
    async with Client("http://localhost:8000/mcp") as client:
        
        print("\n1. Listing available books...")
        list_result = await client.call_tool("list_available_books", {})
        books = list_result.content[0].text
        print(f"Available books:\n{books}\n")
        
        print("\n2. Getting preview of Pride and Prejudice...")
        preview_result = await client.call_tool(
            "get_book_preview",
            {"book_name": "pride_and_prejudice", "lines": 5}
        )
        print(f"{preview_result.content[0].text}\n")
        
        print("\n3. Getting statistics for a book...")
        stats_result = await client.call_tool(
            "get_book_statistics",
            {"book_name": "pride_and_prejudice"}
        )
        print(f"Book statistics:\n{stats_result.content[0].text}\n")
        
        print("\n4. Searching for a term in a book...")
        search_result = await client.call_tool(
            "search_in_book",
            {"book_name": "pride_and_prejudice", "search_term": "love"}
        )
        print(f"Search results:\n{search_result.content[0].text}\n")
        
        print("\n5. Comparing two books...")
        compare_result = await client.call_tool(
            "compare_books",
            {"book1": "pride_and_prejudice", "book2": "moby_dick"}
        )
        print(f"Comparison:\n{compare_result.content[0].text}\n")


if __name__ == "__main__":
    asyncio.run(main())
