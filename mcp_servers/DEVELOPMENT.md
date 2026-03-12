# FastMCP 2.0 Server Development Guide

This guide explains how to build, run, and extend MCP servers using FastMCP 2.0.

## Overview

FastMCP is a Python framework for building Model Context Protocol (MCP) servers. It abstracts away the complexity of the MCP protocol and provides a simple, Pythonic interface.

### Key Benefits

- **Simple Syntax**: Decorate functions with `@mcp.tool` to create tools
- **Type Safety**: Type hints are used to generate MCP schemas automatically
- **Multiple Transports**: Supports stdio (local) and HTTP (remote) transports
- **Automatic Documentation**: Docstrings become tool descriptions
- **Production Ready**: Includes error handling, logging, and deployment options

## Project Structure

```
mcp_servers/
├── book_tools_server.py           # Example: Book analysis tools
├── code_analysis_server.py        # Example: Python code analysis
├── client_example.py              # Example: How to use a server
├── requirements.txt               # Python dependencies
├── fastmcp.json                   # Server configuration
├── README.md                       # Full documentation
├── QUICKSTART.md                  # Quick start guide
└── DEVELOPMENT.md                 # This file
```

## Building Your First Server

### Step 1: Basic Structure

```python
from fastmcp import FastMCP

# Create server instance
mcp = FastMCP("My Server Name", version="1.0.0")

# Add tools
@mcp.tool
def my_tool(param: str) -> dict:
    """Description of what this tool does."""
    return {"result": "value"}

# Run server
if __name__ == "__main__":
    mcp.run()
```

### Step 2: Add Multiple Tools

```python
@mcp.tool
def tool_one(input: str) -> str:
    """First tool."""
    return f"Processed: {input}"

@mcp.tool
def tool_two(x: int, y: int) -> int:
    """Second tool."""
    return x + y

@mcp.tool
def tool_three(name: str, age: int) -> dict:
    """Third tool with dictionary return."""
    return {
        "name": name,
        "age": age,
        "next_year": age + 1
    }
```

### Step 3: Run and Test

```bash
# Run with stdio (default)
python my_server.py

# Run with HTTP
fastmcp run my_server.py:mcp --transport http --port 8000

# Test with CLI
fastmcp client my_server.py:mcp list-tools
fastmcp client my_server.py:mcp call-tool my_tool --input '{"param": "test"}'
```

## Tool Development Patterns

### Pattern 1: Simple Tools

```python
@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

### Pattern 2: Tools with Error Handling

```python
@mcp.tool
def divide(a: float, b: float) -> dict:
    """Divide two numbers."""
    if b == 0:
        return {"error": "Division by zero"}
    return {"result": a / b}
```

### Pattern 3: Tools with Complex Return Types

```python
@mcp.tool
def analyze(data: str) -> dict:
    """Analyze some data."""
    return {
        "input": data,
        "length": len(data),
        "uppercase": data.upper(),
        "lowercase": data.lower(),
        "reversed": data[::-1]
    }
```

### Pattern 4: Tools with Optional Parameters

```python
@mcp.tool
def search(query: str, max_results: int = 10) -> dict:
    """Search for something."""
    # Implementation
    return {
        "query": query,
        "max_results": max_results,
        "results": []
    }
```

### Pattern 5: Tools with List Returns

```python
@mcp.tool
def list_items() -> dict:
    """List available items."""
    items = ["item1", "item2", "item3"]
    return {
        "items": items,
        "count": len(items)
    }
```

## Type Hints and Schemas

Type hints are crucial - they're used to generate MCP schemas:

```python
# Good: Clear types
@mcp.tool
def process(text: str, count: int) -> dict:
    """Process text."""
    pass

# Less clear: Generic types
@mcp.tool
def process(text) -> dict:  # Missing type hint
    pass
```

### Supported Types

- **Basic**: `str`, `int`, `float`, `bool`
- **Collections**: `list`, `dict`, `tuple`, `set`
- **Optional**: `Optional[str]` for optional parameters
- **Union**: `Union[str, int]` for multiple types
- **Literals**: `Literal["option1", "option2"]` for choices

```python
@mcp.tool
def flexible_tool(
    text: str,
    count: int = 1,
    format: Literal["json", "csv", "text"] = "json"
) -> dict:
    """Flexible tool with various parameter types."""
    return {"result": "value"}
