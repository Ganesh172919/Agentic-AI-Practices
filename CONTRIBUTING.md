# Contributing to Agentic AI Practices

Thank you for your interest in contributing! This guide will help you get started.

## Ways to Contribute

### 1. Add New Examples
Share your agentic AI implementations:
- Create a new Python file in the appropriate `examples/` subdirectory
- Include comprehensive comments and docstrings
- Add usage examples in the file
- Update `examples/README.md` with your example

### 2. Write Documentation
Help others learn:
- Add new design patterns to `docs/design-patterns/`
- Expand theory documentation in `docs/theory/`
- Create tutorials or guides
- Improve existing documentation

### 3. Improve Code
Enhance existing examples:
- Fix bugs
- Improve error handling
- Add more features
- Optimize performance

### 4. Report Issues
Found a problem?
- Check if it's already reported
- Provide clear description
- Include steps to reproduce
- Share error messages

## Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Agentic-AI-Practices.git
cd Agentic-AI-Practices
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

### 3. Make Changes
```bash
# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes
# Test your changes

# Commit
git add .
git commit -m "Description of changes"
```

### 4. Submit Pull Request
```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

## Code Standards

### Python Code
- Follow PEP 8 style guide
- Use type hints where appropriate
- Include docstrings for functions and classes
- Add comments for complex logic
- Keep functions focused and single-purpose

### Documentation
- Use clear, concise language
- Include code examples
- Add practical use cases
- Explain the "why" not just the "what"
- Use proper markdown formatting

### Example Structure
```python
"""
Module Name

Brief description of what this module does and when to use it.

Key Concepts:
1. Concept 1
2. Concept 2
"""

from typing import List, Dict
import other_modules


def example_function(param: str) -> str:
    """
    Brief description of function.
    
    Detailed explanation of what the function does,
    how it works, and when to use it.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    
    Example:
        >>> result = example_function("test")
        >>> print(result)
        "Result: test"
    """
    # Implementation with clear comments
    pass


if __name__ == "__main__":
    # Demonstration code
    pass
```

## Documentation Standards

### Theory Documents
- Start with clear overview
- Define key concepts
- Provide examples
- Include use cases
- Link to related resources

### Design Pattern Documents
- Pattern name and alias
- Problem it solves
- When to use (and when not to)
- Implementation example
- Best practices
- Common pitfalls
- Real-world examples

### README Files
- Clear title and description
- Quick start guide
- Usage examples
- Links to detailed docs
- Contribution guidelines

## Testing Guidelines

### Before Submitting
- [ ] Code runs without errors
- [ ] All examples have been tested
- [ ] Documentation is clear and accurate
- [ ] No sensitive data (API keys, etc.)
- [ ] Follows existing code style
- [ ] Added to appropriate README files

### Testing Your Code
```bash
# Test Python syntax
python -m py_compile your_file.py

# Run your example
python your_file.py

# Check for common issues
pylint your_file.py  # Optional
```

## Content Guidelines

### Adding Examples

**Good Example:**
```python
"""
Clear Title

What this example demonstrates and why it's useful.

Prerequisites:
- List required knowledge
- List required packages

Key Concepts:
1. First concept
2. Second concept
"""

# Clear, commented code
# Demonstrates best practices
# Includes error handling
```

**Avoid:**
- Overly complex examples
- Undocumented code
- Examples requiring special setup
- Deprecated patterns

### Adding Documentation

**Good Documentation:**
- Clear hierarchy (headers)
- Code examples with explanations
- Practical use cases
- Links to related content
- Visual aids (when helpful)

**Avoid:**
- Walls of text
- Jargon without explanation
- Outdated information
- Broken links

## Review Process

### What We Look For
1. **Accuracy**: Information is correct and up-to-date
2. **Clarity**: Easy to understand for target audience
3. **Completeness**: All necessary information included
4. **Consistency**: Matches existing style and structure
5. **Value**: Adds meaningful content

### Response Time
- Initial review: Within 1 week
- Follow-up: Within 3 days
- We'll provide feedback and suggestions

## Questions?

- Open an issue for questions
- Tag with "question" label
- Be specific about what you need help with

## Code of Conduct

### Be Respectful
- Treat others with kindness
- Accept constructive criticism
- Focus on what's best for the community

### Be Collaborative
- Help others learn
- Share knowledge
- Give credit where due

### Be Professional
- Keep discussions on-topic
- No spam or self-promotion
- Follow GitHub's Terms of Service

## Recognition

Contributors will be:
- Listed in commit history
- Credited in documentation (if desired)
- Mentioned in release notes

## Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## License

By contributing, you agree that your contributions will be available under the same license as the project.

---

**Thank you for contributing to Agentic AI Practices! 🚀**
