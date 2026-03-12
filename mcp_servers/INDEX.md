# FastMCP 2.0 MCP Servers - Complete Project

This directory contains a complete MCP (Model Context Protocol) server project built with FastMCP 2.0. All documentation references follow the official FastMCP documentation at https://gofastmcp.com/llms.txt.

## 📁 Project Structure

```
mcp_servers/
├── book_tools_server.py          # Primary: Book analysis MCP server
├── code_analysis_server.py       # Secondary: Python code analysis server
├── client_example.py             # Example: How to use the servers
├── test_servers.py               # Testing suite and demonstrations
├── fastmcp.json                  # Server configuration (FastMCP CLI)
├── requirements.txt              # Python dependencies
├── README.md                      # Complete documentation (START HERE!)
├── QUICKSTART.md                 # 5-minute quick start guide
├── DEVELOPMENT.md                # Server development patterns & best practices
├── INDEX.md                       # This file
```

## 🚀 Quick Navigation

### For First-Time Users
1. **[QUICKSTART.md](QUICKSTART.md)** — Get a server running in 5 minutes
2. **[README.md](README.md)** — Full documentation of tools and features

### For Developers
1. **[DEVELOPMENT.md](DEVELOPMENT.md)** — Patterns, best practices, and advanced topics
2. **[book_tools_server.py](book_tools_server.py)** — Study this example server
3. **[code_analysis_server.py](code_analysis_server.py)** — More advanced patterns

### For Testing
1. **[test_servers.py](test_servers.py)** — Run tests and see examples
2. **[client_example.py](client_example.py)** — Basic client usage example

## 📚 What's Inside

### Servers Included

#### 1. **Book Tools Server** (`book_tools_server.py`)
Demonstrates practical tools for working with text files:
- List available books
- Get book content and previews
- Search for terms in books
- Get book statistics
- Compare multiple books

**Use this to learn:**
- File I/O in tools
- Search and filtering logic
- Statistics calculation
- Error handling

#### 2. **Code Analysis Server** (`code_analysis_server.py`)
Demonstrates advanced code analysis capabilities:
- Analyze Python file structure
- Count lines of code
- Find unused imports
- Estimate function complexity
- Validate Python syntax

**Use this to learn:**
- AST (Abstract Syntax Tree) handling
- Complex return types
- Optional parameters
- Advanced error handling

### Example Client (`client_example.py`)
Shows how to:
- Connect to an HTTP server
- Call tools with arguments
- Handle responses
- Use async/await patterns

## 🎯 What You'll Learn

### FastMCP Fundamentals
- Creating servers with `FastMCP` class
- Registering tools with `@mcp.tool` decorator
- Type hints for automatic schema generation
- Multiple transport types (stdio, HTTP)

### Server Development
- Error handling patterns
- Optional parameters and defaults
- Complex return types
- Input validation
- Performance optimization

### Integration
- Claude Desktop integration
- HTTP server deployment
- CLI usage
- Client connections

## 📖 Official Documentation

All information follows the FastMCP 2.0 official documentation:

