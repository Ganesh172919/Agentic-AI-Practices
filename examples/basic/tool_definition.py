"""
Tool Definition Examples

This module demonstrates best practices for defining tools that agents can use.
Tools are the primary way agents interact with the world.

Key Principles:
1. Clear, descriptive names
2. Detailed docstrings
3. Typed parameters
4. Informative return values
5. Proper error handling
"""

from typing import Optional, List, Dict, Any
from langchain.tools import Tool, StructuredTool
from pydantic import BaseModel, Field
import json


# ============================================================================
# BASIC TOOL DEFINITION
# ============================================================================

def simple_calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    
    This is a basic tool with simple string input/output.
    
    Args:
        expression: A mathematical expression like "2 + 2" or "10 * 5"
    
    Returns:
        The result of the calculation as a string
    
    Examples:
        >>> simple_calculator("2 + 2")
        "4"
        >>> simple_calculator("10 / 2")
        "5.0"
    """
    try:
        result = eval(expression)  # WARNING: Not safe for production!
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# Wrap in LangChain Tool
calculator_tool = Tool(
    name="Calculator",
    func=simple_calculator,
    description="Evaluates mathematical expressions. Input: expression string. Returns: result."
)


# ============================================================================
# STRUCTURED TOOL WITH PYDANTIC
# ============================================================================

class SearchInput(BaseModel):
    """Input schema for search tool"""
    query: str = Field(description="The search query")
    max_results: int = Field(default=5, description="Maximum number of results to return")
    filter_type: Optional[str] = Field(default=None, description="Filter by type: 'news', 'academic', 'general'")


class SearchOutput(BaseModel):
    """Output schema for search results"""
    results: List[Dict[str, str]]
    total_found: int
    query: str


def structured_search(query: str, max_results: int = 5, filter_type: Optional[str] = None) -> str:
    """
    Search for information with structured input/output.
    
    This demonstrates using Pydantic models for better type safety.
    
    Args:
        query: The search query string
        max_results: Maximum number of results (default: 5, max: 100)
        filter_type: Optional filter ('news', 'academic', 'general')
    
    Returns:
        JSON string with search results
    """
    # Simulate search
    mock_results = [
        {"title": f"Result {i}", "url": f"https://example.com/{i}", "snippet": f"Information about {query}"}
        for i in range(1, min(max_results, 4) + 1)
    ]
    
    output = SearchOutput(
        results=mock_results,
        total_found=len(mock_results),
        query=query
    )
    
    return json.dumps(output.dict(), indent=2)


# Create structured tool
search_tool = StructuredTool.from_function(
    func=structured_search,
    name="WebSearch",
    description="""Search the web for information.
    
    Parameters:
    - query: What to search for
    - max_results: How many results to return (1-100)
    - filter_type: Optional filter ('news', 'academic', 'general')
    
    Returns JSON with search results including title, url, and snippet.
    """,
    args_schema=SearchInput
)


# ============================================================================
# TOOL WITH RICH ERROR HANDLING
# ============================================================================

def file_reader(filepath: str) -> str:
    """
    Read contents of a file with comprehensive error handling.
    
    Demonstrates proper error handling and informative error messages.
    
    Args:
        filepath: Path to the file to read
    
    Returns:
        File contents or detailed error message
    """
    import os
    
    # Validate input
    if not filepath:
        return "Error: filepath cannot be empty"
    
    if not isinstance(filepath, str):
        return f"Error: filepath must be a string, got {type(filepath)}"
    
    # Check file exists
    if not os.path.exists(filepath):
        return f"Error: File not found at '{filepath}'. Please check the path."
    
    # Check if it's a file (not directory)
    if not os.path.isfile(filepath):
        return f"Error: '{filepath}' is not a file. It may be a directory."
    
    # Check file size
    file_size = os.path.getsize(filepath)
    max_size = 1024 * 1024  # 1MB
    if file_size > max_size:
        return f"Error: File too large ({file_size} bytes). Maximum size is {max_size} bytes."
    
    # Try to read
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Successfully read {len(content)} characters from '{filepath}':\n\n{content}"
    except UnicodeDecodeError:
        return f"Error: File '{filepath}' is not a text file or uses unsupported encoding."
    except PermissionError:
        return f"Error: Permission denied when reading '{filepath}'."
    except Exception as e:
        return f"Error reading file: {str(e)}"


file_tool = Tool(
    name="FileReader",
    func=file_reader,
    description="""Read contents of a text file.
    
    Input: filepath (string) - Absolute or relative path to the file
    Output: File contents or detailed error message
    
    Handles errors gracefully and provides helpful feedback.
    """
)


# ============================================================================
# TOOL WITH STATE MANAGEMENT
# ============================================================================

class NoteTaker:
    """
    A tool that maintains state across calls.
    
    Useful for tasks that need to remember information.
    """
    
    def __init__(self):
        self.notes: Dict[str, str] = {}
    
    def add_note(self, key: str, value: str) -> str:
        """Add or update a note"""
        self.notes[key] = value
        return f"Note '{key}' saved successfully. Total notes: {len(self.notes)}"
    
    def get_note(self, key: str) -> str:
        """Retrieve a note"""
        if key in self.notes:
            return f"Note '{key}': {self.notes[key]}"
        return f"Note '{key}' not found. Available notes: {list(self.notes.keys())}"
    
    def list_notes(self) -> str:
        """List all notes"""
        if not self.notes:
            return "No notes saved yet."
        
        notes_list = "\n".join([f"- {k}: {v}" for k, v in self.notes.items()])
        return f"All notes ({len(self.notes)}):\n{notes_list}"
    
    def clear_notes(self) -> str:
        """Clear all notes"""
        count = len(self.notes)
        self.notes.clear()
        return f"Cleared {count} notes."


# Create stateful tools
note_taker = NoteTaker()

add_note_tool = Tool(
    name="AddNote",
    func=note_taker.add_note,
    description="Save a note with a key-value pair. Args: key (string), value (string)"
)

get_note_tool = Tool(
    name="GetNote",
    func=note_taker.get_note,
    description="Retrieve a saved note by key. Args: key (string)"
)

list_notes_tool = Tool(
    name="ListNotes",
    func=lambda _: note_taker.list_notes(),
    description="List all saved notes. No arguments needed."
)


# ============================================================================
# ASYNC TOOL EXAMPLE
# ============================================================================

async def async_api_call(endpoint: str, params: Optional[Dict] = None) -> str:
    """
    Asynchronous API call tool.
    
    Useful for I/O-bound operations that can run concurrently.
    
    Args:
        endpoint: API endpoint to call
        params: Optional parameters for the API call
    
    Returns:
        API response as string
    """
    import asyncio
    
    # Simulate async API call
    await asyncio.sleep(0.5)  # Simulated network delay
    
    response = {
        "endpoint": endpoint,
        "params": params or {},
        "status": "success",
        "data": f"Response from {endpoint}"
    }
    
    return json.dumps(response, indent=2)


# For async tools, use coroutine parameter
async_api_tool = StructuredTool.from_function(
    coroutine=async_api_call,
    name="AsyncAPI",
    description="Make asynchronous API calls. Args: endpoint (string), params (optional dict)"
)


# ============================================================================
# TOOL COMPOSITION
# ============================================================================

def compose_tools(tool1_result: str, tool2_result: str) -> str:
    """
    Combine results from multiple tools.
    
    Demonstrates how to create meta-tools that use other tools.
    """
    return f"Combined Results:\n\nFrom Tool 1:\n{tool1_result}\n\nFrom Tool 2:\n{tool2_result}"


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_tools():
    """Show how different tools work"""
    
    print("=" * 70)
    print("TOOL DEFINITION EXAMPLES")
    print("=" * 70)
    
    # Basic tool
    print("\n1. Basic Calculator Tool:")
    print("-" * 70)
    result1 = calculator_tool.func("2 + 2")
    print(f"Input: '2 + 2'")
    print(f"Output: {result1}")
    
    # Structured tool
    print("\n2. Structured Search Tool:")
    print("-" * 70)
    result2 = search_tool.func(query="artificial intelligence", max_results=3)
    print(f"Input: query='artificial intelligence', max_results=3")
    print(f"Output:\n{result2}")
    
    # Error handling tool
    print("\n3. File Reader with Error Handling:")
    print("-" * 70)
    result3 = file_tool.func("nonexistent_file.txt")
    print(f"Input: 'nonexistent_file.txt'")
    print(f"Output: {result3}")
    
    # Stateful tool
    print("\n4. Stateful Note-Taking Tool:")
    print("-" * 70)
    print(add_note_tool.func("task1", "Complete documentation"))
    print(add_note_tool.func("task2", "Review code"))
    print(list_notes_tool.func(""))
    
    print("\n" + "=" * 70)
    print("TOOL BEST PRACTICES SUMMARY")
    print("=" * 70)
    print("""
1. Clear Naming: Use descriptive, action-oriented names
2. Rich Descriptions: Include parameters, return values, examples
3. Type Safety: Use Pydantic models for complex inputs
4. Error Handling: Return informative error messages
5. State Management: Use classes for tools that need memory
6. Async Support: Use async for I/O-bound operations
7. Composability: Design tools to work together
8. Validation: Check inputs before processing
9. Documentation: Include docstrings with examples
10. Testing: Write tests for each tool
    """)


if __name__ == "__main__":
    demonstrate_tools()
