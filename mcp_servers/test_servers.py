#!/usr/bin/env python3
"""
Testing Guide for FastMCP Servers

This file provides practical examples for testing the MCP servers.
Run individual sections or the entire file to test all servers.
"""

import asyncio
import json
from pathlib import Path


async def test_book_tools_server():
    """Test the Book Tools Server."""
    print("\n" + "=" * 70)
    print("TESTING: Book Tools Server")
    print("=" * 70)
    
    from fastmcp import Client
    import sys
    
    try:
        # Try HTTP connection first
        async with Client("http://localhost:8000/mcp") as client:
            print("✓ Connected to HTTP server at localhost:8000")
            
            # Test 1: List books
            print("\n[Test 1] Listing available books...")
            result = await client.call_tool("list_available_books", {})
            print(f"Result: {result.content[0].text[:200]}...")
            
            # Test 2: Get preview
            print("\n[Test 2] Getting book preview...")
            result = await client.call_tool(
                "get_book_preview",
                {"book_name": "pride_and_prejudice", "lines": 3}
            )
            print(f"Result: {result.content[0].text[:200]}...")
            
            # Test 3: Get statistics
            print("\n[Test 3] Getting book statistics...")
            result = await client.call_tool(
                "get_book_statistics",
                {"book_name": "moby_dick"}
            )
            print(f"Result: {result.content[0].text[:200]}...")
            
            # Test 4: Search
            print("\n[Test 4] Searching in book...")
            result = await client.call_tool(
                "search_in_book",
                {"book_name": "frankenstein", "search_term": "victor"}
            )
            print(f"Result: {result.content[0].text[:200]}...")
            
            print("\n✓ Book Tools Server: All tests passed!")
    
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("  Make sure the server is running:")
        print("  fastmcp run book_tools_server.py:mcp --transport http --port 8000")


async def test_code_analysis_server():
    """Test the Code Analysis Server."""
    print("\n" + "=" * 70)
    print("TESTING: Code Analysis Server")
    print("=" * 70)
    
    from fastmcp import Client
    
    try:
        async with Client("http://localhost:8001/mcp") as client:
            print("✓ Connected to HTTP server at localhost:8001")
            
            # Test with a known Python file
            test_file = Path(__file__).resolve()
            
            # Test 1: Validate syntax
            print(f"\n[Test 1] Validating syntax of {test_file.name}...")
            result = await client.call_tool(
                "validate_python_syntax",
                {"file_path": str(test_file)}
            )
            print(f"Result: {result.content[0].text[:200]}...")
            
            # Test 2: Count lines
            print(f"\n[Test 2] Counting lines in {test_file.name}...")
            result = await client.call_tool(
                "count_lines_of_code",
                {"file_path": str(test_file)}
            )
            print(f"Result: {result.content[0].text[:200]}...")
            
            # Test 3: Analyze file
            print(f"\n[Test 3] Analyzing {test_file.name}...")
            result = await client.call_tool(
                "analyze_python_file",
                {"file_path": str(test_file)}
            )
            print(f"Result: {result.content[0].text[:200]}...")
            
            print("\n✓ Code Analysis Server: All tests passed!")
    
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("  Make sure the server is running:")
        print("  fastmcp run code_analysis_server.py:mcp --transport http --port 8001")