```

## Error Handling

Always return error information in responses:

```python
@mcp.tool
def safe_operation(file_path: str) -> dict:
    """Perform operation safely."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {"success": True, "content": content}
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

## Transports

### Stdio Transport (Default)

Best for local clients (Claude Desktop, Cursor, etc.):

```bash
python my_server.py
fastmcp run my_server.py:mcp
```

```python
if __name__ == "__main__":
    mcp.run()  # Defaults to stdio
```

### HTTP Transport

Best for remote access and testing:

```bash
fastmcp run my_server.py:mcp --transport http --port 8000
```

```python
if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

Connect with:

```python
from fastmcp import Client

async with Client("http://localhost:8000/mcp") as client:
    result = await client.call_tool("my_tool", {"param": "value"})
```

## Testing Tools

### Using FastMCP CLI

```bash
# List tools
fastmcp client my_server.py:mcp list-tools

# Call a tool
fastmcp client my_server.py:mcp call-tool my_tool --input '{"param": "value"}'

# Get tool documentation
fastmcp client my_server.py:mcp inspect my_tool
```

### Using Python Client

```python
import asyncio
from fastmcp import Client

async def test():
    async with Client("http://localhost:8000/mcp") as client:
        result = await client.call_tool("my_tool", {"param": "value"})
        print(result)

asyncio.run(test())
```

### Using curl (HTTP only)

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "my_tool", "arguments": {"param": "value"}}}'
```

## Integration with Claude Desktop

1. Get your server's absolute path:

```bash
pwd  # Get current directory
# Then append /my_server.py
```

2. Edit Claude Desktop config:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

3. Add your server:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/absolute/path/to/my_server.py"]
    }
  }
}
```

4. Restart Claude Desktop

5. Claude will now have access to all your tools!

## Deployment

### Local Development

```bash
python my_server.py
```

### Production with Prefect Horizon

[Prefect Horizon](https://horizon.prefect.io) is the MCP platform by the FastMCP team:

1. Push code to GitHub
2. Sign in with GitHub account
3. Create project from repo, set entrypoint to `my_server.py:mcp`
4. Server deployed at `https://your-project.fastmcp.app/mcp`

### Self-Hosted HTTP Server

```bash
fastmcp run my_server.py:mcp --transport http --port 8000
```

Then use in clients:

```python
async with Client("http://your-server.com:8000/mcp") as client:
    # Use tools
```

## Best Practices

### 1. Documentation

```python
@mcp.tool
def my_tool(param: str) -> dict:
    """Clear description of what this tool does.
    
    Include usage examples or important details here.
    """
    pass
```

### 2. Input Validation

```python
@mcp.tool
def validate_example(email: str) -> dict:
    """Validate an email address."""
    if '@' not in email:
        return {"error": "Invalid email format"}
    return {"valid": True, "email": email}
```

### 3. Consistent Response Format

```python
# Good: Consistent structure
@mcp.tool
def consistent(param: str) -> dict:
    """Example tool with consistent responses."""
    if error_condition:
        return {"error": "Description", "param": param}
    return {"success": True, "result": "value", "param": param}
```

### 4. Limit Large Results

```python
@mcp.tool
def search(query: str, max_results: int = 20) -> dict:
    """Search with result limiting."""
    all_results = do_search(query)
    # Limit to prevent overwhelming responses
    limited = all_results[:max_results]
    return {
        "query": query,
        "total": len(all_results),
        "returned": len(limited),
        "results": limited,
        "truncated": len(all_results) > max_results
    }
```

### 5. Performance Considerations

```python
# Bad: Slow
@mcp.tool
def slow_tool(data: str) -> dict:
    # Processes everything
    result = process_all(data)
    return {"result": result}

# Better: Configurable
@mcp.tool
def fast_tool(data: str, limit: int = 100) -> dict:
    # Processes only what's needed
    result = process_limited(data, limit)
    return {"result": result, "truncated": len(data) > limit}
```

## Debugging

### Enable Logging

```bash
FASTMCP_LOG_LEVEL=DEBUG python my_server.py
```

### Common Issues

1. **"Module not found"**: Install dependencies with `pip install -r requirements.txt`
2. **"Connection refused"**: Server not running or wrong port
3. **"Tool not found"**: Tool name must match function name exactly
4. **"Invalid arguments"**: Check parameter types and names

## Examples Included

1. **book_tools_server.py**: File/text analysis tools
   - Lists books
   - Searches for terms
   - Compares files
   - Generates statistics

2. **code_analysis_server.py**: Python code analysis
   - Analyzes code structure
   - Counts lines of code
   - Finds unused imports
   - Estimates complexity

Both demonstrate real-world patterns you can use in your own servers.

## Next Steps

1. Create a new server file
2. Add tools using `@mcp.tool` decorator
3. Test locally with FastMCP CLI
4. Integrate with Claude Desktop
5. Deploy with Prefect Horizon

## Resources

- **Documentation**: https://gofastmcp.com/llms.txt
- **Quickstart**: https://gofastmcp.com/getting-started/quickstart.md
- **Installation**: https://gofastmcp.com/getting-started/installation.md
- **API Reference**: https://gofastmcp.com/python-sdk/fastmcp-cli-__init__.md
