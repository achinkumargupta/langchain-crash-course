"""
FastMCP 2.0 Server - Book Tools MCP Server

A practical MCP server that provides tools for working with books.
This server demonstrates core FastMCP concepts including:
- Tool definition and registration
- Type hints and automatic schema generation
- Multiple tool implementations
- Error handling
"""

import os
from pathlib import Path
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Book Tools Server", version="1.0.0")

# Path to books directory
BOOKS_DIR = Path(__file__).parent.parent / "4_rag" / "books"


@mcp.tool
def list_available_books() -> dict:
    """List all available books in the library."""
    if not BOOKS_DIR.exists():
        return {"books": [], "count": 0, "error": "Books directory not found"}
    
    books = []
    for book_file in sorted(BOOKS_DIR.glob("*.txt")):
        books.append({
            "name": book_file.stem,
            "filename": book_file.name,
            "size_kb": round(book_file.stat().st_size / 1024, 2)
        })
    
    return {
        "books": books,
        "count": len(books)
    }


@mcp.tool
def get_book_content(book_name: str, max_lines: int = 50) -> dict:
    """Get the content of a specific book, limited to max_lines."""
    book_path = BOOKS_DIR / f"{book_name}.txt"
    
    if not book_path.exists():
        return {
            "error": f"Book '{book_name}' not found",
            "available_books": [b.stem for b in BOOKS_DIR.glob("*.txt")]
        }
    
    try:
        with open(book_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        content = ''.join(lines[:max_lines])
        return {
            "book": book_name,
            "lines_returned": min(max_lines, len(lines)),
            "total_lines": len(lines),
            "content": content
        }
    except Exception as e:
        return {"error": f"Failed to read book: {str(e)}"}


@mcp.tool
def search_in_book(book_name: str, search_term: str) -> dict:
    """Search for a term in a specific book and return matching lines."""
    book_path = BOOKS_DIR / f"{book_name}.txt"
    
    if not book_path.exists():
        return {"error": f"Book '{book_name}' not found"}
    
    try:
        with open(book_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Search for matching lines (case-insensitive)
        search_lower = search_term.lower()
        matches = []
        for i, line in enumerate(lines, 1):
            if search_lower in line.lower():
                matches.append({
                    "line_number": i,
                    "content": line.strip()
                })
        
        # Limit results to first 20 matches
        return {
            "book": book_name,
            "search_term": search_term,
            "matches_found": len(matches),
            "matches": matches[:20],
            "truncated": len(matches) > 20
        }
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}


@mcp.tool
def get_book_statistics(book_name: str) -> dict:
    """Get statistics about a book including word count and basic metrics."""
    book_path = BOOKS_DIR / f"{book_name}.txt"
    
    if not book_path.exists():
        return {"error": f"Book '{book_name}' not found"}
    
    try:
        with open(book_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        words = content.split()
        characters = len(content)
        
        # Find average word length
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        
        return {
            "book": book_name,
            "total_lines": len(lines),
            "total_words": len(words),
            "total_characters": characters,
            "average_word_length": round(avg_word_length, 2),
            "size_mb": round(characters / (1024 * 1024), 3)
        }
    except Exception as e:
        return {"error": f"Failed to calculate statistics: {str(e)}"}


@mcp.tool
def get_book_preview(book_name: str, lines: int = 10) -> dict:
    """Get a quick preview of the first N lines of a book."""
    book_path = BOOKS_DIR / f"{book_name}.txt"
    
    if not book_path.exists():
        return {"error": f"Book '{book_name}' not found"}
    
    try:
        with open(book_path, 'r', encoding='utf-8', errors='ignore') as f:
            preview = []
            for i, line in enumerate(f):
                if i >= lines:
                    break
                preview.append(line.rstrip())
        
        return {
            "book": book_name,
            "preview_lines": len(preview),
            "content": '\n'.join(preview)
        }
    except Exception as e:
        return {"error": f"Failed to get preview: {str(e)}"}


@mcp.tool
def compare_books(book1: str, book2: str) -> dict:
    """Compare statistics between two books."""
    books = [book1, book2]
    stats = {}
    
    for book in books:
        book_path = BOOKS_DIR / f"{book}.txt"
        if not book_path.exists():
            return {"error": f"Book '{book}' not found"}
        
        try:
            with open(book_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            words = content.split()
            stats[book] = {
                "word_count": len(words),
                "character_count": len(content),
                "line_count": len(content.split('\n'))
            }
        except Exception as e:
            return {"error": f"Failed to read book {book}: {str(e)}"}
    
    # Calculate differences
    word_diff = stats[book2]["word_count"] - stats[book1]["word_count"]
    char_diff = stats[book2]["character_count"] - stats[book1]["character_count"]
    
    return {
        "book1": book1,
        "book2": book2,
        "stats": stats,
        "differences": {
            "word_count_diff": word_diff,
            "word_count_percentage": round((word_diff / stats[book1]["word_count"] * 100), 2) if stats[book1]["word_count"] > 0 else 0,
            "character_count_diff": char_diff
        }
    }


if __name__ == "__main__":
    # Run the server with stdio transport (default)
    # Use transport="http" and port=8000 for HTTP transport
    mcp.run()
