"""
Agentic AI Practices - Main Demo Script

This script demonstrates various agentic AI patterns and examples.
Run different examples by providing command-line arguments.

Usage:
    python main.py                    # Show menu
    python main.py simple             # Run simple agent
    python main.py react              # Run ReAct pattern
    python main.py multi-agent        # Run multi-agent system
    python main.py planning           # Run planning agent
    python main.py tools              # Show tool definitions
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def show_menu():
    """Display available examples and resources"""
    print("=" * 70)
    print("Agentic AI Practices - Learning Resources")
    print("=" * 70)
    print("\n📚 Available Examples:\n")
    print("  1. simple        - Basic agent with tools")
    print("  2. react         - ReAct pattern (Reasoning + Acting)")
    print("  3. multi-agent   - Hierarchical multi-agent system")
    print("  4. planning      - Plan-and-Execute pattern")
    print("  5. tools         - Tool definition examples")
    print("\n📖 Documentation:\n")
    print("  - Theory: docs/theory/")
    print("  - Patterns: docs/design-patterns/")
    print("  - Quick Reference: QUICK_REFERENCE.md")
    print("\n💻 Usage:\n")
    print("  python main.py <example_name>")
    print("  python main.py simple")
    print("\n🔑 Setup:\n")
    print("  1. Create .env file with OPENAI_API_KEY")
    print("  2. Install: pip install langchain langgraph langchain-openai python-dotenv")
    print("  3. Run any example above")
    print("\n" + "=" * 70)


def run_simple_agent():
    """Run simple agent example"""
    print("\n🚀 Running Simple Agent Example...\n")
    from examples.basic import simple_agent
    simple_agent.main()


def run_react():
    """Run ReAct pattern example"""
    print("\n🚀 Running ReAct Pattern Example...\n")
    from examples.react_pattern import basic_react
    basic_react.main()


def run_multi_agent():
    """Run multi-agent example"""
    print("\n🚀 Running Multi-Agent System Example...\n")
    from examples.multi_agent import hierarchical
    hierarchical.main()


def run_planning():
    """Run planning agent example"""
    print("\n🚀 Running Plan-and-Execute Example...\n")
    from examples.planning import plan_and_execute
    plan_and_execute.main()


def show_tools():
    """Show tool definition examples"""
    print("\n🚀 Running Tool Definition Examples...\n")
    from examples.basic import tool_definition
    tool_definition.demonstrate_tools()


def main():
    """Main entry point"""
    
    # Check for command line arguments
    if len(sys.argv) < 2:
        show_menu()
        return
    
    command = sys.argv[1].lower()
    
    # Route to appropriate example
    examples = {
        'simple': run_simple_agent,
        'react': run_react,
        'multi-agent': run_multi_agent,
        'multiagent': run_multi_agent,
        'planning': run_planning,
        'plan': run_planning,
        'tools': show_tools,
        'tool': show_tools,
    }
    
    if command in ['help', '-h', '--help']:
        show_menu()
    elif command in examples:
        try:
            examples[command]()
        except ImportError as e:
            print(f"❌ Error importing example: {e}")
            print("Make sure all dependencies are installed:")
            print("pip install langchain langgraph langchain-openai python-dotenv")
        except Exception as e:
            print(f"❌ Error running example: {e}")
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python main.py' to see available examples")


if __name__ == "__main__":
    main()
