"""
Hierarchical Multi-Agent System

This example demonstrates a manager-worker pattern where:
- A manager agent receives tasks and delegates to specialized workers
- Worker agents have specific expertise (research, analysis, writing)
- The manager coordinates workers and synthesizes final results

Pattern: Manager → Worker1, Worker2, Worker3 → Manager → Final Result
"""

from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain.tools import Tool
from dotenv import load_dotenv
import operator
import os

load_dotenv()


# Define state for multi-agent system
class AgentState(TypedDict):
    """State shared between agents"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    task: str
    research_results: str
    analysis_results: str
    writing_results: str
    final_output: str
    next_agent: str


# Simulated tools for different agents
def web_search(query: str) -> str:
    """Simulated web search for research"""
    knowledge_base = {
        "artificial intelligence": "AI is transforming industries with machine learning, NLP, and computer vision.",
        "climate change": "Climate change involves rising global temperatures and environmental impacts.",
        "quantum computing": "Quantum computers use qubits to solve complex problems faster than classical computers.",
        "blockchain": "Blockchain is a distributed ledger technology enabling secure, transparent transactions.",
    }
    
    for key in knowledge_base:
        if key in query.lower():
            return f"Research finding: {knowledge_base[key]}"
    
    return f"Research finding: General information about {query}"


def analyze_data(data: str) -> str:
    """Analyze data and extract insights"""
    return f"Analysis: The data shows important patterns and trends. Key insight: {data[:100]}..."


def sentiment_analysis(text: str) -> str:
    """Analyze sentiment of text"""
    positive_words = ["good", "great", "excellent", "positive", "beneficial"]
    if any(word in text.lower() for word in positive_words):
        return "Sentiment: Positive - The content has optimistic and constructive themes"
    return "Sentiment: Neutral - The content presents factual information"


def generate_summary(content: str) -> str:
    """Generate a summary"""
    return f"Summary: {content[:150]}... [Content summarized]"


# Create specialized worker agents
class ResearchAgent:
    """Specialized agent for research tasks"""
    
    def __init__(self):
        self.tools = [
            Tool(
                name="WebSearch",
                func=web_search,
                description="Search for information on a topic"
            )
        ]
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    def research(self, topic: str) -> str:
        """Conduct research on a topic"""
        print(f"\n🔬 Research Agent: Investigating '{topic}'...")
        
        # Simple research simulation
        result = web_search(topic)
        return f"Research completed on '{topic}': {result}"


class AnalysisAgent:
    """Specialized agent for data analysis"""
    
    def __init__(self):
        self.tools = [
            Tool(
                name="AnalyzeData",
                func=analyze_data,
                description="Analyze data and extract insights"
            ),
            Tool(
                name="SentimentAnalysis",
                func=sentiment_analysis,
                description="Analyze sentiment of text"
            )
        ]
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    def analyze(self, data: str) -> str:
        """Analyze provided data"""
        print(f"\n📊 Analysis Agent: Analyzing data...")
        
        # Perform analysis
        insights = analyze_data(data)
        sentiment = sentiment_analysis(data)
        
        return f"Analysis complete: {insights}\n{sentiment}"


class WritingAgent:
    """Specialized agent for content creation"""
    
    def __init__(self):
        self.tools = [
            Tool(
                name="GenerateSummary",
                func=generate_summary,
                description="Generate a summary of content"
            )
        ]
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    
    def write(self, content: str) -> str:
        """Create written content based on inputs"""
        print(f"\n✍️ Writing Agent: Creating content...")
        
        summary = generate_summary(content)
        
        return f"""
📝 Written Report:

{summary}

