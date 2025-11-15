# Multi-Agent Patterns

## Overview

Multi-agent patterns involve multiple specialized agents working together to accomplish complex tasks. This approach leverages the principle of specialization - different agents excel at different tasks.

## Why Multi-Agent?

### Advantages
1. **Specialization**: Each agent focuses on what it does best
2. **Parallelization**: Independent tasks can run simultaneously
3. **Modularity**: Easier to update or replace individual agents
4. **Scalability**: Add more agents as needed
5. **Robustness**: Failure of one agent doesn't crash the system

### Challenges
1. **Coordination**: Managing communication between agents
2. **Consistency**: Ensuring agents work toward same goals
3. **Debugging**: More complex to trace issues
4. **Cost**: Multiple agents mean multiple LLM calls
5. **Latency**: Communication overhead between agents

## Core Patterns

## 1. Hierarchical (Manager-Worker)

Manager agent delegates tasks to specialized worker agents.

### Structure
```
         Manager Agent
              |
    +---------+---------+
    |         |         |
 Worker1   Worker2   Worker3
```

### When to Use
- Clear task decomposition
- Different expertise needed
- Centralized coordination desired

### Implementation
```python
class ManagerAgent:
    def __init__(self, workers: Dict[str, Agent]):
        self.workers = workers
        
    def delegate(self, task: str) -> str:
        # Analyze task
        subtasks = self.break_down_task(task)
        
        # Assign to workers
        results = {}
        for subtask in subtasks:
            worker = self.select_worker(subtask)
            results[subtask] = worker.execute(subtask)
        
        # Synthesize results
        return self.synthesize(results)
    
    def select_worker(self, subtask: str) -> Agent:
        # Route to appropriate worker based on capability
        for name, worker in self.workers.items():
            if worker.can_handle(subtask):
                return worker
        return self.default_worker


# Example usage
manager = ManagerAgent({
    "researcher": ResearchAgent(),
    "analyst": AnalysisAgent(),
    "writer": WritingAgent()
})

result = manager.delegate("Create a report on AI trends")
```

### Example
```python
# See: examples/multi-agent/hierarchical.py

task = "Research AI and write a report"

Manager:
  → Delegates to Researcher: "Research AI trends"
  → Delegates to Analyst: "Analyze research findings"
  → Delegates to Writer: "Write report from analysis"
  → Synthesizes all results
```

## 2. Sequential (Pipeline)

Agents form a pipeline, each processing output of previous agent.

### Structure
```
Input → Agent1 → Agent2 → Agent3 → Output
```

### When to Use
- Linear workflow
- Each step depends on previous
- Clear transformation chain

### Implementation
```python
class Pipeline:
    def __init__(self, agents: List[Agent]):
        self.agents = agents
    
    def execute(self, input: str) -> str:
        result = input
        
        for agent in self.agents:
            result = agent.process(result)
            
            # Optional: validate between steps
            if not self.validate(result):
                return f"Pipeline failed at {agent.name}"
        
        return result


# Example usage
pipeline = Pipeline([
    DataCollectionAgent(),
    DataCleaningAgent(),
    DataAnalysisAgent(),
    ReportGenerationAgent()
])

output = pipeline.execute("Analyze sales data")
```

### Example
```python
task = "Process customer feedback"

Pipeline:
  Collector → collects feedback from sources
    ↓
  Classifier → categorizes by sentiment
    ↓
  Analyzer → extracts insights
    ↓
  Reporter → generates summary report
```

## 3. Parallel (Map-Reduce)

Multiple agents work on different parts simultaneously, results merged.

### Structure
```
           Input
             |
    +--------+--------+
    |        |        |
 Agent1   Agent2   Agent3
    |        |        |
    +--------+--------+
             |
          Merger
```

### When to Use
- Independent subtasks
- Need for speed
- Data can be partitioned

