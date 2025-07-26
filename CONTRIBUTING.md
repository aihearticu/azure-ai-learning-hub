# Contributing to Azure AI Learning Hub

Thank you for your interest in contributing to the Azure AI Learning Hub! This guide will help you get started.

## 🤝 How to Contribute

### 1. Types of Contributions

We welcome various types of contributions:

- **New Labs**: Add new hands-on labs for Azure AI services
- **Improvements**: Enhance existing labs with better explanations or code
- **Bug Fixes**: Fix issues in code samples or documentation
- **Translations**: Help translate labs to other languages
- **Examples**: Add real-world use cases and examples

### 2. Getting Started

1. **Fork the repository**
   ```bash
   # Fork via GitHub UI, then clone
   git clone https://github.com/YOUR-USERNAME/azure-ai-learning-hub.git
   cd azure-ai-learning-hub
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Test your code thoroughly
   - Update documentation as needed

### 3. Lab Template

When creating new labs, use this structure:

```
XX-service-name/
├── lab-name/
│   ├── README.md           # Lab overview and objectives
│   ├── setup.md           # Detailed setup instructions
│   ├── lab-instructions.md # Step-by-step guide
│   ├── src/               # Source code
│   │   ├── python/       # Python implementation
│   │   └── dotnet/       # .NET implementation (optional)
│   ├── tests/            # Test files
│   ├── images/           # Screenshots and diagrams
│   └── cleanup.md        # Resource cleanup instructions
```

### 4. Code Standards

#### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Include docstrings for functions
- Handle exceptions gracefully

```python
def analyze_text(text: str, api_key: str) -> dict:
    """
    Analyze text using Azure Text Analytics.
    
    Args:
        text: The text to analyze
        api_key: Azure API key
        
    Returns:
        Dictionary containing analysis results
    """
    # Implementation
```

#### Documentation
- Use clear, concise language
- Include code snippets with syntax highlighting
- Add screenshots for UI-based steps
- Provide troubleshooting sections

### 5. Commit Guidelines

- Use clear, descriptive commit messages
- Follow conventional commits format:
  ```
  feat: add speech-to-text lab
  fix: correct API endpoint in vision lab
  docs: update setup instructions
  refactor: improve error handling
  ```

### 6. Pull Request Process

1. **Before submitting**:
   - Test all code samples
   - Run linters and fix issues
   - Update relevant documentation
   - Add yourself to CONTRIBUTORS.md

2. **Submit PR**:
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots if applicable
   - Ensure all checks pass

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] New lab
   - [ ] Bug fix
   - [ ] Documentation update
   - [ ] Code improvement

   ## Testing
   - [ ] Code tested locally
   - [ ] Documentation reviewed
   - [ ] Screenshots added (if applicable)

   ## Checklist
   - [ ] Follows code standards
   - [ ] Includes error handling
   - [ ] Documentation updated
   - [ ] No hardcoded credentials
   ```

### 7. Review Process

- PRs are reviewed within 3-5 business days
- Address reviewer feedback promptly
- Once approved, PRs are merged to main

## 📋 Development Guidelines

### Security
- Never commit API keys or credentials
- Use environment variables for sensitive data
- Follow Azure security best practices
- Include security considerations in labs

### Testing
- Test with different Azure regions
- Verify free tier compatibility
- Test error scenarios
- Include cleanup verification

### Documentation
- Explain concepts before implementation
- Include prerequisites clearly
- Provide estimated completion time
- Add links to official docs

## 🚀 Setting Up Development Environment

1. **Install prerequisites**:
   ```bash
   # Python development
   python -m pip install -r requirements-dev.txt
   
   # Pre-commit hooks
   pre-commit install
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Add your Azure credentials for testing
   ```

3. **Run tests**:
   ```bash
   python -m pytest tests/
   ```

## 💡 Ideas for Contributions

Looking for ideas? Check out:
- [Open Issues](https://github.com/AIHeartICU/azure-ai-learning-hub/issues)
- [Requested Features](https://github.com/AIHeartICU/azure-ai-learning-hub/discussions/categories/ideas)
- Gaps in current documentation
- New Azure AI services without labs

## 📞 Getting Help

- **Questions**: Open a [Discussion](https://github.com/AIHeartICU/azure-ai-learning-hub/discussions)
- **Bugs**: Create an [Issue](https://github.com/AIHeartICU/azure-ai-learning-hub/issues)
- **Security**: Email security concerns privately

## 🏆 Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- GitHub contributors page
- Special badges for significant contributions

## 📜 Code of Conduct

Please follow our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

Thank you for helping make Azure AI learning accessible to everyone! 🚀