- **[Documentation Index](https://gofastmcp.com/llms.txt)** — Complete reference
- **[Welcome Guide](https://gofastmcp.com/getting-started/welcome.md)** — Overview
- **[Quickstart](https://gofastmcp.com/getting-started/quickstart.md)** — Official tutorial
- **[Installation](https://gofastmcp.com/getting-started/installation.md)** — Setup guide

## 🛠️ Installation

```bash
# Install FastMCP
pip install fastmcp

# Or with uv
uv add fastmcp

# Install from requirements.txt
pip install -r requirements.txt
```

Verify installation:
```bash
fastmcp version
```

## 🚀 Running Servers

### Using Python Directly
```bash
python book_tools_server.py
```

### Using FastMCP CLI
```bash
# Stdio transport (default)
fastmcp run book_tools_server.py:mcp

# HTTP transport
fastmcp run book_tools_server.py:mcp --transport http --port 8000
```

## 📊 Basic Usage Example

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/mcp") as client:
        result = await client.call_tool(
            "list_available_books",
            {}
        )
        print(result)

asyncio.run(main())
```

## 🔧 Development Workflow

1. **Create Server** — Write a Python file with `@mcp.tool` functions
2. **Test Locally** — Run with `python my_server.py` or FastMCP CLI
3. **Test Tools** — Use `fastmcp client my_server.py:mcp list-tools`
4. **Integrate** — Add to Claude Desktop config
5. **Deploy** — Use Prefect Horizon or self-host

## 📋 File Descriptions

| File | Purpose |
|------|---------|
| `book_tools_server.py` | Working example of book/text tools |
| `code_analysis_server.py` | Advanced example with code analysis |
| `client_example.py` | Shows how to use servers as a client |
| `test_servers.py` | Testing suite and demonstrations |
| `fastmcp.json` | Configuration for FastMCP CLI |
| `requirements.txt` | Python dependencies |
| `README.md` | Complete tool and API documentation |
| `QUICKSTART.md` | 5-minute getting started guide |
| `DEVELOPMENT.md` | Development patterns and best practices |
| `INDEX.md` | This file |

## 🎓 Learning Path

### Beginner
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `book_tools_server.py`
3. Try the CLI commands
4. Test with [client_example.py](client_example.py)

### Intermediate
1. Study [book_tools_server.py](book_tools_server.py) code
2. Create your own simple server
3. Integrate with Claude Desktop
4. Test with FastMCP CLI

### Advanced
1. Read [DEVELOPMENT.md](DEVELOPMENT.md)
2. Study [code_analysis_server.py](code_analysis_server.py)
3. Create complex multi-feature servers
4. Deploy to Prefect Horizon

## ✨ Key Features of This Project

✅ **Two Complete Example Servers** — Learn from working implementations
✅ **Comprehensive Documentation** — QUICKSTART, README, and DEVELOPMENT guides
✅ **Testing Tools** — Built-in test suite and examples
✅ **Best Practices** — Error handling, type hints, documentation patterns
✅ **Multiple Patterns** — Simple tools, complex returns, error handling
✅ **Ready to Integrate** — Works with Claude Desktop, Cursor, Gemini
✅ **Following Official Docs** — All patterns from https://gofastmcp.com

## 🤝 Integration Points

### Claude Desktop
Add to `claude_desktop_config.json`:
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

### HTTP Endpoint
```python
mcp.run(transport="http", port=8000)
```

### FastMCP CLI
```bash
fastmcp run book_tools_server.py:mcp
```

## 📝 Quick Command Reference

```bash
# Installation
pip install fastmcp

# Running servers
python book_tools_server.py                    # Stdio
fastmcp run book_tools_server.py:mcp          # Stdio (CLI)
fastmcp run book_tools_server.py:mcp --transport http --port 8000  # HTTP

# Testing
fastmcp client book_tools_server.py:mcp list-tools
fastmcp client book_tools_server.py:mcp call-tool list_available_books
python test_servers.py

# Creating new server
# 1. Copy this template to new_server.py:
#    from fastmcp import FastMCP
#    mcp = FastMCP("My Server")
#    @mcp.tool
#    def my_tool(param: str) -> str:
#        return f"Hello {param}"
#    if __name__ == "__main__":
#        mcp.run()
# 2. Run: python new_server.py
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Module not found` | Run `pip install fastmcp` |
| `Connection refused` | Make sure server is running |
| `Tool not found` | Check tool name matches function name |
| `Invalid type hints` | Ensure all parameters have type hints |

## 📚 Additional Resources

- **[Official Docs](https://gofastmcp.com/getting-started/welcome.md)** — Complete API reference
- **[Prefect Horizon](https://horizon.prefect.io)** — Deploy FastMCP servers
- **[MCP Protocol](https://modelcontextprotocol.io/)** — Understanding MCP
- **[FastMCP GitHub](https://github.com/PrefectHQ/fastmcp)** — Source code and issues

## 🎯 Next Steps

1. **Run QUICKSTART.md** to get a server running
2. **Study book_tools_server.py** to understand patterns
3. **Create your own server** based on these examples
4. **Integrate with Claude Desktop** for easy access
5. **Explore DEVELOPMENT.md** for advanced patterns

## 📞 Support

- Check [README.md](README.md) for detailed documentation
- Review [DEVELOPMENT.md](DEVELOPMENT.md) for patterns and best practices
- See [QUICKSTART.md](QUICKSTART.md) for quick answers
- Refer to [Official Docs](https://gofastmcp.com/llms.txt) for complete reference

---

**Built with FastMCP 2.0** — The fast, Pythonic way to build MCP servers
**Documentation**: https://gofastmcp.com/llms.txt
