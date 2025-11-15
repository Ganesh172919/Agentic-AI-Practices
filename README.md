# Agentic AI Practices

A comprehensive learning resource for Agentic AI, including theory, design patterns, and practical code examples.

## 📚 What's Inside

This repository provides a complete learning path for understanding and implementing agentic AI systems:

### 🎓 Theory & Concepts
- **[Introduction to Agentic AI](docs/theory/introduction-to-agentic-ai.md)** - Core concepts and fundamentals
- **[Best Practices](docs/theory/best-practices.md)** - Production-ready guidelines and patterns

### 🏗️ Design Patterns
- **[Pattern Overview](docs/design-patterns/overview.md)** - Catalog of agentic AI patterns
- **[ReAct Pattern](docs/design-patterns/react-pattern.md)** - Reasoning + Acting pattern
- **More patterns** - Plan-and-Execute, Multi-Agent, Memory patterns, and more

### 💻 Code Examples
- **[Basic Examples](examples/basic/)** - Get started with simple agents
- **[ReAct Implementation](examples/react-pattern/)** - Practical ReAct pattern examples
- **[Multi-Agent Systems](examples/multi-agent/)** - Coordinating multiple agents
- **[Tool Use Patterns](examples/tool-use/)** - Advanced tool integration
- **[Planning Agents](examples/planning/)** - Agents that plan before executing

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.11 or higher
python --version

# Install dependencies
pip install langchain langgraph langchain-openai python-dotenv

# Or use uv (faster)
uv pip install langchain langgraph langchain-openai python-dotenv
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Ganesh172919/Agentic-AI-Practices.git
cd Agentic-AI-Practices
```

2. Create a `.env` file with your API key:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

3. Run your first agent:
```bash
python examples/basic/simple_agent.py
```

## 📖 Learning Path

### Beginner Track
1. **Understand the Basics**
   - Read [Introduction to Agentic AI](docs/theory/introduction-to-agentic-ai.md)
   - Study the [Pattern Overview](docs/design-patterns/overview.md)

2. **First Code**
   - Run [Simple Agent](examples/basic/simple_agent.py)
   - Understand tool definitions and agent loops

3. **Core Pattern**
   - Learn [ReAct Pattern](docs/design-patterns/react-pattern.md)
   - Try [Basic ReAct Example](examples/react-pattern/basic_react.py)

### Intermediate Track
1. **Advanced Patterns**
   - Explore Plan-and-Execute pattern
   - Understand memory-augmented agents
   - Study tool composition

2. **Multi-Agent Systems**
   - Learn agent coordination patterns
   - Try [Hierarchical Multi-Agent](examples/multi-agent/hierarchical.py)
   - Understand agent communication

3. **Best Practices**
   - Read [Best Practices Guide](docs/theory/best-practices.md)
   - Implement error handling
   - Add logging and monitoring

### Advanced Track
1. **Production Systems**
   - Implement safety measures
   - Add human-in-the-loop
   - Optimize performance and costs

2. **Custom Implementations**
   - Build domain-specific agents
   - Create custom tool ecosystems
   - Design complex workflows

## 🎯 Key Concepts

### What is Agentic AI?
Agentic AI systems can autonomously achieve goals through:
- **Reasoning**: Thinking step-by-step about problems
- **Planning**: Breaking down complex tasks
- **Tool Use**: Interacting with external systems
- **Memory**: Learning from past interactions
- **Adaptation**: Adjusting strategies based on feedback

### Core Components
- **Agent**: The decision-making entity
- **Tools**: Functions the agent can call
- **Environment**: Context where the agent operates
- **Memory**: Short-term and long-term storage
- **Executor**: Manages the agent execution loop

### Common Patterns
1. **ReAct** - Alternating reasoning and action
2. **Plan-and-Execute** - Strategic upfront planning
3. **Multi-Agent** - Specialized agents collaborating
4. **Reflection** - Self-critique and improvement
5. **Memory-Augmented** - Learning from history

## 📁 Repository Structure

```
Agentic-AI-Practices/
├── docs/
│   ├── theory/              # Conceptual documentation
│   │   ├── introduction-to-agentic-ai.md
│   │   └── best-practices.md
│   └── design-patterns/     # Pattern documentation
│       ├── overview.md
│       └── react-pattern.md
├── examples/
│   ├── basic/               # Foundational examples
│   ├── react-pattern/       # ReAct implementations
│   ├── multi-agent/         # Multi-agent systems
│   ├── tool-use/            # Advanced tool patterns
│   └── planning/            # Planning agents
├── main.py                  # Main application
└── README.md               # This file
```

## 🛠️ Technologies Used

- **LangChain** - Framework for LLM applications
- **LangGraph** - Library for building stateful agents
- **OpenAI** - LLM provider (GPT-4, GPT-3.5)
- **Python 3.11+** - Programming language

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-pattern`
3. Add your content (documentation or examples)
4. Follow existing structure and style
5. Test your code examples
6. Submit a pull request

### Contribution Guidelines
- Maintain consistent formatting
- Include clear documentation
- Add practical examples
- Follow best practices from the guide
- Test all code before submitting

## 📚 Additional Resources

### Papers & Articles
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Constitutional AI](https://arxiv.org/abs/2212.08073)

### Frameworks & Tools
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

### Community
- [LangChain Discord](https://discord.gg/langchain)
- [AI Agent Research](https://github.com/topics/ai-agents)

## 🔒 Safety & Ethics

When building agentic AI systems:
- ✅ Set clear boundaries and limits
- ✅ Implement human oversight for critical decisions
- ✅ Validate all tool executions
- ✅ Monitor and log all agent actions
- ✅ Test thoroughly before production
- ❌ Never allow unrestricted system access
- ❌ Don't ignore potential misuse scenarios

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

Built with inspiration from:
- The LangChain community
- OpenAI's research on agents
- Academic research in autonomous AI systems

## 📧 Contact

For questions or suggestions:
- Open an issue on GitHub
- Contribute improvements via pull requests

---

**Start Learning:** Begin with [Introduction to Agentic AI](docs/theory/introduction-to-agentic-ai.md) 🚀
