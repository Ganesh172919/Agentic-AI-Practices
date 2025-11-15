"""
Plan-and-Execute Pattern

This example demonstrates the plan-and-execute pattern where:
1. Planning Phase: Agent creates a detailed plan
2. Execution Phase: Agent executes each step
3. Monitoring Phase: Agent tracks progress and adapts

This pattern is ideal for complex, well-defined tasks that benefit from upfront planning.
"""

from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import json

load_dotenv()


class PlanAndExecuteAgent:
    """Agent that plans before executing"""
    
    def __init__(self, llm):
        self.llm = llm
        self.current_plan = []
        self.execution_log = []
        
    def create_plan(self, task: str) -> List[Dict[str, str]]:
        """
        Create a step-by-step plan for the task.
        
        Args:
            task: The high-level task to accomplish
            
        Returns:
            List of steps with descriptions
        """
        planning_prompt = f"""Create a detailed step-by-step plan to accomplish this task:

Task: {task}

Requirements:
1. Break down the task into clear, actionable steps
2. Each step should be specific and measurable
3. Steps should be in logical order
4. Include validation/checking steps

Return the plan as a JSON list where each step has:
- step_number: int
- description: string
- estimated_complexity: "low", "medium", or "high"

Example format:
[
  {{"step_number": 1, "description": "Research topic X", "estimated_complexity": "medium"}},
  {{"step_number": 2, "description": "Analyze findings", "estimated_complexity": "low"}}
]

Plan:"""

        response = self.llm.invoke(planning_prompt)
        
        try:
            # Extract JSON from response
            content = response.content
            # Find JSON array in response
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end > start:
                plan_json = content[start:end]
                plan = json.loads(plan_json)
                self.current_plan = plan
                return plan
            else:
                # Fallback to simple parsing
                return self._create_fallback_plan(task)
        except Exception as e:
            print(f"Error parsing plan: {e}")
            return self._create_fallback_plan(task)
    
    def _create_fallback_plan(self, task: str) -> List[Dict[str, str]]:
        """Create a simple fallback plan"""
        return [
            {"step_number": 1, "description": f"Understand: {task}", "estimated_complexity": "low"},
            {"step_number": 2, "description": "Gather required information", "estimated_complexity": "medium"},
            {"step_number": 3, "description": "Execute main task", "estimated_complexity": "high"},
            {"step_number": 4, "description": "Verify results", "estimated_complexity": "low"}
        ]
    
    def execute_step(self, step: Dict[str, str], context: str = "") -> Dict[str, Any]:
        """
        Execute a single step from the plan.
        
        Args:
            step: The step to execute
            context: Context from previous steps
            
        Returns:
            Execution result with status and output
        """
        print(f"\n🔧 Executing Step {step['step_number']}: {step['description']}")
        
        execution_prompt = f"""Execute this step:

Step: {step['description']}
Complexity: {step['estimated_complexity']}

Context from previous steps:
{context}

Provide:
1. What you did
2. The result
3. Any issues encountered
4. Whether this step is complete

Response:"""

        response = self.llm.invoke(execution_prompt)
        
        result = {
            "step_number": step["step_number"],
            "description": step["description"],
            "output": response.content,
            "status": "completed",
            "timestamp": "now"
        }
        
        self.execution_log.append(result)
        
        print(f"   ✅ Completed: {step['description'][:60]}...")
        
        return result
    
    def monitor_progress(self) -> Dict[str, Any]:
        """
        Monitor execution progress and adapt if needed.
        
        Returns:
            Progress report
        """
        total_steps = len(self.current_plan)
        completed_steps = len(self.execution_log)
        
        progress = {
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "progress_percentage": (completed_steps / total_steps * 100) if total_steps > 0 else 0,
            "remaining_steps": total_steps - completed_steps
        }
        
        return progress
    
    def should_replan(self, last_result: Dict[str, Any]) -> bool:
        """
        Decide if replanning is needed based on execution results.
        
        Args:
            last_result: Result of the last executed step
            
        Returns:
            True if replanning is needed
        """
        # Simple heuristic: check if the last step failed
        if "error" in last_result.get("output", "").lower():
            return True
        if "failed" in last_result.get("output", "").lower():
            return True
        return False
    
    def run(self, task: str) -> Dict[str, Any]:
        """
        Execute the complete plan-and-execute cycle.
        
        Args:
            task: The task to accomplish
            
        Returns:
            Final results
        """
        print("=" * 70)
        print("PLAN-AND-EXECUTE AGENT")
        print("=" * 70)
        print(f"\n📋 Task: {task}\n")
        
        # Phase 1: Planning
        print("=" * 70)
        print("PHASE 1: PLANNING")
        print("=" * 70)
        
        plan = self.create_plan(task)
        
        print(f"\n📝 Created plan with {len(plan)} steps:")
        for step in plan:
            complexity_emoji = {
                "low": "🟢",
                "medium": "🟡",
                "high": "🔴"
            }
            emoji = complexity_emoji.get(step.get("estimated_complexity", "medium"), "⚪")
            print(f"   {emoji} Step {step['step_number']}: {step['description']}")
        
        # Phase 2: Execution
        print("\n" + "=" * 70)
        print("PHASE 2: EXECUTION")
        print("=" * 70)
        
        context = f"Task: {task}\n\n"
        
        for step in plan:
            # Execute step
            result = self.execute_step(step, context)
            
            # Update context
            context += f"Step {step['step_number']}: {result['output'][:200]}...\n\n"
            
            # Monitor progress
            progress = self.monitor_progress()
            print(f"   📊 Progress: {progress['completed_steps']}/{progress['total_steps']} steps ({progress['progress_percentage']:.0f}%)")
            
            # Check if replanning needed (simplified)
            if self.should_replan(result):
                print("   ⚠️  Replanning needed due to issues...")
                # In a real implementation, would replan here
        
        # Phase 3: Summary
        print("\n" + "=" * 70)
        print("PHASE 3: SUMMARY")
        print("=" * 70)
        
        final_result = {
            "task": task,
            "plan": plan,
            "execution_log": self.execution_log,
            "progress": self.monitor_progress(),
            "status": "completed"
        }
        
        print(f"\n✅ Task completed!")
        print(f"   Total steps executed: {len(self.execution_log)}")
        print(f"   Success rate: {progress['progress_percentage']:.0f}%")
        
        return final_result


