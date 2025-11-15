# Tool Use Pattern

## Overview

The Tool Use pattern (also called Function Calling) enables agents to interact with external systems, APIs, and capabilities in a structured way. Tools are the primary mechanism for agents to take actions in the world.

## Core Concept

Instead of agents generating arbitrary text, they learn to:
1. Recognize when a tool is needed
2. Select the appropriate tool
3. Format the correct parameters
4. Execute the tool
5. Interpret the results

## Pattern Structure

```
Agent receives task
  ↓
Agent analyzes available tools
  ↓
Agent selects appropriate tool
  ↓
Agent formats tool parameters
  ↓
Tool executes and returns result
  ↓
Agent processes result
  ↓
Agent decides next action
```

## Tool Definition

### Basic Tool

```python
from langchain.tools import Tool

def my_function(input: str) -> str:
    """
    Clear description of what this tool does.
    
    Args:
        input: Description of the input parameter
    
    Returns:
        Description of what's returned
    """
    # Implementation
    return result

tool = Tool(
    name="ToolName",
    func=my_function,
    description="When to use this tool and what it does"
)
```

### Structured Tool with Pydantic

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class ToolInput(BaseModel):
    """Input schema for the tool"""
    param1: str = Field(description="Description of param1")
    param2: int = Field(default=10, description="Description of param2")

def structured_function(param1: str, param2: int = 10) -> str:
    """Function implementation"""
    return f"Processed {param1} with {param2}"

tool = StructuredTool.from_function(
    func=structured_function,
    name="StructuredTool",
    description="Detailed description with parameter info",
    args_schema=ToolInput
)
```

## Tool Design Principles

### 1. Single Responsibility

Each tool should do one thing well:

```python
# Good - Focused tools
def read_file(path: str) -> str:
    """Read a file"""
    pass

def write_file(path: str, content: str) -> None:
    """Write to a file"""
    pass

def delete_file(path: str) -> None:
    """Delete a file"""
    pass

# Bad - Swiss army knife tool
def file_operations(path: str, operation: str, content: str = None):
    """Do any file operation"""
    if operation == "read":
        # read logic
    elif operation == "write":
        # write logic
    elif operation == "delete":
        # delete logic
```

### 2. Clear Naming

Tool names should be action-oriented and descriptive:

```python
# Good
"SearchWeb"
"CalculatePrice"
"SendEmail"
"QueryDatabase"