### Implementation
```python
import asyncio

class ParallelSystem:
    def __init__(self, agents: List[Agent], merger: Agent):
        self.agents = agents
        self.merger = merger
    
    async def execute(self, task: str) -> str:
        # Split task
        subtasks = self.split_task(task)
        
        # Execute in parallel
        tasks = [
            agent.execute_async(subtask)
            for agent, subtask in zip(self.agents, subtasks)
        ]
        results = await asyncio.gather(*tasks)
        
        # Merge results
        return self.merger.merge(results)
    
    def split_task(self, task: str) -> List[str]:
        """Split task into independent parts"""
        # Implementation depends on task type
        pass


# Example usage
system = ParallelSystem(
    agents=[Agent1(), Agent2(), Agent3()],
    merger=MergerAgent()
)

result = await system.execute("Analyze data from 3 regions")
```

### Example
```python
task = "Analyze customer reviews from 3 regions"

Split:
  → Agent1: Analyzes North region
  → Agent2: Analyzes South region  (parallel)
  → Agent3: Analyzes West region

Merge:
  → Combines regional insights
  → Creates unified report
```

## 4. Debate/Consensus

Multiple agents discuss and debate to reach best solution.

### Structure
```
     Moderator
         |
    +----+----+
    |    |    |
  A1    A2   A3
    |    |    |
  debate cycle
    |    |    |
    v    v    v
    Consensus
```

### When to Use
- Need multiple perspectives
- Complex decisions
- Quality over speed

### Implementation
```python
class DebateSystem:
    def __init__(self, agents: List[Agent], moderator: Agent, max_rounds: int = 3):
        self.agents = agents
        self.moderator = moderator
        self.max_rounds = max_rounds
    
    def debate(self, question: str) -> str:
        positions = {}
        
        for round in range(self.max_rounds):
            # Each agent presents position
            for agent in self.agents:
                # Agent sees other positions
                context = self.build_context(positions)
                positions[agent.name] = agent.argue(question, context)
            
            # Check for consensus
            if self.moderator.has_consensus(positions):
                break
        
        # Synthesize final answer
        return self.moderator.synthesize(positions)
    
    def build_context(self, positions: Dict) -> str:
        """Build context from other agents' positions"""
        return "\n".join([
            f"{name}: {position}"
            for name, position in positions.items()
        ])


# Example usage
debate = DebateSystem(
    agents=[
        OptimisticAgent(),
        PessimisticAgent(),
        NeutralAgent()
    ],
    moderator=ModeratorAgent(),
    max_rounds=3
)

answer = debate.debate("Should we invest in technology X?")
```

### Example
```python
question = "Best approach for system architecture?"

Round 1:
  Agent1: "Use microservices for scalability"
  Agent2: "Monolith is simpler to maintain"
  Agent3: "Hybrid approach balances both"

Round 2 (agents respond to each other):
  Agent1: "Microservices handle Agent2's concern via containers"
  Agent2: "Agent3's hybrid seems reasonable"
  Agent3: "Let's define clear boundaries for hybrid"

Moderator: "Consensus on hybrid approach with clear service boundaries"
```

## 5. Swarm

Many simple agents cooperate through local interactions.

### Structure
```
     Environment
         |
    [Agent Pool]
    A1 A2 A3 A4 A5
    ... (many agents)
    
    Local interactions
    → Emergent behavior
```

### When to Use
- Complex optimization
- Exploration tasks
- Distributed search

### Implementation
```python
class SwarmAgent:
    def __init__(self, id: int):
        self.id = id
        self.position = random_position()
        self.best_found = None
    
    def explore(self, environment):
        # Explore local area
        local_result = environment.evaluate(self.position)
        
        # Share with neighbors
        neighbors = self.get_neighbors()
        for neighbor in neighbors:
            if neighbor.best_found and neighbor.best_found > self.best_found:
                # Move toward better solution
                self.position = self.adjust_toward(neighbor.position)
        
        return local_result


class SwarmSystem:
    def __init__(self, num_agents: int):
        self.agents = [SwarmAgent(i) for i in range(num_agents)]
    
    def optimize(self, environment, iterations: int):
        for _ in range(iterations):
            for agent in self.agents:
                agent.explore(environment)
        
        # Return best solution found
        return max(agent.best_found for agent in self.agents)
```

## Agent Communication

### Message Passing

```python
class Message:
    def __init__(self, sender: str, receiver: str, content: str):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = time.time()


class MessageBus:
    def __init__(self):
        self.messages = []
    
    def send(self, message: Message):
        self.messages.append(message)
    
    def receive(self, agent_name: str) -> List[Message]:
        return [m for m in self.messages if m.receiver == agent_name]
```

