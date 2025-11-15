# ReAct Pattern (Reasoning + Acting)

## Overview

ReAct (Reasoning and Acting) is one of the most fundamental patterns in agentic AI. It combines reasoning traces and task-specific actions in an interleaved manner, allowing agents to solve complex tasks through iterative cycles of thinking and doing.

## Core Concept

The agent alternates between three phases:
1. **Thought**: Reasoning about the current situation
2. **Action**: Taking an action using available tools
3. **Observation**: Receiving feedback from the action

This cycle continues until the agent reaches a final answer.

## Pattern Structure

```
Question: [User's question]

Thought: I need to figure out X by doing Y
Action: tool_name(arguments)
Observation: [Result from tool]

Thought: Based on the result, I should now do Z
Action: another_tool(arguments)
Observation: [Result from another tool]

Thought: I now have enough information to answer
Final Answer: [Complete answer]
```

## Example Scenario

**Question**: What's the current temperature in the capital of France?

```
Thought: I need to find the capital of France first
Action: search("capital of France")
Observation: Paris is the capital of France

Thought: Now I need to get the current temperature in Paris
Action: get_weather("Paris, France")
Observation: Current temperature: 18°C, partly cloudy

Thought: I have all the information needed
Final Answer: The current temperature in Paris (capital of France) is 18°C with partly cloudy conditions.
```

## Implementation

### Basic ReAct Agent

```python
from typing import List, Dict, Any, Callable
import re

class ReActAgent:
    def __init__(self, llm, tools: Dict[str, Callable]):
        """
        Args:
            llm: Language model instance
            tools: Dictionary of tool_name -> function mappings
        """
        self.llm = llm
        self.tools = tools
        self.max_iterations = 10
        
    def run(self, question: str) -> str:
        """
        Execute ReAct loop to answer the question
        """
        prompt = self._create_system_prompt()
        history = f"Question: {question}\n\n"
        
        for i in range(self.max_iterations):
            # Get agent's thought and action
            response = self.llm.generate(prompt + history)
            history += response + "\n\n"
            
            # Check if we have a final answer
            if "Final Answer:" in response:
                return self._extract_final_answer(response)
            
            # Extract and execute action
            action, args = self._parse_action(response)
            
            if action and action in self.tools:
                # Execute the tool
                observation = self.tools[action](**args)
                history += f"Observation: {observation}\n\n"
            else:
                history += "Observation: Invalid action. Please try again.\n\n"
        
        return "Max iterations reached without final answer"
    
    def _create_system_prompt(self) -> str:
        tools_desc = "\n".join([
            f"- {name}: {func.__doc__}" 
            for name, func in self.tools.items()
        ])
        
        return f"""You are a helpful assistant that uses tools to answer questions.

Available tools:
{tools_desc}

Use this format:
Thought: [your reasoning]
Action: tool_name(arg1="value1", arg2="value2")
Observation: [result will be provided]

Continue this cycle until you can provide:
Final Answer: [your final answer]

"""
    
    def _parse_action(self, response: str) -> tuple:
        """Parse action and arguments from response"""
        match = re.search(r'Action:\s*(\w+)\((.*?)\)', response)
        if match:
            action = match.group(1)
            args_str = match.group(2)
            # Simple argument parsing (in production, use proper parser)
            args = {}
            if args_str:
                for arg in args_str.split(','):
                    if '=' in arg:
                        key, value = arg.split('=', 1)
                        args[key.strip()] = value.strip().strip('"\'')
            return action, args
        return None, {}
    
    def _extract_final_answer(self, response: str) -> str:
        """Extract final answer from response"""
        match = re.search(r'Final Answer:\s*(.+)', response, re.DOTALL)
        return match.group(1).strip() if match else response


# Example usage
def search(query: str) -> str:
    """Search for information on the web"""
    # Simulate search
    knowledge = {
        "capital of France": "Paris is the capital of France",
        "population of Tokyo": "Tokyo has a population of about 14 million"
    }
    return knowledge.get(query.lower(), "No results found")

def calculate(expression: str) -> str:
    """Calculate mathematical expressions"""
    try:
        result = eval(expression)  # Don't use in production!
        return str(result)
    except:
        return "Error in calculation"

# Create and run agent
tools = {
    "search": search,
    "calculate": calculate
}

agent = ReActAgent(llm=your_llm, tools=tools)
answer = agent.run("What's the capital of France and what's 2+2?")
print(answer)
```

