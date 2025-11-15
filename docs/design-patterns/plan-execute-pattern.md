# Plan-and-Execute Pattern

## Overview

The Plan-and-Execute pattern separates the planning phase from the execution phase, allowing agents to think strategically before taking action. This pattern is particularly effective for complex, well-defined tasks that benefit from upfront planning.

## Core Concept

Unlike ReAct which interleaves thinking and acting, Plan-and-Execute works in distinct phases:

1. **Planning Phase**: Create a comprehensive plan with all steps
2. **Execution Phase**: Execute each step in sequence
3. **Monitoring Phase**: Track progress and adapt as needed

## Pattern Structure

```
Input: Task description

Phase 1: PLANNING
→ Analyze task
→ Identify sub-goals
→ Create ordered step list
→ Estimate resources needed

Phase 2: EXECUTION
For each step in plan:
  → Execute step
  → Record result
  → Update context
  → Check progress

Phase 3: COMPLETION
→ Synthesize results
→ Verify completion
→ Return final output
```

## When to Use

### Ideal For:
- ✅ Complex tasks with clear end goals
- ✅ Tasks where planning saves execution time
- ✅ Projects needing resource estimation
- ✅ Workflows with dependencies between steps
- ✅ Tasks where you need progress tracking

### Not Ideal For:
- ❌ Exploratory tasks with unclear requirements
- ❌ Tasks where environment changes rapidly
- ❌ Simple single-step operations
- ❌ Highly interactive workflows

## Advantages

### 1. Better Resource Planning
Knowing all steps upfront allows for:
- Cost estimation
- Time estimation
- Resource allocation

### 2. Improved Debugging
Separate phases make it easier to identify where issues occur:
- Planning errors vs execution errors
- Step-level tracking

### 3. Progress Visibility
Clear progress metrics:
- Steps completed / total steps
- Current phase
- Time remaining estimates

### 4. Easier Parallelization
With a complete plan, you can:
- Identify independent steps
- Execute in parallel
- Optimize execution order

## Implementation

### Basic Implementation

```python
class PlanAndExecuteAgent:
    def __init__(self, llm):
        self.llm = llm
        self.plan = []
        self.results = []
    
    def plan(self, task: str) -> List[Step]:
        """Create execution plan"""
        prompt = f"""
        Create a step-by-step plan for: {task}
        
        Format:
        1. [Step description]
        2. [Step description]
        ...
        """
        
        response = self.llm.generate(prompt)
        plan = self._parse_plan(response)
        self.plan = plan
        return plan
    
    def execute(self) -> Dict:
        """Execute the plan"""
        for step in self.plan:
            result = self._execute_step(step)
            self.results.append(result)
            
            # Check if replanning needed
            if self._should_replan(result):
                self.plan = self.replan()
        
        return self._synthesize_results()
    
    def _execute_step(self, step: Step) -> Result:
        """Execute a single step"""
        # Use tools/LLM to execute
        pass
    
    def _should_replan(self, result: Result) -> bool:
        """Decide if replanning is needed"""
        return result.has_errors()
    
    def run(self, task: str) -> Dict:
        """Complete plan-and-execute cycle"""
        self.plan(task)
        return self.execute()
```

### Advanced Features

#### 1. Dynamic Replanning

```python
def replan(self, completed_steps: List[Step]) -> List[Step]:
    """
    Replan based on execution results.
    Keeps completed steps, revises remaining steps.
    """
    context = self._build_context(completed_steps)
    
    prompt = f"""
    Original task: {self.original_task}
    
    Completed steps:
    {context}
    
    Issue encountered: {self.last_error}
    
    Create a revised plan for remaining work:
    """
    
    new_plan = self.llm.generate(prompt)
    return self._parse_plan(new_plan)
```

#### 2. Step Dependencies

```python
class Step:
    def __init__(self, description: str, depends_on: List[int] = None):
        self.description = description
        self.depends_on = depends_on or []
        self.status = "pending"
    
    def can_execute(self, completed_steps: Set[int]) -> bool:
        """Check if all dependencies are satisfied"""
        return all(dep in completed_steps for dep in self.depends_on)


def execute_with_dependencies(plan: List[Step]):
    """Execute steps respecting dependencies"""
    completed = set()
    
    while len(completed) < len(plan):
        for i, step in enumerate(plan):
            if i not in completed and step.can_execute(completed):
                execute_step(step)
                completed.add(i)
```

#### 3. Parallel Execution

```python
import asyncio

async def execute_parallel(plan: List[Step]):
    """Execute independent steps in parallel"""
    
    # Group by dependency level
    levels = group_by_dependency_level(plan)
    
    for level in levels:
        # Execute all steps in this level in parallel
        tasks = [execute_step_async(step) for step in level]
        results = await asyncio.gather(*tasks)
        
        # Check results before proceeding
        if any(r.failed for r in results):
            return handle_failure(results)
    
    return combine_results(results)
```

#### 4. Progress Tracking

```python
class ProgressTracker:
    def __init__(self, plan: List[Step]):
        self.total_steps = len(plan)
        self.completed_steps = 0
        self.start_time = time.time()
    
    def update(self, step_result: Result):
        """Update progress metrics"""
        self.completed_steps += 1
        
    def get_progress(self) -> Dict:
        """Get current progress"""
        elapsed = time.time() - self.start_time
        progress_pct = self.completed_steps / self.total_steps
        
        return {
            "completed": self.completed_steps,
            "total": self.total_steps,
            "percentage": progress_pct * 100,
            "elapsed_time": elapsed,
            "estimated_remaining": elapsed / progress_pct - elapsed if progress_pct > 0 else None
        }
```

