"""
Basic ReAct Pattern Implementation

This example demonstrates the ReAct (Reasoning + Acting) pattern:
- Alternating between reasoning and action
- Using tools based on reasoning
- Iterative problem-solving approach

ReAct Flow:
1. Thought: Agent reasons about the problem
2. Action: Agent takes an action using a tool
3. Observation: Agent receives feedback
4. Repeat until solution found
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


# Simulated tool implementations
class MockDatabase:
    """Simulated database for demonstration"""
    
    def __init__(self):
        self.data = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
                {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25},
                {"id": 3, "name": "Charlie", "email": "charlie@example.com", "age": 35},
            ],
            "orders": [
                {"id": 101, "user_id": 1, "product": "Laptop", "price": 1200},
                {"id": 102, "user_id": 2, "product": "Mouse", "price": 25},
                {"id": 103, "user_id": 1, "product": "Keyboard", "price": 75},
            ]
        }
    
    def query(self, table: str, condition: str = None) -> str:
        """Query the database"""
        if table not in self.data:
            return f"Table '{table}' not found. Available tables: {list(self.data.keys())}"
        
        results = self.data[table]
        
        if condition:
            # Simple condition parsing (for demo purposes)
            results = [r for r in results if self._matches_condition(r, condition)]
        
        return str(results) if results else "No results found"
    
    def _matches_condition(self, record: dict, condition: str) -> bool:
        """Simple condition matcher"""
        # Very basic implementation for demo
        if ">" in condition:
            key, value = condition.split(">")
            return record.get(key.strip()) > int(value.strip())
        elif "=" in condition:
            key, value = condition.split("=")
            return str(record.get(key.strip())) == value.strip().strip("'\"")
        return True


# Initialize mock database
db = MockDatabase()


def search_web(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: Search query string
    
    Returns:
        Simulated search results
    """
    # Simulated search results
    results = {
        "python": "Python is a high-level programming language known for readability and versatility.",
        "react": "React is a JavaScript library for building user interfaces, maintained by Facebook.",
        "ai": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "weather": f"Current weather: Sunny, 22°C (Simulated data for {datetime.now().strftime('%Y-%m-%d')})",
    }
    
    # Find relevant result
    query_lower = query.lower()
    for key, value in results.items():
        if key in query_lower:
            return value
    
    return f"No specific results found for '{query}'. This is a simulated search."


def query_database(query: str) -> str:
    """
    Query the database with natural language.
    
    Args:
        query: Natural language query like "find all users" or "get orders for user_id=1"
    
    Returns:
        Query results
    """
    query_lower = query.lower()
    
    # Parse query
    if "users" in query_lower:
        if "age" in query_lower and ">" in query_lower:
            age = query_lower.split(">")[1].strip().split()[0]
            return db.query("users", f"age>{age}")
        return db.query("users")
    elif "orders" in query_lower:
        if "user_id" in query_lower:
            # Extract user_id
            parts = query_lower.split("user_id")
            if len(parts) > 1:
                user_id = parts[1].strip().split()[0].replace("=", "").replace(":", "")
                return db.query("orders", f"user_id={user_id}")
        return db.query("orders")
    
    return "Could not parse query. Try: 'find all users' or 'get orders for user_id=1'"


def calculate(expression: str) -> str:
    """
    Perform mathematical calculations.
    
    Args:
        expression: Mathematical expression to evaluate
    
    Returns:
        Calculation result
    """
    try:
        result = eval(expression)  # WARNING: Don't use in production!
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


# Define tools
tools = [
    Tool(
        name="SearchWeb",
        func=search_web,
        description="Search the web for information. Input should be a search query string. Useful for finding general information about topics."
    ),
    Tool(
        name="QueryDatabase",
        func=query_database,
        description="Query the database. Input should be a natural language query like 'find all users' or 'get orders for user_id=1'. Returns database records."
    ),
    Tool(
        name="Calculate",
        func=calculate,
        description="Perform mathematical calculations. Input should be a mathematical expression like '2 + 2' or '(100 - 20) * 1.5'."
    )
]


# ReAct prompt template
react_prompt = """You are a helpful assistant that uses tools to answer questions.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: think about what you need to do step by step
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Important:
- Always think step by step
- Use tools when you need information
- Combine information from multiple tools if needed
- Be specific in your final answer

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


def create_react_agent_executor():
    """Create a ReAct agent with tools."""
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    prompt = PromptTemplate.from_template(react_prompt)
    agent = create_react_agent(llm, tools, prompt)
    
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    return executor


def main():
    """Demonstrate ReAct pattern with various examples."""
    print("=" * 70)
    print("ReAct Pattern Example")
    print("=" * 70)
    
    agent = create_react_agent_executor()
    
    # Example 1: Simple information retrieval
    print("\n🔍 Example 1: Information Retrieval")
    print("-" * 70)
    result1 = agent.invoke({"input": "What is Python?"})
    print(f"\n✅ Answer: {result1['output']}\n")
    
    # Example 2: Database query
    print("\n🔍 Example 2: Database Query")
    print("-" * 70)
    result2 = agent.invoke({"input": "Find all users in the database"})
    print(f"\n✅ Answer: {result2['output']}\n")
    
    # Example 3: Multi-step reasoning with calculation
    print("\n🔍 Example 3: Multi-step Task")
    print("-" * 70)
    result3 = agent.invoke({
        "input": "Find all orders in the database and calculate the total price"
    })
    print(f"\n✅ Answer: {result3['output']}\n")
    
    # Example 4: Complex reasoning combining multiple tools
    print("\n🔍 Example 4: Complex Multi-tool Task")
    print("-" * 70)
    result4 = agent.invoke({
        "input": "How many users are in the database, and what percentage are over 30 years old?"
    })
    print(f"\n✅ Answer: {result4['output']}\n")
    
    print("=" * 70)
    print("ReAct Pattern Examples Completed!")
    print("=" * 70)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        print("Create a .env file with: OPENAI_API_KEY=your_key_here")
    else:
        main()
