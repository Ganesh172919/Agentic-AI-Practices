"""
Simple Agent Example

This example demonstrates the basics of creating an agentic AI system:
- Defining tools for the agent to use
- Creating an agent with a language model
- Running the agent with a task

Key Concepts:
1. Tools: Functions the agent can call
2. Agent: The decision-making entity
3. Executor: Manages the agent execution loop
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: A mathematical expression like "2 + 2" or "10 * 5"
    
    Returns:
        The result of the calculation
    
    Example:
        calculator("2 + 2") -> "4"
    """
    try:
        # WARNING: eval() is dangerous in production - use a safe math parser
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


def get_word_length(word: str) -> str:
    """
    Get the length of a word.
    
    Args:
        word: A word or string
    
    Returns:
        The number of characters in the word
    
    Example:
        get_word_length("hello") -> "The word 'hello' has 5 letters"
    """
    length = len(word.strip())
    return f"The word '{word}' has {length} letters"


def reverse_string(text: str) -> str:
    """
    Reverse a string.
    
    Args:
        text: A string to reverse
    
    Returns:
        The reversed string
    
    Example:
        reverse_string("hello") -> "olleh"
    """
    reversed_text = text[::-1]
    return f"Reversed: {reversed_text}"


# Define tools for the agent
tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for mathematical calculations. Input should be a mathematical expression like '2 + 2' or '10 * 5'."
    ),
    Tool(
        name="WordLength",
        func=get_word_length,
        description="Returns the length of a word or string. Input should be a single word or phrase."
    ),
    Tool(
        name="ReverseString",
        func=reverse_string,
        description="Reverses a string. Input should be the text to reverse."
    )
]


# Create prompt template for ReAct agent
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)


def create_simple_agent():
    """
    Create a simple ReAct agent with basic tools.
    
    Returns:
        AgentExecutor instance ready to process tasks
    """
    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,  # More deterministic
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create executor to manage agent execution
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,  # Show reasoning steps
        max_iterations=10,  # Prevent infinite loops
        handle_parsing_errors=True  # Gracefully handle errors
    )
    
    return agent_executor


def main():
    """
    Main function demonstrating agent usage with various tasks.
    """
    print("=" * 60)
    print("Simple Agent Example")
    print("=" * 60)
    
    # Create the agent
    agent = create_simple_agent()
    
    # Example 1: Simple calculation
    print("\n📝 Example 1: Mathematical Calculation")
    print("-" * 60)
    question1 = "What is 15 multiplied by 8?"
    result1 = agent.invoke({"input": question1})
    print(f"\n✅ Result: {result1['output']}\n")
    
    # Example 2: String manipulation
    print("\n📝 Example 2: String Operations")
    print("-" * 60)
    question2 = "How many letters are in the word 'artificial'?"
    result2 = agent.invoke({"input": question2})
    print(f"\n✅ Result: {result2['output']}\n")
    
    # Example 3: Multi-step task
    print("\n📝 Example 3: Multi-step Task")
    print("-" * 60)
    question3 = "What is the reverse of the word 'hello' and how many letters does it have?"
    result3 = agent.invoke({"input": question3})
    print(f"\n✅ Result: {result3['output']}\n")
    
    # Example 4: Complex reasoning
    print("\n📝 Example 4: Complex Reasoning")
    print("-" * 60)
    question4 = "Calculate (25 + 15) * 2, then tell me if the result has more or less than 5 digits"
    result4 = agent.invoke({"input": question4})
    print(f"\n✅ Result: {result4['output']}\n")
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_key_here")
    else:
        main()
