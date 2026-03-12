"""
Advanced FastMCP 2.0 Server - Code Analysis Tools

This server demonstrates more advanced FastMCP features:
- Tools with complex return types
- Error handling patterns
- Tool composition
- Python code analysis capabilities
"""

import ast
import os
import json
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Code Analysis Server", version="1.0.0")


@mcp.tool
def analyze_python_file(file_path: str) -> dict:
    """Analyze a Python file and extract its structure."""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        if not path.suffix == ".py":
            return {"error": "File must be a Python file (.py)"}
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST
        tree = ast.parse(content)
        
        analysis = {
            "file": str(file_path),
            "total_lines": len(content.split('\n')),
            "total_characters": len(content),
            "classes": [],
            "functions": [],
            "imports": [],
            "docstrings": {
                "module": ast.get_docstring(tree),
                "classes": {},
                "functions": {}
            }
        }
        
        # Extract classes, functions, and imports
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                
                analysis["classes"].append({
                    "name": node.name,
                    "methods": methods,
                    "docstring": ast.get_docstring(node),
                    "line": node.lineno
                })
                analysis["docstrings"]["classes"][node.name] = ast.get_docstring(node)
            
            elif isinstance(node, ast.FunctionDef):
                # Only capture top-level functions
                if node.col_offset == 0:
                    analysis["functions"].append({
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node),
                        "line": node.lineno
                    })
                    analysis["docstrings"]["functions"][node.name] = ast.get_docstring(node)
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis["imports"].append({
                        "type": "import",
                        "module": alias.name
                    })
            
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    analysis["imports"].append({
                        "type": "from",
                        "module": node.module,
                        "name": alias.name
                    })
        
        return analysis
    
    except SyntaxError as e:
        return {"error": f"Syntax error in file: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to analyze file: {str(e)}"}


@mcp.tool
def count_lines_of_code(file_path: str) -> dict:
    """Count lines of code, comments, and blank lines in a Python file."""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#'):
                comment_lines += 1
            else:
                code_lines += 1
        
        return {
            "file": str(file_path),
            "total_lines": len(lines),
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines,
            "code_percentage": round(code_lines / len(lines) * 100, 2) if lines else 0
        }
    except Exception as e:
        return {"error": f"Failed to count lines: {str(e)}"}


@mcp.tool
def find_unused_imports(file_path: str) -> dict:
    """Find potentially unused imports in a Python file."""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        # Collect all imports
        imports = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name.split('.')[0]
                    imports[name] = {"type": "import", "line": node.lineno}
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = {"type": "from", "module": node.module, "line": node.lineno}
        
        # Find usages
        used = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used.add(node.id)
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    used.add(node.value.id)
        
        # Find unused
        unused = {}
        for name, info in imports.items():
            if name not in used and not name.startswith('_'):
                unused[name] = info
        
        return {
            "file": str(file_path),
            "total_imports": len(imports),
            "unused_imports": len(unused),
            "unused": unused if unused else {}
        }
    except Exception as e:
        return {"error": f"Failed to find unused imports: {str(e)}"}


@mcp.tool
def get_function_complexity(file_path: str, function_name: Optional[str] = None) -> dict:
    """Estimate cyclomatic complexity of functions in a file."""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if function_name and node.name != function_name:
                    continue
                
                # Count control flow statements
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                        complexity += 1
                
                functions[node.name] = {
                    "complexity": complexity,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node)
                }
        
        return {
            "file": str(file_path),
            "functions": functions,
            "average_complexity": round(sum(f["complexity"] for f in functions.values()) / len(functions), 2) if functions else 0
        }
    except Exception as e:
        return {"error": f"Failed to analyze complexity: {str(e)}"}


@mcp.tool
def validate_python_syntax(file_path: str) -> dict:
    """Validate Python syntax of a file."""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse
        ast.parse(content)
        
        return {
            "file": str(file_path),
            "valid": True,
            "message": "File has valid Python syntax"
        }
    except SyntaxError as e:
        return {
            "file": str(file_path),
            "valid": False,
            "error": str(e),
            "line": e.lineno,
            "offset": e.offset
        }
    except Exception as e:
        return {"error": f"Failed to validate: {str(e)}"}


if __name__ == "__main__":
    # Run the server with stdio transport (default)
    mcp.run()
