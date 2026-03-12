# Book Tools MCP Server

A FastMCP 2.0 server that provides tools for working with books. This is a practical example of building MCP servers using the FastMCP framework.

## Overview

This server demonstrates the key concepts of FastMCP 2.0:

- **Tool Definition**: Functions decorated with `@mcp.tool` are automatically registered as MCP tools
- **Type Hints**: Return types are used to generate MCP schemas automatically
- **Multiple Transports**: Supports both stdio (local) and HTTP (remote) transports
- **Error Handling**: Graceful error handling with informative responses

## Available Tools

### 1. `list_available_books`
Lists all available books in the library with their file sizes.

**Returns:**
- `books`: List of books with name, filename, and size
- `count`: Total number of books available

### 2. `get_book_content`
Retrieves the content of a specific book, limited to a maximum number of lines.

**Parameters:**
- `book_name` (str): Name of the book (without .txt extension)
- `max_lines` (int, default=50): Maximum number of lines to return

**Returns:**
- `book`: Book name
- `lines_returned`: Number of lines returned
- `total_lines`: Total lines in the book
- `content`: The book content

### 3. `search_in_book`
Searches for a term in a book and returns matching lines (case-insensitive).

**Parameters:**
- `book_name` (str): Name of the book
- `search_term` (str): Term to search for

**Returns:**
- `book`: Book name
- `search_term`: The search term used
- `matches_found`: Total matches found
- `matches`: List of matching lines (limited to 20)
- `truncated`: Whether results were truncated

### 4. `get_book_statistics`
Gets statistics about a book including word count and character count.

**Parameters:**
- `book_name` (str): Name of the book

**Returns:**
- `total_lines`: Number of lines
- `total_words`: Total word count
- `total_characters`: Total character count
- `average_word_length`: Average length of words
- `size_mb`: Size in megabytes

### 5. `get_book_preview`
Gets a quick preview of the first N lines of a book.

**Parameters:**
- `book_name` (str): Name of the book
- `lines` (int, default=10): Number of lines to preview

**Returns:**
- `book`: Book name
- `preview_lines`: Number of lines in preview
- `content`: Preview content

### 6. `compare_books`
Compares statistics between two books.

**Parameters:**
- `book1` (str): First book name
- `book2` (str): Second book name

**Returns:**
- `book1`, `book2`: Book names
- `stats`: Statistics for both books
- `differences`: Calculated differences

## Installation

First, install FastMCP:

```bash
pip install fastmcp
```

Or with uv:

```bash
uv add fastmcp
```

## Running the Server

### Option 1: Using Python directly (stdio transport)

```bash
python book_tools_server.py
```

This starts the server using the default stdio transport, suitable for local MCP clients.

### Option 2: Using FastMCP CLI (stdio transport)

```bash
fastmcp run book_tools_server.py:mcp
```

### Option 3: Using HTTP transport (for remote access)

**Start the server:**

```bash
python -c "from book_tools_server import mcp; mcp.run(transport='http', port=8000)"
```

Or use the FastMCP CLI:

```bash
fastmcp run book_tools_server.py:mcp --transport http --port 8000
```

## Using the Client

### Option 1: HTTP Client Example

First, start the server with HTTP transport (see above). Then run:

```bash
python client_example.py
```

The client example demonstrates:
- Connecting to the server
- Calling various tools
- Processing and displaying results

### Option 2: Programmatic Usage

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/mcp") as client:
        result = await client.call_tool("list_available_books", {})
        print(result)

asyncio.run(main())
```

### Option 3: Stdio Usage

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("stdio", ["python", "book_tools_server.py"]) as client:
        result = await client.call_tool("list_available_books", {})
        print(result)

asyncio.run(main())
```

## Integration with Claude and Other LLMs

### Claude Desktop

To use this server with Claude Desktop, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "book-tools": {
      "command": "python",
      "args": ["/path/to/book_tools_server.py"]
    }
  }
}
```

### HTTP Integration

To use with Claude via HTTP endpoint:

```json
{
  "mcpServers": {
    "book-tools": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## Key FastMCP 2.0 Concepts

### 1. Server Initialization

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server Name", version="1.0.0")
```

### 2. Tool Decoration

```python
@mcp.tool
def my_tool(param: str) -> dict:
    """Description of the tool."""
    return {"result": "value"}
```

- The `@mcp.tool` decorator automatically registers the function
- Type hints generate the JSON schema
- The docstring becomes the tool description

### 3. Error Handling

Return informative error messages in the response dict:

```python
return {"error": "Description of what went wrong"}
```

### 4. Running the Server

```python
if __name__ == "__main__":
    mcp.run()  # stdio transport (default)
    # OR
    mcp.run(transport="http", port=8000)  # HTTP transport
```

## FastMCP Documentation

For more information about FastMCP, refer to:
- **Quickstart**: https://gofastmcp.com/getting-started/quickstart.md
- **Installation**: https://gofastmcp.com/getting-started/installation.md
- **Welcome Guide**: https://gofastmcp.com/getting-started/welcome.md
- **Documentation Index**: https://gofastmcp.com/llms.txt

## Architecture

```
book_tools_server.py          # Main server with tool implementations
client_example.py             # Example client demonstrating usage
README.md                      # This file
```

## Best Practices Used

1. **Type Hints**: All functions have complete type hints for automatic schema generation
2. **Error Handling**: All tools include try-catch blocks and return error responses
3. **Documentation**: Each tool has a docstring explaining its purpose
4. **Modularity**: Tools are independent and can be used separately
5. **Resource-Aware**: Default limits on results (e.g., max 20 search results)

## Extending the Server

To add new tools, simply create a function and decorate it with `@mcp.tool`:

```python
@mcp.tool
def new_tool(param1: str, param2: int) -> dict:
    """Description of the tool."""
    # Implementation
    return {"result": "value"}
```

## Troubleshooting

### "Books directory not found"
Ensure the `4_rag/books` directory exists relative to the server location.

### Connection refused (HTTP)
Make sure the server is running on the specified port:
```bash
fastmcp run book_tools_server.py:mcp --transport http --port 8000
```

### Import errors
Make sure FastMCP is installed:
```bash
pip install fastmcp
```

## License

This example server is provided as part of the langchain-crash-course project.
