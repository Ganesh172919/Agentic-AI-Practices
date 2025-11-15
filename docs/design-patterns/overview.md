# Agentic AI Design Patterns

This document covers common design patterns used in building agentic AI systems. Each pattern addresses specific challenges and use cases.

## Pattern Categories

### 1. Single Agent Patterns
Patterns for individual agents performing tasks.

### 2. Multi-Agent Patterns
Patterns for coordinating multiple agents.

### 3. Tool Use Patterns
Patterns for effective tool integration and usage.

### 4. Memory Patterns
Patterns for managing agent memory and context.

## Core Patterns

## 1. ReAct (Reasoning + Acting)

**Problem**: Agents need to reason about problems and take actions iteratively.

**Solution**: Alternate between reasoning steps and action steps.

**Structure**:
```
Thought: [Agent's reasoning]
Action: [Tool to use]
Observation: [Result from tool]
Thought: [Next reasoning step]
...
Final Answer: [Solution]
```

**When to Use**:
- Multi-step problem solving
- Tasks requiring tools/APIs
- Exploratory tasks

**Example**: See [ReAct Pattern Implementation](./react-pattern.md)

---

## 2. Plan-and-Execute

**Problem**: Complex tasks need upfront planning before execution.

**Solution**: Separate planning phase from execution phase.

**Structure**:
1. **Planning Phase**: Create a detailed plan with steps
2. **Execution Phase**: Execute each step sequentially
3. **Monitoring Phase**: Track progress and adjust plan

**When to Use**:
- Well-defined complex tasks
- Tasks with clear sub-goals
- When you need to estimate time/cost upfront

**Example**: See [Plan-and-Execute Pattern](./plan-execute-pattern.md)

---

## 3. Tool Calling / Function Calling

**Problem**: Agents need structured way to use external tools and APIs.

**Solution**: Define tools with schemas that agents can invoke.

**Structure**:
```python
{
    "name": "search_web",
    "description": "Search the web for information",
    "parameters": {
        "query": "string",
        "max_results": "integer"
    }
}
```

**When to Use**:
- Integrating with external systems
- Performing structured operations
- Need reliable, predictable actions

**Example**: See [Tool Use Pattern](./tool-use-pattern.md)

---

## 4. Reflection

**Problem**: Agents make mistakes and need to self-correct.

**Solution**: Agent reviews its own output and refines it.

**Structure**:
1. Generate initial output
2. Critique the output
3. Refine based on critique
4. Repeat until satisfied

**When to Use**:
- Quality-critical outputs
- Complex generation tasks
- When iterative improvement is needed

**Example**: See [Reflection Pattern](./reflection-pattern.md)

---

## 5. Multi-Agent Collaboration

**Problem**: Complex tasks need different specialized capabilities.

**Solution**: Multiple specialized agents work together.

**Variants**:
- **Hierarchical**: Manager agent delegates to worker agents
- **Parallel**: Multiple agents work independently then merge results
- **Sequential**: Agents form a pipeline, each processing output of previous
- **Debate**: Agents argue different perspectives to reach consensus

**When to Use**:
- Tasks requiring diverse expertise
- Parallel processing opportunities
- Need for different perspectives

**Example**: See [Multi-Agent Pattern](./multi-agent-pattern.md)

---

## 6. Memory-Augmented Agents

**Problem**: Agents need to remember information across interactions.

**Solution**: Implement different types of memory storage.

**Memory Types**:
- **Short-term**: Conversation history (last N messages)
- **Long-term**: Vector database for facts and knowledge
- **Working**: Temporary storage for current task
- **Episodic**: Memory of past experiences/tasks

**When to Use**:
- Long conversations
- Tasks requiring historical context
- Learning from past interactions

**Example**: See [Memory Patterns](./memory-patterns.md)

---

## 7. Chain-of-Thought (CoT)

**Problem**: Complex reasoning requires breaking down into steps.

**Solution**: Force agent to show its reasoning process.

**Structure**:
```
Let me think step by step:
1. First, I need to understand X
2. Then, I should analyze Y
3. Based on that, Z follows
Therefore, the answer is...
```

**When to Use**:
- Math and logic problems
- Complex decision making
- Need transparency in reasoning

---

## 8. Self-Ask

**Problem**: Complex questions need decomposition into sub-questions.

**Solution**: Agent asks itself clarifying questions.

**Structure**:
```
Question: [Main question]
Are follow-up questions needed? Yes
Follow-up: [Sub-question 1]
Answer: [Answer to sub-question 1]
Follow-up: [Sub-question 2]
Answer: [Answer to sub-question 2]
So the final answer is: [Final answer]
```

**When to Use**:
- Research tasks
- Complex information gathering
- Unclear requirements

---

## 9. Human-in-the-Loop

**Problem**: Some decisions need human approval.

**Solution**: Pause for human confirmation before critical actions.

**Structure**:
1. Agent proposes action
2. System requests human approval
3. Human approves/rejects/modifies
4. Agent proceeds based on feedback

**When to Use**:
- High-stakes decisions
- Sensitive operations
- Legal/compliance requirements

---

## 10. Constitutional AI

**Problem**: Need to ensure agent follows rules and values.

**Solution**: Embed rules in agent's constitution and self-critique.

**Structure**:
1. Generate response
2. Check against constitutional rules
3. Revise if violations found
4. Repeat until compliant

**When to Use**:
- Safety-critical applications
- Need for ethical behavior
- Regulatory compliance

---

## Pattern Selection Guide

| Task Type | Recommended Pattern |
|-----------|-------------------|
| Simple queries | Direct LLM call |
| Tool usage needed | ReAct or Tool Calling |
| Complex planning | Plan-and-Execute |
| Multiple specialties | Multi-Agent |
| Iterative refinement | Reflection |
| Long conversations | Memory-Augmented |
| High accuracy needed | Chain-of-Thought + Reflection |
| Research/exploration | ReAct + Self-Ask |
| Safety-critical | Constitutional AI + Human-in-the-Loop |

## Combining Patterns

Patterns can be combined for more powerful systems:

- **ReAct + Memory**: Agent that learns from past tool usage
- **Plan-and-Execute + Multi-Agent**: Plan distributed across specialized agents
- **Reflection + Constitutional AI**: Self-improving ethical agent
- **Human-in-the-Loop + Any Pattern**: Add human oversight to any pattern

## Implementation Considerations

### Performance
- More complex patterns = more LLM calls = higher cost
- Balance capability with efficiency
- Cache when possible

### Reliability
- Simpler patterns are more reliable
- Add validation and error handling
- Set maximum iterations

### Observability
- Log all reasoning steps
- Track token usage
- Monitor success rates

## Next Steps

- Explore detailed pattern implementations in subdirectories
- Try [example implementations](../../examples/README.md)
- Learn [best practices](../theory/best-practices.md)