## Advanced Features

### 1. Tool Result Formatting

```python
def format_observation(tool_name: str, result: Any) -> str:
    """Format tool results for better agent understanding"""
    if isinstance(result, dict):
        if "error" in result:
            return f"Error: {result['error']}"
        return "\n".join([f"{k}: {v}" for k, v in result.items()])
    return str(result)
```

### 2. Action History Tracking

```python
class ReActWithHistory(ReActAgent):
    def __init__(self, llm, tools):
        super().__init__(llm, tools)
        self.action_history = []
    
    def run(self, question: str) -> str:
        self.action_history = []
        # ... rest of implementation
        
    def _execute_action(self, action: str, args: dict):
        self.action_history.append({
            "action": action,
            "args": args,
            "timestamp": time.time()
        })
        return self.tools[action](**args)
```

### 3. Retry Logic

```python
def run_with_retry(self, question: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            return self.run(question)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            # Add error to history and retry
            self.history += f"Error occurred: {e}. Let's try again.\n\n"
```

## Best Practices

### 1. Clear Thought Format
Encourage structured thinking:
```
Thought: 
- What I know: X
- What I need: Y
- Next step: Z
```

### 2. Tool Descriptions
Provide detailed tool descriptions with examples:
```python
def search(query: str) -> str:
    """
    Search for information on the web.
    
    Args:
        query: Search query string
        
    Returns:
        Relevant information or "No results found"
        
    Example:
        search("capital of France") -> "Paris is the capital of France"
    """
```

### 3. Error Recovery
Handle tool errors gracefully:
```python
try:
    result = self.tools[action](**args)
    observation = f"Success: {result}"
except Exception as e:
    observation = f"Error: {str(e)}. Please try a different approach."
```

### 4. Iteration Limits
Always set maximum iterations to prevent infinite loops:
```python
self.max_iterations = 10  # Adjust based on task complexity
```

## Common Pitfalls

### 1. Verbose Thoughts
**Problem**: Agent's thoughts are too long and waste tokens
**Solution**: Prompt for concise reasoning

### 2. Invalid Actions
**Problem**: Agent tries to use non-existent tools
**Solution**: Provide clear error messages and available tool list

### 3. Repetitive Actions
**Problem**: Agent keeps trying the same failed action
**Solution**: Track action history and prompt to try different approach

### 4. No Progress
**Problem**: Agent doesn't make progress toward goal
**Solution**: Add intermediate checkpoints and success criteria

## Variations

### ReAct with Memory
Store observations for future reference:
```python
class ReActWithMemory(ReActAgent):
    def __init__(self, llm, tools):
        super().__init__(llm, tools)
        self.memory = []
    
    def _store_observation(self, obs: str):
        self.memory.append(obs)
```

### ReAct with Planning
Add planning phase before acting:
```python
def run_with_planning(self, question: str) -> str:
    # First, create a plan
    plan = self.llm.generate(f"Create a step-by-step plan for: {question}")
    
    # Then execute with ReAct
    return self.run(question, plan=plan)
```

## When to Use ReAct

**Good for**:
- Exploratory tasks
- Tasks requiring multiple tools
- Complex reasoning chains
- Learning and adapting

**Not ideal for**:
- Simple single-step tasks (use direct tool calling)
- Tasks needing upfront planning (use Plan-and-Execute)
- Highly structured workflows (use state machines)

## Performance Metrics

Track these metrics for ReAct agents:
- Average iterations to completion
- Token usage per task
- Success rate
- Tool usage distribution
- Time to completion

## Example: Real-World Code Assistant

See [examples/react-pattern/code_assistant.py](../../examples/react-pattern/code_assistant.py) for a complete implementation of a ReAct agent that helps with coding tasks.

## Resources

- Original Paper: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [LangChain ReAct Agent](https://python.langchain.com/docs/modules/agents/agent_types/react)
- [Example Implementations](../../examples/react-pattern/)
