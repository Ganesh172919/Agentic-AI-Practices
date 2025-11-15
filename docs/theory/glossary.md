# Agentic AI Glossary

A comprehensive glossary of terms used in agentic AI systems.

## A

**Action**
A step taken by an agent to interact with its environment, typically through tool execution.

**Action Space**
The set of all possible actions an agent can take in a given environment.

**Agent**
An autonomous entity that perceives its environment and takes actions to achieve goals.

**Agent Executor**
A component that manages the agent's execution loop, handling tool calls and state management.

**Autonomous**
Capable of operating independently without constant human intervention.

## B

**Backbone Model**
The underlying language model (LLM) that powers the agent's reasoning capabilities.

**Backoff Strategy**
A retry mechanism that increases wait time between failed attempts.

**Branching**
Creating multiple execution paths based on conditions or decisions.

## C

**Chain-of-Thought (CoT)**
A prompting technique where the model explicitly shows its reasoning steps.

**Checkpoint**
A saved state in the agent's execution that can be restored if needed.

**Circular Dependency**
When tools or agents depend on each other in a loop, potentially causing deadlock.

**Constitutional AI**
An approach where agents follow predefined rules and principles.

**Context Window**
The amount of text (in tokens) that a language model can process at once.

## D

**Delegation**
When one agent assigns tasks to other specialized agents.

**Deterministic**
Producing the same output for the same input every time.

**Dynamic Planning**
Adjusting plans during execution based on results and feedback.

## E

**Embedding**
A vector representation of text used for semantic search and similarity.

**Environment**
The context or system in which an agent operates (e.g., file system, web, database).

**Episodic Memory**
Memory of past experiences and task executions.

**Execution Loop**
The cycle of perceiving, reasoning, acting, and observing.

## F

**Fallback**
Alternative action or path when the primary approach fails.

**Few-Shot Learning**
Providing a few examples to guide the model's behavior.

**Function Calling**
Structured way for LLMs to invoke functions with specific parameters.

## G

**Goal-Oriented**
Behavior directed toward achieving specific objectives.

**Graceful Degradation**
Continuing to operate with reduced functionality when errors occur.

**Grounding**
Connecting agent responses to factual, verifiable information.

## H

**Hallucination**
When an AI model generates incorrect or fabricated information.

**Hierarchical Agent**
A manager agent that coordinates multiple worker agents.

**Human-in-the-Loop (HITL)**
Including human decisions or approvals in the agent's workflow.

## I

**Idempotent**
An operation that produces the same result no matter how many times it's executed.

**Instruction Tuning**
Fine-tuning a model to follow instructions better.

**Iteration Limit**
Maximum number of steps an agent can take to prevent infinite loops.

## L

**LangChain**
A framework for developing applications powered by language models.

**LangGraph**
A library for building stateful, multi-agent applications.

**Latency**
The delay between requesting an action and receiving a response.

**Long-term Memory**
Persistent storage of information across sessions.

## M

**Max Iterations**
The maximum number of reasoning-action cycles allowed.

**Memory-Augmented**
Agents enhanced with additional memory capabilities beyond the context window.

**Meta-Agent**
An agent that manages or coordinates other agents.

**Multi-Agent System**
Multiple agents working together to accomplish tasks.

## N

**Non-deterministic**
Producing potentially different outputs for the same input.

**Node**
A step or component in a workflow graph.

## O

**Observation**
Feedback from the environment after an agent takes an action.

**One-Shot Learning**
Learning from a single example.

**Orchestration**
Coordinating multiple agents or tools to work together.

## P

**Parallel Execution**
Running multiple operations simultaneously.

**Plan-and-Execute**
A pattern where planning happens before execution.

**Planner**
Component responsible for creating execution plans.

**Prompt Engineering**
Crafting effective prompts to guide model behavior.

**Prompt Template**
A reusable structure for creating prompts with variables.

## R

**Rate Limiting**
Restricting the number of operations per time period.

**ReAct**
Reasoning and Acting pattern - alternating between thinking and doing.

**Reasoning Trace**
The recorded thought process of an agent.

**Reflection**
When an agent critiques and improves its own output.

**Replanning**
Creating a new plan when the original plan fails or circumstances change.

**Router**
Component that decides which path or agent to use next.

## S

**Sandbox**
An isolated environment for safe agent execution.

**Scratchpad**
Temporary storage for an agent's working memory.

**Self-Ask**
Pattern where agent asks itself clarifying questions.

**Semantic Search**
Finding information based on meaning rather than exact keywords.

**Sequential Execution**
Running operations one after another in order.

**Short-term Memory**
Recent conversation history kept in the context window.

**State**
The current condition of the agent and its environment.

**State Graph**
A graph representing different states and transitions in a workflow.

**Stateful**
Maintaining information across multiple interactions.

**Stateless**
Each interaction is independent with no retained information.

**Streaming**
Sending output incrementally as it's generated rather than all at once.

## T

**Temperature**
A parameter controlling randomness in model outputs (0 = deterministic, higher = more random).

**Token**
A unit of text (word, subword, or character) processed by language models.

**Tool**
A function or capability that an agent can use to interact with the world.

**Tool Calling**
The mechanism by which an agent invokes tools with parameters.

**Trajectory**
The sequence of states and actions taken by an agent.

## V

**Validation**
Checking inputs or outputs for correctness and safety.

**Vector Database**
A database optimized for storing and searching embeddings.

**Verbose Mode**
Outputting detailed information about agent reasoning and actions.

## W

**Workflow**
A series of steps or processes to accomplish a task.

**Working Memory**
Temporary storage for information needed during current task.

## Z

**Zero-Shot Learning**
Performing a task without any examples.

---

## Common Abbreviations

- **AI** - Artificial Intelligence
- **API** - Application Programming Interface
- **CoT** - Chain-of-Thought
- **HITL** - Human-in-the-Loop
- **LLM** - Large Language Model
- **RAG** - Retrieval-Augmented Generation
- **ReAct** - Reasoning and Acting
- **SFT** - Supervised Fine-Tuning
- **ToT** - Tree of Thoughts

## Related Concepts

### From Reinforcement Learning
- **Policy** - Strategy for choosing actions
- **Reward** - Feedback signal for actions
- **Episode** - A complete task execution

### From Software Engineering
- **Idempotency** - Same result from repeated operations
- **Middleware** - Software between components
- **Pipeline** - Sequential processing chain

### From Cognitive Science
- **Working Memory** - Short-term information storage
- **Episodic Memory** - Memory of events
- **Semantic Memory** - Memory of facts

## Usage Examples

### In Context

**"The agent used ReAct pattern with a max iteration of 10."**
- The agent alternated between reasoning and acting
- It was limited to 10 reasoning-action cycles

**"We implemented HITL for critical operations."**
- Human approval required for important decisions

**"The tool exhibits idempotent behavior."**
- Running the tool multiple times produces consistent results

**"Add few-shot examples to the prompt template."**
- Include example inputs and outputs in the prompt

**"The agent maintains episodic memory of past tasks."**
- Agent remembers previous task executions

## See Also

- [Introduction to Agentic AI](./introduction-to-agentic-ai.md)
- [Best Practices](./best-practices.md)
- [Design Patterns](../design-patterns/overview.md)