# Bad
"Searcher"
"PriceHandler"
"EmailTool"
"DBTool"
```

### 3. Rich Descriptions

Help the agent understand when and how to use the tool:

```python
def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web for information.
    
    Use this tool when you need current information from the internet.
    
    Args:
        query: The search query. Be specific for better results.
               Example: "latest AI research 2024" not just "AI"
        max_results: Number of results to return (1-100, default: 5)
    
    Returns:
        JSON string with list of results, each containing:
        - title: Result title
        - url: Result URL
        - snippet: Short description
    
    Example:
        search_web("Python tutorials", max_results=3)
        Returns top 3 Python tutorial results
    """
```

### 4. Error Handling

Return informative errors that help the agent recover:

```python
def divide_numbers(a: float, b: float) -> str:
    """Divide two numbers"""
    try:
        result = a / b
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero. Please provide a non-zero divisor."
    except TypeError:
        return f"Error: Both inputs must be numbers. Got {type(a)} and {type(b)}."
    except Exception as e:
        return f"Error: {str(e)}. Please check your inputs."
```

### 5. Validation

Validate inputs before processing:

```python
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""
    
    # Validate email address
    if not "@" in to:
        return f"Error: '{to}' is not a valid email address"
    
    # Validate required fields
    if not subject or not body:
        return "Error: Both subject and body are required"
    
    # Validate length
    if len(subject) > 100:
        return "Error: Subject must be 100 characters or less"
    
    # Send email
    try:
        # Email sending logic
        return f"Email sent successfully to {to}"
    except Exception as e:
        return f"Error sending email: {str(e)}"
```

## Advanced Tool Patterns

### 1. Async Tools

For I/O-bound operations:

```python
import asyncio

async def fetch_api_data(endpoint: str) -> str:
    """Asynchronously fetch data from API"""
    # Simulate async API call
    await asyncio.sleep(1)
    return f"Data from {endpoint}"

# Create async tool
from langchain.tools import StructuredTool

async_tool = StructuredTool.from_function(
    coroutine=fetch_api_data,
    name="FetchAPI",
    description="Fetch data from an API endpoint"
)
```

### 2. Stateful Tools

Tools that maintain state:

```python
class Calculator:
    """Stateful calculator that remembers history"""
    
    def __init__(self):
        self.history = []
        self.memory = 0
    
    def calculate(self, expression: str) -> str:
        result = eval(expression)
        self.history.append(f"{expression} = {result}")
        self.memory = result
        return str(result)
    
    def get_history(self) -> str:
        return "\n".join(self.history)
    
    def recall_memory(self) -> str:
        return str(self.memory)

# Create tools from the stateful object
calc = Calculator()
calc_tool = Tool(name="Calculate", func=calc.calculate, 
                 description="Calculate expression")
history_tool = Tool(name="GetHistory", func=lambda _: calc.get_history(),
                   description="Get calculation history")
```

### 3. Composite Tools

Tools that use other tools:

```python
def research_and_summarize(topic: str, 
                          search_tool, 
                          summarize_tool) -> str:
    """
    Composite tool that searches and then summarizes.
    """
    # Use search tool
    search_results = search_tool(topic)
    
    # Use summarize tool
    summary = summarize_tool(search_results)
    
    return f"Research on '{topic}':\n{summary}"
```

### 4. Tool Collections

Group related tools:

```python
class FileSystemTools:
    """Collection of file system tools"""
    
    @staticmethod
    def read(path: str) -> str:
        """Read file"""
        pass
    
    @staticmethod
    def write(path: str, content: str) -> str:
        """Write file"""
        pass
    
    @staticmethod
    def list_dir(path: str) -> str:
        """List directory"""
        pass
    
    @staticmethod
    def get_tools():
        """Return all tools as list"""
        return [
            Tool(name="ReadFile", func=FileSystemTools.read,
                 description="Read file contents"),
            Tool(name="WriteFile", func=FileSystemTools.write,
                 description="Write content to file"),
            Tool(name="ListDirectory", func=FileSystemTools.list_dir,
                 description="List files in directory")
        ]
```

## Tool Selection Strategies

### 1. Description-Based

Agent uses tool descriptions to decide:

```python
tools = [
    Tool(
        name="Weather",
        func=get_weather,
        description="Get current weather for a location. Use when asked about weather, temperature, or conditions."
    ),
    Tool(
        name="News",
        func=get_news,
        description="Get latest news headlines. Use when asked about current events or news."
    )
]
```

### 2. Few-Shot Examples

Provide examples of tool usage:

```python
system_prompt = """You have access to these tools:

1. Calculator - For math operations
   Example: User asks "What is 2+2?" → Use Calculator("2+2")

2. Search - For information lookup
   Example: User asks "Who is the president?" → Use Search("current president")

