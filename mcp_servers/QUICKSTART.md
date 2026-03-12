# Quick Start Guide - Book Tools MCP Server

This guide will help you get the server up and running in minutes.

## Step 1: Install FastMCP

```bash
pip install fastmcp
```

Verify installation:

```bash
fastmcp version
```

## Step 2: Run the Server

### Option A: Using Python directly

```bash
cd /workspaces/langchain-crash-course/mcp_servers
python book_tools_server.py
```

The server will start with stdio transport, waiting for client connections.

### Option B: Using FastMCP CLI

```bash
cd /workspaces/langchain-crash-course/mcp_servers
fastmcp run book_tools_server.py:mcp
```

### Option C: Using HTTP transport (for testing with curl/browser)

```bash
cd /workspaces/langchain-crash-course/mcp_servers
fastmcp run book_tools_server.py:mcp --transport http --port 8000
```

Then test with:

```bash
curl http://localhost:8000/mcp
```

## Step 3: Test with Python Client

Open a new terminal and run:

```bash
cd /workspaces/langchain-crash-course/mcp_servers
python client_example.py
```

## Step 4: Use with FastMCP CLI Client

List all tools:

```bash
fastmcp client book_tools_server.py:mcp list-tools
```

Call a tool:

```bash
fastmcp client book_tools_server.py:mcp call-tool list_available_books
```

Search in a book:

```bash
fastmcp client book_tools_server.py:mcp call-tool search_in_book \
  --input '{"book_name": "moby_dick", "search_term": "whale"}'
```

## Step 5: Integrate with Claude Desktop

1. Find your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add this server configuration:

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

3. Restart Claude Desktop

4. Chat with Claude - it will now have access to all book tools!

## Common Commands

```bash
# List available books
fastmcp client book_tools_server.py:mcp call-tool list_available_books

# Get preview of a book
fastmcp client book_tools_server.py:mcp call-tool get_book_preview \
  --input '{"book_name": "pride_and_prejudice", "lines": 20}'

# Get book statistics
fastmcp client book_tools_server.py:mcp call-tool get_book_statistics \
  --input '{"book_name": "moby_dick"}'

# Search for a term
fastmcp client book_tools_server.py:mcp call-tool search_in_book \
  --input '{"book_name": "frankenstein", "search_term": "monster"}'

# Compare books
fastmcp client book_tools_server.py:mcp call-tool compare_books \
  --input '{"book1": "pride_and_prejudice", "book2": "moby_dick"}'
```

## Troubleshooting

### Connection refused

If you get "Connection refused", make sure the server is running in another terminal.

### Python not found

Make sure you're in the correct directory and Python is installed:

```bash
python --version
```

### Book not found error

Available books are in `../4_rag/books/`. Use the exact filename (without .txt):
- `pride_and_prejudice`
- `moby_dick`
- `frankenstein`
- `odyssey`
- etc.

### FastMCP not installed

```bash
pip install fastmcp
```

## Next Steps

- Read the full [README.md](README.md) for detailed tool documentation
- Check the [FastMCP Quickstart](https://gofastmcp.com/getting-started/quickstart.md)
- Explore extending the server with your own tools
- Deploy to Prefect Horizon for cloud hosting
