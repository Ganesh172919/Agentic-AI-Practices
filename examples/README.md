# Agentic AI Examples

This directory contains practical code examples demonstrating various agentic AI patterns and implementations.

## Directory Structure

### `/basic` - Foundational Examples
Simple examples to understand core concepts:
- `simple_agent.py` - Basic agent with tool calling
- `tool_definition.py` - How to define and use tools
- `agent_loop.py` - Understanding the agent execution loop

### `/react-pattern` - ReAct Implementation
Examples using the ReAct (Reasoning + Acting) pattern:
- `basic_react.py` - Simple ReAct agent
- `react_with_tools.py` - ReAct agent with multiple tools
- `code_assistant.py` - Code debugging assistant

### `/tool-use` - Advanced Tool Usage
Patterns for effective tool integration:
- `tool_composition.py` - Combining tools effectively
- `error_handling.py` - Robust tool error handling
- `parallel_tools.py` - Using tools in parallel

### `/multi-agent` - Multi-Agent Systems
Examples with multiple cooperating agents:
- `hierarchical.py` - Manager-worker pattern
- `sequential.py` - Pipeline of specialized agents
- `debate.py` - Multiple agents debating solutions

### `/planning` - Planning Agents
Agents that plan before executing:
- `plan_and_execute.py` - Separate planning and execution
- `dynamic_planning.py` - Adjusting plans based on results
- `hierarchical_planning.py` - Breaking down complex plans

## Getting Started

### Prerequisites

```bash
# Install dependencies
pip install langchain langgraph langchain-openai python-dotenv

# Or use uv (faster)
uv pip install langchain langgraph langchain-openai python-dotenv
```

### Environment Setup

Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

### Running Examples

```bash
# Run a basic example
python examples/basic/simple_agent.py

# Run ReAct pattern
python examples/react-pattern/basic_react.py

# Run multi-agent example
python examples/multi-agent/hierarchical.py
```

## Learning Path

### Level 1: Fundamentals
1. Start with `basic/simple_agent.py` - Understand agent basics
2. Read `basic/tool_definition.py` - Learn tool creation
3. Try `basic/agent_loop.py` - Understand execution flow

### Level 2: Core Patterns
1. Study `react-pattern/basic_react.py` - Learn ReAct
2. Explore `tool-use/tool_composition.py` - Advanced tool usage
3. Try `react-pattern/code_assistant.py` - Real-world application

### Level 3: Advanced Concepts
1. `planning/plan_and_execute.py` - Strategic planning
2. `multi-agent/hierarchical.py` - Multi-agent coordination
3. Build your own agent for a specific use case!

## Example Templates

### Basic Agent Template

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# Define your tools
def my_tool(input: str) -> str:
    """Tool description"""
    return "result"

tools = [Tool(name="MyTool", func=my_tool, description="What it does")]

# Create agent
llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, tools, prompt_template)
executor = AgentExecutor(agent=agent, tools=tools)

# Run
result = executor.invoke({"input": "Your question"})
```

### Multi-Agent Template

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    messages: list
    current_agent: str

def agent_1(state: State):
    # First agent logic
    return state

def agent_2(state: State):
    # Second agent logic
    return state

# Build graph
workflow = StateGraph(State)
workflow.add_node("agent_1", agent_1)
workflow.add_node("agent_2", agent_2)
workflow.add_edge("agent_1", "agent_2")
workflow.add_edge("agent_2", END)

app = workflow.compile()
result = app.invoke(initial_state)
```

## Common Patterns

### Pattern: ReAct Agent
```python
# See: react-pattern/basic_react.py
agent_type = "react"  # Reasoning + Acting
```

### Pattern: Plan-and-Execute
```python
# See: planning/plan_and_execute.py
1. Create plan
2. Execute steps
3. Monitor and adjust
```

### Pattern: Multi-Agent Collaboration
```python
# See: multi-agent/hierarchical.py
Manager → assigns → Worker Agents
```

## Best Practices Demonstrated

1. **Error Handling**: See `tool-use/error_handling.py`
2. **Logging**: All examples include comprehensive logging
3. **Testing**: Each example includes unit tests
4. **Documentation**: Inline comments explain each step
5. **Modularity**: Reusable components across examples

## Troubleshooting

### Common Issues

**API Key Error**
```
Error: OpenAI API key not found
Solution: Check your .env file has OPENAI_API_KEY set
```

**Import Error**
```
Error: No module named 'langchain'
Solution: Install dependencies: pip install -r requirements.txt
```

**Rate Limit Error**
```
Error: Rate limit exceeded
Solution: Add delays or use GPT-3.5-turbo for testing
```

## Contributing Examples

To add a new example:
1. Choose appropriate directory
2. Follow existing code structure
3. Include docstrings and comments
4. Add to this README
5. Include test cases

## Additional Resources

- [Theory Documentation](../docs/theory/)
- [Design Patterns](../docs/design-patterns/)
- [Best Practices](../docs/theory/best-practices.md)

## Example Use Cases

### Research Assistant
Combines search, summarization, and analysis tools.
See: `react-pattern/research_assistant.py`

### Code Debugger
Reads code, identifies bugs, suggests fixes.
See: `react-pattern/code_assistant.py`

### Data Analyzer
Queries databases, performs analysis, generates reports.
See: `tool-use/data_analyzer.py`

### Content Creator
Plans content, generates drafts, edits and refines.
See: `planning/content_creator.py`

### Multi-Agent System
Multiple specialized agents collaborate on complex tasks.
See: `multi-agent/task_solver.py`