## Best Practices

### 1. Clear Step Definitions

```python
# Good - Specific and actionable
steps = [
    "Search for Python tutorials on web scraping",
    "Extract top 5 tutorial URLs",
    "Download content from each URL",
    "Summarize key concepts from tutorials"
]

# Bad - Vague and hard to execute
steps = [
    "Research Python",
    "Get information",
    "Process it"
]
```

### 2. Validation Steps

Always include verification steps:

```python
plan = [
    "Fetch data from API",
    "Validate data format",  # Validation
    "Transform data",
    "Verify transformation",  # Validation
    "Store in database",
    "Confirm storage success"  # Validation
]
```

### 3. Error Handling

Build error recovery into the plan:

```python
def create_plan_with_error_handling(task: str) -> List[Step]:
    plan = create_base_plan(task)
    
    # Add error handling steps
    enhanced_plan = []
    for step in plan:
        enhanced_plan.append(step)
        if step.is_critical:
            enhanced_plan.append(Step(
                f"Verify {step.description} completed successfully",
                depends_on=[step.id]
            ))
    
    return enhanced_plan
```

### 4. Resource Estimation

Estimate resources for each step:

```python
class Step:
    def __init__(self, description: str):
        self.description = description
        self.estimated_time = None
        self.estimated_cost = None
        self.required_tools = []
    
    def estimate_resources(self):
        """Estimate resources needed"""
        # Based on step complexity, tool requirements, etc.
        pass
```

## Comparison with ReAct

| Aspect | Plan-and-Execute | ReAct |
|--------|-----------------|-------|
| Planning | Upfront, comprehensive | None or minimal |
| Execution | Sequential, organized | Iterative, exploratory |
| Adaptability | Requires replanning | Naturally adaptive |
| Complexity | Better for complex tasks | Better for simple tasks |
| Observability | Clear progress tracking | Less structured |
| Token Usage | Potentially more efficient | Can be wasteful |
| Best For | Defined workflows | Exploration and discovery |

## Variations

### 1. Hierarchical Planning

Break complex plans into sub-plans:

```python
def hierarchical_plan(task: str) -> HierarchicalPlan:
    # Top-level plan
    high_level_plan = create_plan(task)
    
    # Expand each step into sub-steps
    detailed_plan = HierarchicalPlan()
    for step in high_level_plan:
        if step.is_complex:
            sub_plan = create_plan(step.description)
            detailed_plan.add(step, sub_plan)
        else:
            detailed_plan.add(step)
    
    return detailed_plan
```

### 2. Rolling Planning

Plan a few steps ahead, not everything:

```python
def rolling_plan(task: str, window_size: int = 3):
    """Plan only next N steps, replan as you go"""
    
    current_context = task
    all_results = []
    
    while not task_complete():
        # Plan next few steps
        next_steps = plan_next_steps(current_context, window_size)
        
        # Execute them
        for step in next_steps:
            result = execute_step(step)
            all_results.append(result)
            current_context = update_context(current_context, result)
    
    return all_results
```

### 3. Conditional Planning

Include conditional branches in plans:

```python
class ConditionalStep:
    def __init__(self, description: str, condition: Callable, 
                 on_true: List[Step], on_false: List[Step]):
        self.description = description
        self.condition = condition
        self.on_true = on_true
        self.on_false = on_false
    
    def execute(self, context):
        if self.condition(context):
            return execute_steps(self.on_true, context)
        else:
            return execute_steps(self.on_false, context)
```

## Common Pitfalls

### 1. Over-Planning
**Problem**: Spending too much time planning instead of executing
**Solution**: Set a time/token limit on planning phase

### 2. Rigid Plans
**Problem**: Not adapting when circumstances change
**Solution**: Implement dynamic replanning and monitoring

### 3. Unclear Steps
**Problem**: Steps that are too vague to execute
**Solution**: Enforce specific, actionable step descriptions

### 4. No Error Recovery
**Problem**: Plan fails at first error
**Solution**: Build in validation and recovery steps

## Example Use Case: Research Report

```python
# Task: Create a research report on AI safety

# Phase 1: Plan
plan = [
    "Search for recent AI safety papers (last 2 years)",
    "Extract key themes from top 10 papers",
    "Identify main researchers and organizations",
    "Analyze trends and emerging concerns",
    "Structure report outline",
    "Write introduction section",
    "Write findings section",
    "Write conclusion section",
    "Review and edit final report",
    "Format and export as PDF"
]

# Phase 2: Execute
for step in plan:
    result = execute(step)
    log_progress(step, result)
    
    if needs_more_research(result):
        plan.insert(current_step + 1, 
                   "Conduct additional research on [topic]")

# Phase 3: Deliver
return final_report
```

## Monitoring and Metrics

Track these metrics:

```python
class PlanMetrics:
    def __init__(self):
        self.steps_planned = 0
        self.steps_completed = 0
        self.steps_failed = 0
        self.replans_needed = 0
        self.total_time = 0
        self.tokens_used = 0
    
    def report(self):
        return {
            "success_rate": self.steps_completed / self.steps_planned,
            "replan_rate": self.replans_needed / self.steps_planned,
            "avg_time_per_step": self.total_time / self.steps_completed,
            "total_cost": estimate_cost(self.tokens_used)
        }
```

## Resources

- [Example Implementation](../../examples/planning/plan_and_execute.py)
- [LangChain Plan-and-Execute Agent](https://python.langchain.com/docs/use_cases/plan_and_execute)
- [ReAct Pattern](./react-pattern.md) for comparison
- [Best Practices](../theory/best-practices.md)