async def test_tool_calling():
    """Test direct tool calling."""
    print("\n" + "=" * 70)
    print("TESTING: Direct Tool Calling with FastMCP CLI")
    print("=" * 70)
    
    import subprocess
    
    print("\nTesting book_tools_server.py with CLI:")
    
    try:
        # List tools
        print("\n[CLI Test 1] Listing tools...")
        result = subprocess.run(
            ["fastmcp", "client", "book_tools_server.py:mcp", "list-tools"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✓ Available tools:\n{result.stdout[:300]}...")
        else:
            print(f"✗ Error: {result.stderr}")
        
        # Call a tool
        print("\n[CLI Test 2] Calling list_available_books...")
        result = subprocess.run(
            ["fastmcp", "client", "book_tools_server.py:mcp", "call-tool", "list_available_books"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✓ Result:\n{result.stdout[:300]}...")
        else:
            print(f"✗ Error: {result.stderr}")
    
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        print("  Make sure fastmcp is installed:")
        print("  pip install fastmcp")


async def demonstrate_client_usage():
    """Demonstrate practical client usage patterns."""
    print("\n" + "=" * 70)
    print("CLIENT USAGE PATTERNS")
    print("=" * 70)
    
    print("""
Here are practical patterns for using MCP servers with clients:

1. Basic Tool Calling:
   ```python
   import asyncio
   from fastmcp import Client
   
   async def main():
       async with Client("http://localhost:8000/mcp") as client:
           result = await client.call_tool("tool_name", {"param": "value"})
           print(result)
   
   asyncio.run(main())
   ```

2. Error Handling:
   ```python
   async with Client("http://localhost:8000/mcp") as client:
       result = await client.call_tool("tool_name", {"param": "value"})
       content = json.loads(result.content[0].text)
       
       if "error" in content:
           print(f"Error: {content['error']}")
       else:
           print(f"Success: {content}")
   ```

3. Multiple Calls:
   ```python
   async with Client("http://localhost:8000/mcp") as client:
       # Multiple calls in same context
       result1 = await client.call_tool("tool1", {})
       result2 = await client.call_tool("tool2", {})
       result3 = await client.call_tool("tool3", {})
   ```

4. With Claude Desktop:
   Add to claude_desktop_config.json:
   ```json
   {
     "mcpServers": {
       "my-books": {
         "command": "python",
         "args": ["/path/to/book_tools_server.py"]
       }
     }
   }
   ```
   Then Claude will have access to all tools automatically.

5. Integration with FastMCP Client:
   ```python
   from fastmcp import Client
   
   async with Client("stdio", ["python", "book_tools_server.py"]) as client:
       # Use stdio transport for local connections
       result = await client.call_tool("list_available_books", {})
   ```
    """)


async def demo_server_setup():
    """Show how to set up servers."""
    print("\n" + "=" * 70)
    print("SERVER SETUP INSTRUCTIONS")
    print("=" * 70)
    
    print("""
Setup Steps:

1. Install FastMCP:
   pip install fastmcp

2. Terminal 1 - Run Book Tools Server (HTTP):
   fastmcp run book_tools_server.py:mcp --transport http --port 8000

3. Terminal 2 - Run Code Analysis Server (HTTP):
   fastmcp run code_analysis_server.py:mcp --transport http --port 8001

4. Terminal 3 - Test with Client:
   python client_example.py
   
   OR use CLI:
   fastmcp client book_tools_server.py:mcp list-tools
   fastmcp client book_tools_server.py:mcp call-tool list_available_books

5. Integrate with Claude Desktop:
   - Find config file location (see README.md)
   - Add server configuration
   - Restart Claude Desktop
   - Claude can now use book tools!

Available Tools:

Book Tools Server:
  - list_available_books: List all books
  - get_book_content: Get book content
  - search_in_book: Search for text
  - get_book_statistics: Get book stats
  - get_book_preview: Get preview
  - compare_books: Compare two books

Code Analysis Server:
  - analyze_python_file: Analyze file structure
  - count_lines_of_code: Count lines
  - find_unused_imports: Find unused imports
  - get_function_complexity: Estimate complexity
  - validate_python_syntax: Check syntax
    """)


async def main():
    """Run all tests and demonstrations."""
    print("\n╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "FastMCP 2.0 Server Testing & Demonstration".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Show setup instructions
    await demo_server_setup()
    
    # Show client usage patterns
    await demonstrate_client_usage()
    
    # Run tests (if servers are available)
    print("\n" + "=" * 70)
    print("RUNNING TESTS (Ensure servers are running!)")
    print("=" * 70)
    
    try:
        await test_book_tools_server()
    except Exception as e:
        print(f"Skipping book tools test: {e}")
    
    try:
        await test_code_analysis_server()
    except Exception as e:
        print(f"Skipping code analysis test: {e}")
    
    try:
        await test_tool_calling()
    except Exception as e:
        print(f"Skipping CLI test: {e}")
    
    print("\n" + "=" * 70)
    print("Testing completed!")
    print("=" * 70)
    print("""
Next steps:
1. Read README.md for detailed documentation
2. Read DEVELOPMENT.md for server development patterns
3. Read QUICKSTART.md for quick getting started
4. Create your own MCP servers using these examples
5. Integrate with Claude Desktop for easy access
    """)


if __name__ == "__main__":
    asyncio.run(main())
