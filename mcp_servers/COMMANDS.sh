#!/bin/bash
# FastMCP 2.0 MCP Servers - Quick Command Reference
# Run this file or copy commands as needed

# ============================================
# INSTALLATION
# ============================================

# Install FastMCP
pip install fastmcp

# Verify installation
fastmcp version

# Install from requirements.txt
pip install -r requirements.txt

# ============================================
# RUNNING SERVERS
# ============================================

# Option 1: Run with Python (stdio transport - default)
python book_tools_server.py

# Option 2: Run with FastMCP CLI (stdio transport)
fastmcp run book_tools_server.py:mcp

# Option 3: Run with HTTP transport (port 8000)
fastmcp run book_tools_server.py:mcp --transport http --port 8000

# ============================================
# TESTING AND LISTING TOOLS
# ============================================

# List all available tools
fastmcp client book_tools_server.py:mcp list-tools

# Get detailed help for a tool
fastmcp client book_tools_server.py:mcp call-tool list_available_books

# ============================================
# CALLING TOOLS VIA CLI
# ============================================

# Call: list_available_books (no parameters)
fastmcp client book_tools_server.py:mcp call-tool list_available_books

# Call: get_book_preview with parameters
fastmcp client book_tools_server.py:mcp call-tool get_book_preview \
  --input '{"book_name": "moby_dick", "lines": 20}'

# Call: search_in_book
fastmcp client book_tools_server.py:mcp call-tool search_in_book \
  --input '{"book_name": "pride_and_prejudice", "search_term": "love"}'

# Call: get_book_statistics
fastmcp client book_tools_server.py:mcp call-tool get_book_statistics \
  --input '{"book_name": "frankenstein"}'

# Call: compare_books
fastmcp client book_tools_server.py:mcp call-tool compare_books \
  --input '{"book1": "pride_and_prejudice", "book2": "moby_dick"}'

# ============================================
# CODE ANALYSIS SERVER
# ============================================

# List tools in code analysis server
fastmcp client code_analysis_server.py:mcp list-tools

# Validate Python syntax
fastmcp client code_analysis_server.py:mcp call-tool validate_python_syntax \
  --input '{"file_path": "book_tools_server.py"}'

# Count lines of code
fastmcp client code_analysis_server.py:mcp call-tool count_lines_of_code \
  --input '{"file_path": "book_tools_server.py"}'

# Analyze file structure
fastmcp client code_analysis_server.py:mcp call-tool analyze_python_file \
  --input '{"file_path": "book_tools_server.py"}'

# ============================================
# TESTING
# ============================================

# Run test suite
python test_servers.py

# Run example client (requires server running on port 8000)
python client_example.py

# ============================================
# CURL TESTING (HTTP only)
# ============================================

# Health check
curl http://localhost:8000/mcp

# Call tool via curl (requires proper JSON):
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "list_available_books", "arguments": {}}}'

# ============================================
# MULTIPLE TERMINAL SETUP
# ============================================

# Terminal 1: Run book tools server (HTTP)
fastmcp run book_tools_server.py:mcp --transport http --port 8000

# Terminal 2: Run code analysis server (HTTP)
fastmcp run code_analysis_server.py:mcp --transport http --port 8001

# Terminal 3: Test with CLI
fastmcp client book_tools_server.py:mcp list-tools

# Terminal 4: Run client example
python client_example.py

# ============================================
# INTEGRATION WITH CLAUDE DESKTOP
# ============================================

# Find your config file:
# macOS: ~/Library/Application\ Support/Claude/claude_desktop_config.json
# Windows: %APPDATA%\Claude\claude_desktop_config.json
# Linux: ~/.config/Claude/claude_desktop_config.json

# Add this to your claude_desktop_config.json:
# {
#   "mcpServers": {
#     "book-tools": {
#       "command": "python",
#       "args": ["/absolute/path/to/book_tools_server.py"]
#     }
#   }
# }

# Then restart Claude Desktop and it will have access to all tools!

# ============================================
# HELPFUL INFORMATION COMMANDS
# ============================================

# Show FastMCP version
fastmcp version

# Show help
fastmcp --help
fastmcp run --help
fastmcp client --help

# Show current directory
pwd

# List files in current directory
ls -la

# Show Python version
python --version

# ============================================
# DEVELOPMENT COMMANDS
# ============================================

# Create a new server from template
cat > my_server.py << 'EOF'
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
EOF

# Test the new server
python my_server.py

# ============================================
# DOCUMENTATION COMMANDS
# ============================================

# View locally
cat README.md
cat QUICKSTART.md
cat DEVELOPMENT.md
cat INDEX.md

# Visit official documentation
# https://gofastmcp.com/llms.txt
# https://gofastmcp.com/getting-started/quickstart.md
# https://gofastmcp.com/getting-started/welcome.md

# ============================================
# TROUBLESHOOTING
# ============================================

# Check if FastMCP is installed
pip show fastmcp

# Check if Python file has valid syntax
python -m py_compile book_tools_server.py

# Test import
python -c "from fastmcp import FastMCP; print('FastMCP imported successfully')"

# Check if port is in use (Unix/Mac)
lsof -i :8000

# Kill process on port 8000 (Unix/Mac)
kill -9 $(lsof -t -i :8000)

# ============================================
# QUICK REFERENCE SUMMARY
# ============================================
# 
# 1. Install: pip install fastmcp
# 2. Run: python book_tools_server.py
# 3. Test: fastmcp client book_tools_server.py:mcp list-tools
# 4. Call: fastmcp client book_tools_server.py:mcp call-tool list_available_books
# 5. Integrate: Add to claude_desktop_config.json and restart
#
# For more: cat README.md
# Full docs: https://gofastmcp.com/llms.txt
