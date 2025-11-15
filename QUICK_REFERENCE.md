# Agentic AI Quick Reference

A quick reference guide for common patterns, code snippets, and best practices.

## Table of Contents
- [Basic Agent Setup](#basic-agent-setup)
- [Tool Definition](#tool-definition)
- [Common Patterns](#common-patterns)
- [Prompt Templates](#prompt-templates)
- [Error Handling](#error-handling)
- [Best Practices Checklist](#best-practices-checklist)

---

## Basic Agent Setup

### Simple Agent with LangChain
```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Define tools
tools = [
    Tool(name="ToolName", func=my_function, description="What it does")
]

# Create agent
agent = create_react_agent(llm, tools, prompt_template)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run
result = executor.invoke({"input": "Your task"})
```

### LangGraph Multi-Agent
```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(StateType)
workflow.add_node("agent1", agent1_function)
workflow.add_node("agent2", agent2_function)
workflow.add_edge("agent1", "agent2")
workflow.set_entry_point("agent1")
workflow.add_edge("agent2", END)

app = workflow.compile()
result = app.invoke(initial_state)
```

---

## Tool Definition

### Basic Tool
```python
from langchain.tools import Tool

def my_tool(input: str) -> str:
    """Tool description with usage info"""
    try:
        # Tool logic
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

tool = Tool(
    name="MyTool",
    func=my_tool,
    description="Use when you need to... Args: ..."
)
```

### Structured Tool with Pydantic
```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    param1: str = Field(description="Description")
    param2: int = Field(default=10, description="Description")

def my_function(param1: str, param2: int = 10) -> str:
    return f"Result for {param1} with {param2}"

tool = StructuredTool.from_function(
    func=my_function,
    name="MyTool",
    description="Detailed description",
    args_schema=InputSchema
)
```

### Async Tool
```python
async def async_tool(param: str) -> str:
    await asyncio.sleep(1)  # Async operation
    return f"Result: {param}"

tool = StructuredTool.from_function(
    coroutine=async_tool,
    name="AsyncTool",
    description="Async tool description"
)
```

---

## Common Patterns

### ReAct Pattern
```python
# Agent alternates between:
# 1. Thought: Reasoning
# 2. Action: Tool use
# 3. Observation: Result
# 4. Repeat until answer found

template = """
Question: {input}

Thought: [reasoning]
Action: [tool_name(args)]
Observation: [result]
... (repeat)
Final Answer: [answer]
"""
```

### Plan-and-Execute
```python
class PlanAndExecuteAgent:
    def run(self, task: str):
        # Phase 1: Create plan
        plan = self.create_plan(task)
        
        # Phase 2: Execute each step
        for step in plan:
            result = self.execute_step(step)
            
        # Phase 3: Synthesize
        return self.synthesize(results)
```

### Multi-Agent (Hierarchical)
```python
class ManagerAgent:
    def delegate(self, task: str):
        # Break down task
        subtasks = self.decompose(task)
        
        # Assign to workers
        results = {}
        for subtask in subtasks:
            worker = self.select_worker(subtask)
            results[subtask] = worker.execute(subtask)
        
        # Combine results
        return self.synthesize(results)
```

---

## Prompt Templates

### System Prompt Structure
```python
system_prompt = """
[ROLE]
You are a [role description]

[CAPABILITIES]
You have access to these tools:
- Tool1: Description
- Tool2: Description

[CONSTRAINTS]
- Do not [constraint]
- Always [requirement]

[FORMAT]
Use this format:
[format specification]

[EXAMPLES]
Example 1: [demonstration]
"""
```

### ReAct Prompt
```python
react_template = """Answer the question using available tools.

Tools:
{tools}

Format:
Question: {input}
Thought: [your reasoning]
Action: [tool_name(args)]
Observation: [result]
... (repeat)
Final Answer: [answer]

Begin!

Question: {input}
{agent_scratchpad}"""
```

### Few-Shot Examples
```python
few_shot_template = """
Example 1:
Input: "What is 2+2?"
Thought: Need to calculate
Action: Calculator("2+2")
Observation: 4
Final Answer: 4

Example 2:
Input: "What's the weather in Paris?"
Thought: Need current weather data
Action: GetWeather("Paris")
Observation: Sunny, 22°C
Final Answer: Paris is sunny with 22°C

Now solve:
Input: {input}
"""
```

---

## Error Handling

### Tool Error Handling
```python
def safe_tool(input: str) -> str:
    """Tool with comprehensive error handling"""
    
    # Input validation
    if not input:
        return "Error: Input cannot be empty"
    
    try:
        # Main logic
        result = perform_operation(input)
        return f"Success: {result}"
        
    except SpecificError as e:
        return f"Error: {specific_message}"
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return f"Error: {str(e)}"
```

### Agent Error Recovery
```python
def execute_with_retry(agent, task, max_retries=3):
    """Execute agent with retry logic"""
    
    for attempt in range(max_retries):
        try:
            return agent.run(task)
            
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Failed after {max_retries} attempts: {e}"
            
            # Wait before retry (exponential backoff)
            wait_time = 2 ** attempt
            time.sleep(wait_time)
```

### Graceful Degradation
```python
def execute_with_fallback(primary, fallback, task):
    """Try primary, fallback if fails"""
    
    try:
        return primary.execute(task)
    except Exception as e:
        logger.warning(f"Primary failed: {e}, using fallback")
        return fallback.execute(task)
```

---

## Best Practices Checklist

### Agent Design
- [ ] Clear goal definition
- [ ] Maximum iteration limit set
- [ ] Logging enabled
- [ ] Error handling implemented
- [ ] Input validation added

### Tool Design
- [ ] Single responsibility per tool
- [ ] Clear, descriptive name
- [ ] Detailed docstring with examples
- [ ] Type hints for parameters
- [ ] Informative error messages
- [ ] Input validation
- [ ] Return structured results

### Prompts
- [ ] Role clearly defined
- [ ] Available tools listed
- [ ] Constraints specified
- [ ] Output format shown
- [ ] Examples provided
- [ ] Context included

### Testing
- [ ] Unit tests for tools
- [ ] Integration tests for agents
- [ ] Error cases covered
- [ ] Performance benchmarks
- [ ] Cost tracking

### Production
- [ ] Rate limiting implemented
- [ ] Caching configured
- [ ] Monitoring in place
- [ ] Human-in-the-loop for critical ops
- [ ] Security measures active
- [ ] Documentation complete

---

## Common Code Snippets

### Load Environment Variables
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

### Simple Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Agent started")
logger.error("Error occurred", exc_info=True)
```

### Rate Limiting
```python
from functools import wraps
import time

def rate_limit(calls_per_minute):
    def decorator(func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if now - c < 60]
            
            if len(calls) >= calls_per_minute:
                wait = 60 - (now - calls[0])
                time.sleep(wait)
            
            calls.append(time.time())
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

### Token Counting
```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Track usage
total_tokens = count_tokens(prompt) + count_tokens(response)
cost = total_tokens * price_per_token
```

### Caching Results
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(input: str) -> str:
    """Cache results of expensive operations"""
    # Expensive computation
    return result
```

---

## Pattern Selection Guide

| Use Case | Recommended Pattern | Key Benefit |
|----------|-------------------|-------------|
| Simple query | Direct LLM | Fast, cheap |
| Multi-step task | ReAct | Iterative problem solving |
| Complex planning | Plan-and-Execute | Organized execution |
| Multiple specialties | Multi-Agent | Specialized expertise |
| Quality-critical | Reflection | Self-improvement |
| Long conversations | Memory-Augmented | Context retention |
| Exploration | ReAct + Self-Ask | Discovery-focused |
| Safety-critical | Constitutional + HITL | Rule adherence |

---

## Debugging Tips

### Enable Verbose Mode
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Shows reasoning steps
)
```

### Add Custom Callbacks
```python
from langchain.callbacks import StdOutCallbackHandler

callbacks = [StdOutCallbackHandler()]
result = agent.run(task, callbacks=callbacks)
```

### Track Token Usage
```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = agent.run(task)
    print(f"Tokens: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost}")
```

---

## Resources

- **Theory**: [docs/theory/](docs/theory/)
- **Patterns**: [docs/design-patterns/](docs/design-patterns/)
- **Examples**: [examples/](examples/)
- **Glossary**: [docs/theory/glossary.md](docs/theory/glossary.md)

---

**For detailed information, see the main [README.md](README.md)**