Choose the right tool based on these examples.
"""
```

### 3. Structured Output

Use structured output for tool calls:

```python
class ToolCall(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    reasoning: str

# Agent outputs ToolCall objects
agent_output = ToolCall(
    tool_name="SearchWeb",
    parameters={"query": "AI news", "max_results": 5},
    reasoning="User wants current AI news, need to search the web"
)
```

## Best Practices

### 1. Tool Versioning

```python
def my_tool_v1(input: str) -> str:
    """Version 1 of the tool"""
    pass

def my_tool_v2(input: str, extra_param: str = None) -> str:
    """
    Version 2 with additional parameter.
    Backwards compatible with v1.
    """
    pass
```

### 2. Rate Limiting

```python
from functools import wraps
import time

def rate_limit(calls_per_minute: int):
    """Decorator to rate limit tool calls"""
    def decorator(func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove calls older than 1 minute
            calls[:] = [c for c in calls if now - c < 60]
            
            if len(calls) >= calls_per_minute:
                return "Error: Rate limit exceeded. Please wait."
            
            calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

@rate_limit(calls_per_minute=10)
def api_call(endpoint: str) -> str:
    """Rate-limited API call"""
    pass
```

### 3. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_computation(input: str) -> str:
    """Cache expensive computations"""
    # Expensive operation
    return result
```

### 4. Logging

```python
import logging

def logged_tool(input: str) -> str:
    """Tool with comprehensive logging"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Tool called with input: {input}")
    
    try:
        result = perform_operation(input)
        logger.info(f"Tool succeeded: {result[:100]}")
        return result
    except Exception as e:
        logger.error(f"Tool failed: {str(e)}", exc_info=True)
        return f"Error: {str(e)}"
```

### 5. Security

```python
def secure_file_read(filepath: str) -> str:
    """Secure file reading with path validation"""
    import os
    
    # Define allowed directory
    ALLOWED_DIR = "/safe/directory"
    
    # Resolve absolute path
    abs_path = os.path.abspath(filepath)
    
    # Check if path is within allowed directory
    if not abs_path.startswith(ALLOWED_DIR):
        return f"Error: Access denied. File must be in {ALLOWED_DIR}"
    
    # Check for path traversal
    if ".." in filepath:
        return "Error: Path traversal detected"
    
    # Read file
    try:
        with open(abs_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"
```

## Common Pitfalls

### 1. Ambiguous Tools

```python
# Bad - Unclear when to use
def process_data(data: str) -> str:
    """Process some data"""
    pass

# Good - Clear purpose
def calculate_statistics(numbers: List[float]) -> str:
    """Calculate mean, median, and mode of a list of numbers"""
    pass
```

### 2. Poor Error Messages

```python
# Bad
def divide(a, b):
    return a / b  # Crashes on division by zero

# Good
def divide(a: float, b: float) -> str:
    if b == 0:
        return "Error: Cannot divide by zero"
    return str(a / b)
```

### 3. Missing Validation

```python
# Bad - No validation
def send_request(url: str) -> str:
    return requests.get(url).text

# Good - Validated
def send_request(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        return "Error: Invalid URL format"
    
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except requests.Timeout:
        return "Error: Request timeout"
    except Exception as e:
        return f"Error: {str(e)}"
```

## Testing Tools

```python
import pytest

def test_calculator_tool():
    """Test calculator tool"""
    result = calculator("2 + 2")
    assert result == "4"

def test_calculator_error():
    """Test calculator error handling"""
    result = calculator("invalid")
    assert "error" in result.lower()

def test_search_tool():
    """Test search tool"""
    result = search_web("test query", max_results=3)
    assert len(result) > 0
    assert "test query" in result
```

## Performance Optimization

### 1. Parallel Tool Execution

```python
import asyncio

async def execute_tools_parallel(tools: List[Tool], inputs: List[str]):
    """Execute multiple tools in parallel"""
    tasks = [tool.arun(input) for tool, input in zip(tools, inputs)]
    results = await asyncio.gather(*tasks)
    return results
```

### 2. Tool Chaining

```python
def chain_tools(tool1: Tool, tool2: Tool, input: str) -> str:
    """Chain tools together"""
    result1 = tool1.run(input)
    result2 = tool2.run(result1)
    return result2
```

## Resources

- [Tool Definition Examples](../../examples/basic/tool_definition.py)
- [Best Practices Guide](../theory/best-practices.md)
- [ReAct Pattern](./react-pattern.md) - Uses tools extensively