This report synthesizes the research and analysis findings into a coherent narrative.
The content has been structured for clarity and impact.
"""


# Initialize worker agents
research_agent = ResearchAgent()
analysis_agent = AnalysisAgent()
writing_agent = WritingAgent()


# Define manager agent node
def manager_node(state: AgentState) -> AgentState:
    """Manager coordinates worker agents"""
    print("\n👔 Manager Agent: Coordinating task...")
    
    task = state["task"]
    messages = state["messages"]
    
    # Determine next step based on state
    if not state.get("research_results"):
        print("   → Delegating to Research Agent")
        state["next_agent"] = "research"
    elif not state.get("analysis_results"):
        print("   → Delegating to Analysis Agent")
        state["next_agent"] = "analysis"
    elif not state.get("writing_results"):
        print("   → Delegating to Writing Agent")
        state["next_agent"] = "writing"
    else:
        print("   → All workers complete, synthesizing final output")
        state["next_agent"] = "finalize"
    
    return state


def research_node(state: AgentState) -> AgentState:
    """Research agent node"""
    task = state["task"]
    result = research_agent.research(task)
    state["research_results"] = result
    state["next_agent"] = "manager"
    return state


def analysis_node(state: AgentState) -> AgentState:
    """Analysis agent node"""
    research_results = state["research_results"]
    result = analysis_agent.analyze(research_results)
    state["analysis_results"] = result
    state["next_agent"] = "manager"
    return state


def writing_node(state: AgentState) -> AgentState:
    """Writing agent node"""
    research = state["research_results"]
    analysis = state["analysis_results"]
    combined = f"{research}\n\n{analysis}"
    result = writing_agent.write(combined)
    state["writing_results"] = result
    state["next_agent"] = "manager"
    return state


def finalize_node(state: AgentState) -> AgentState:
    """Finalize and combine all results"""
    print("\n✅ Manager Agent: Finalizing results...")
    
    final_output = f"""
{'='*70}
FINAL REPORT
{'='*70}

Task: {state['task']}

{state['research_results']}

{state['analysis_results']}

{state['writing_results']}

{'='*70}
Report complete.
{'='*70}
"""
    
    state["final_output"] = final_output
    state["next_agent"] = "end"
    return state


def route_agent(state: AgentState) -> str:
    """Route to next agent based on state"""
    next_agent = state.get("next_agent", "manager")
    
    routing = {
        "manager": "manager",
        "research": "research",
        "analysis": "analysis",
        "writing": "writing",
        "finalize": "finalize",
        "end": END
    }
    
    return routing.get(next_agent, END)


def create_hierarchical_workflow():
    """Create the hierarchical multi-agent workflow"""
    
    # Create state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("manager", manager_node)
    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("writing", writing_node)
    workflow.add_node("finalize", finalize_node)
    
    # Set entry point
    workflow.set_entry_point("manager")
    
    # Add conditional edges from manager
    workflow.add_conditional_edges(
        "manager",
        route_agent,
        {
            "manager": "manager",
            "research": "research",
            "analysis": "analysis",
            "writing": "writing",
            "finalize": "finalize",
            END: END
        }
    )
    
    # Worker agents return to manager
    workflow.add_edge("research", "manager")
    workflow.add_edge("analysis", "manager")
    workflow.add_edge("writing", "manager")
    workflow.add_edge("finalize", END)
    
    return workflow.compile()


def main():
    """Demonstrate hierarchical multi-agent system"""
    print("=" * 70)
    print("Hierarchical Multi-Agent System Demo")
    print("=" * 70)
    
    # Create the workflow
    app = create_hierarchical_workflow()
    
    # Test cases
    tasks = [
        "Research artificial intelligence and create a report",
        "Investigate climate change impacts and provide analysis",
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\n\n{'='*70}")
        print(f"Task {i}: {task}")
        print('='*70)
        
        # Initialize state
        initial_state = AgentState(
            messages=[HumanMessage(content=task)],
            task=task,
            research_results="",
            analysis_results="",
            writing_results="",
            final_output="",
            next_agent="manager"
        )
        
        # Run the workflow
        result = app.invoke(initial_state)
        
        # Display final output
        print(result["final_output"])


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        print("Create a .env file with: OPENAI_API_KEY=your_key_here")
    else:
        main()