# Tool functions for the agent to use
def research_topic(topic: str) -> str:
    """Simulate research on a topic"""
    knowledge = {
        "machine learning": "ML involves algorithms that improve through experience",
        "neural networks": "Neural networks are computing systems inspired by biological neural networks",
        "climate": "Climate patterns show significant changes in recent decades"
    }
    
    for key in knowledge:
        if key in topic.lower():
            return knowledge[key]
    
    return f"Research findings on {topic}"


def analyze_data(data: str) -> str:
    """Simulate data analysis"""
    return f"Analysis of data reveals key patterns and insights: {data[:100]}..."


def generate_report(content: str) -> str:
    """Generate a report from content"""
    return f"Report generated with {len(content)} characters of content"


def main():
    """Demonstrate plan-and-execute pattern"""
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create agent
    agent = PlanAndExecuteAgent(llm)
    
    # Test tasks
    tasks = [
        "Research machine learning fundamentals and create a beginner's guide",
        "Analyze climate data trends and prepare a summary report",
        "Design a simple web application architecture for an e-commerce site"
    ]
    
    for i, task in enumerate(tasks, 1):
        if i > 1:
            print("\n\n" + "=" * 70)
            print(f"NEW TASK {i}")
            print("=" * 70 + "\n")
        
        result = agent.run(task)
        
        # Reset for next task
        agent.execution_log = []
        agent.current_plan = []


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        print("Create a .env file with: OPENAI_API_KEY=your_key_here")
    else:
        main()