### Shared State

```python
class SharedState:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
    
    def update(self, key: str, value: Any):
        with self.lock:
            self.data[key] = value
    
    def get(self, key: str) -> Any:
        with self.lock:
            return self.data.get(key)
```

### Event-Based

```python
class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)
    
    def subscribe(self, event_type: str, agent: Agent):
        self.subscribers[event_type].append(agent)
    
    def publish(self, event_type: str, data: Any):
        for agent in self.subscribers[event_type]:
            agent.handle_event(event_type, data)
```

## Best Practices

### 1. Clear Roles
Define specific responsibilities for each agent:

```python
class ResearchAgent:
    role = "Gather information from sources"
    capabilities = ["web_search", "database_query"]
    
class AnalysisAgent:
    role = "Analyze and extract insights"
    capabilities = ["data_analysis", "pattern_recognition"]
```

### 2. Communication Protocol
Standardize how agents communicate:

```python
class AgentMessage(BaseModel):
    sender: str
    receiver: str
    message_type: str  # "request", "response", "notification"
    content: Dict[str, Any]
    priority: int = 0
```

### 3. Error Handling
Handle agent failures gracefully:

```python
def execute_with_fallback(primary: Agent, fallback: Agent, task: str) -> str:
    try:
        return primary.execute(task)
    except Exception as e:
        logger.warning(f"Primary agent failed: {e}, using fallback")
        return fallback.execute(task)
```

### 4. Monitoring
Track multi-agent system health:

```python
class SystemMonitor:
    def track_agent(self, agent: Agent, task: str, result: str):
        self.log({
            "agent": agent.name,
            "task": task,
            "success": result.success,
            "duration": result.duration,
            "tokens_used": result.tokens
        })
```

## Common Pitfalls

### 1. Over-Fragmentation
Too many agents for simple tasks.

**Solution**: Start simple, add agents only when needed.

### 2. Communication Overhead
Too much inter-agent communication.

**Solution**: Minimize messages, batch when possible.

### 3. Inconsistent State
Agents have conflicting information.

**Solution**: Use shared state with proper locking.

### 4. Circular Dependencies
Agents waiting on each other.

**Solution**: Design clear dependency graphs.

## Example Use Cases

### Code Review System
```
Developer submits code
  → SecurityAgent: Checks for vulnerabilities
  → StyleAgent: Checks code style
  → TestAgent: Verifies tests exist
  → PerformanceAgent: Analyzes efficiency
  → SynthesisAgent: Combines feedback
```

### Content Creation
```
Manager receives "Create blog post on AI"
  → ResearchAgent: Gathers information
  → OutlineAgent: Creates structure
  → WriterAgent: Writes content
  → EditorAgent: Reviews and refines
  → SEOAgent: Optimizes for search
```

### Customer Support
```
Customer query arrives
  → ClassifierAgent: Categorizes query
  → Router: Sends to specialist
    → Technical support agent
    → Billing agent
    → General inquiries agent
  → QA Agent: Verifies response quality
```

## Tools for Multi-Agent Systems

### LangGraph
```python
from langgraph.graph import StateGraph

workflow = StateGraph(State)
workflow.add_node("researcher", research_node)
workflow.add_node("analyst", analysis_node)
workflow.add_edge("researcher", "analyst")
app = workflow.compile()
```

### CrewAI
```python
from crewai import Agent, Task, Crew

researcher = Agent(role="Researcher", goal="Find information")
analyst = Agent(role="Analyst", goal="Analyze data")

crew = Crew(agents=[researcher, analyst], tasks=[task1, task2])
result = crew.kickoff()
```

## Performance Considerations

### Latency
- Parallel execution reduces total time
- Sequential execution is slower but simpler
- Balance parallelism with coordination overhead

### Cost
- Multiple agents = multiple LLM calls
- Consider caching shared computations
- Use smaller models for simple agents

### Reliability
- More agents = more potential failures
- Implement retry logic and fallbacks
- Monitor agent health

## Resources

- [Hierarchical Multi-Agent Example](../../examples/multi-agent/hierarchical.py)
- [Best Practices](../theory/best-practices.md)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
