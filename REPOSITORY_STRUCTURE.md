# Azure AI Learning Modules - Repository Structure

## Overview
This repository contains hands-on labs and implementations for the Azure AI Engineer learning path, including enterprise business solutions. Each module is self-contained with documentation, source code, and configuration.

## Repository Structure

```
Azure-AI-Learning-Modules/
├── 04-Semantic-Kernel/          # AI agent with expense management
├── 05-Agent-Orchestration/      # Multi-agent collaboration system
├── 05-Custom-Entity-Extraction/ # NER for classified ads
├── 06-Translate-Text/           # Multi-language translation
├── 06-generative-ai/            # AI agent exercises
│   ├── 02-build-ai-agent/
│   ├── 03-Agent-Custom-Functions/
│   ├── 03b-build-multi-agent-solution/
│   └── 03c-use-agent-tools-with-mcp/
├── 07-Bicep-Infrastructure/     # IaC with Azure Bicep
├── 07-Speech/                   # Speech-to-text and TTS
├── 08-Speech-Translation/       # Multi-language speech translation
├── 09-Audio-Chat/               # Multimodal AI chat application
├── 09-Bicep-Conditions-Loops/   # Advanced Bicep features
├── 10-Bicep-Modules/           # Modular infrastructure
├── Azure-Business-Solutions/    # Enterprise AI solutions
│   ├── customer-service/        # Customer service platform
│   ├── financial-analysis/      # Financial intelligence system
│   ├── hr-automation/          # HR automation system
│   ├── sales-intelligence/     # Sales intelligence system
│   └── operations-optimization/ # Operations optimization system
├── LEARNING_PROGRESS.md        # Overall progress tracking
└── REPOSITORY_STRUCTURE.md     # This file
```

## Module Categories

### AI Language & Cognitive Services
- **05-Custom-Entity-Extraction**: Custom NER models for classified ads
- **06-Translate-Text**: 137-language translation service
- **07-Speech**: Speech-to-text and text-to-speech
- **08-Speech-Translation**: Real-time speech translation
- **09-Audio-Chat**: Multimodal chat with audio support

### AI Agents & Orchestration
- **04-Semantic-Kernel**: Expense management agent with plugins
- **05-Agent-Orchestration**: Multi-agent incident response system
- **06-generative-ai**: Collection of AI agent exercises
  - Basic agent implementation
  - Custom function calling
  - Multi-agent solutions
  - MCP tool integration

### Infrastructure as Code
- **07-Bicep-Infrastructure**: Basic to advanced Bicep templates
- **09-Bicep-Conditions-Loops**: Conditional deployments and loops
- **10-Bicep-Modules**: Modular infrastructure components

### Business Solutions
- **Azure-Business-Solutions**: Production-ready enterprise applications
  - Customer Service Platform (sentiment analysis, priority routing)
  - Financial Intelligence System (multi-agent analysis)
  - HR Automation System (recruitment, onboarding, performance)
  - Sales Intelligence System (lead scoring, forecasting)
  - Operations Optimization System (process improvement, resource allocation)

## Standard Module Structure
```
module-name/
├── README.md              # Module overview and instructions
├── src/                   # Source code implementations
│   ├── main.py           # Main application
│   └── utils.py          # Helper functions
├── data/                  # Sample data and test files
├── docs/                  # Additional documentation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
└── tests/                # Unit tests (where applicable)
```

## Key Files
- **LEARNING_PROGRESS.md**: Tracks completion status (54% complete - 13/24 modules)
- **REPOSITORY_STRUCTURE.md**: This file - repository organization
- **README.md**: Main repository overview
- **.gitignore**: Excludes sensitive files and build artifacts

## Environment Configuration
Each module includes `.env.example` showing required settings:
```bash
# Copy and configure
cp .env.example .env
# Edit .env with your Azure credentials
```

## Technology Stack
- **Languages**: Python 3.8+, JavaScript/TypeScript, .NET
- **Azure Services**: 
  - Azure OpenAI
  - Azure AI Services (Speech, Language, Translation)
  - Azure AI Foundry
  - Azure Bicep (IaC)
- **Frameworks**:
  - Semantic Kernel SDK
  - OpenAI Python SDK
  - Azure SDK libraries
- **Business Libraries**:
  - pandas, numpy (data analysis)
  - matplotlib, seaborn (visualization)
  - scikit-learn (ML utilities)

## Development Guidelines

### Best Practices
1. **Security**: Never commit credentials or `.env` files
2. **Isolation**: Use virtual environments for Python modules
3. **Documentation**: Include comprehensive READMEs
4. **Testing**: Add demo functions for easy testing
5. **Structure**: Follow existing module patterns

### Module Development
```bash
# Create new module
mkdir XX-Module-Name/{src,data,docs}
cd XX-Module-Name

# Set up Python environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### Testing
```bash
# Run module demos
python src/demo.py

# Run business solution tests
cd Azure-Business-Solutions
python test_solutions.py
```

## Progress Summary
- **Completed**: 13 modules (54%)
- **AI Agents**: 7 implementations
- **Business Solutions**: 5 enterprise applications
- **Infrastructure**: 3 Bicep modules
- **Total Code**: 10,000+ lines

## Next Steps
1. Complete remaining learning modules
2. Add unit tests to all modules
3. Create CI/CD pipelines
4. Deploy business solutions to Azure
5. Add monitoring and analytics

## Resources
- [Microsoft Learn - AI Engineer](https://learn.microsoft.com/training/paths/azure-ai-engineer/)
- [Azure AI Documentation](https://docs.microsoft.com/azure/cognitive-services/)
- [Semantic Kernel Docs](https://learn.microsoft.com/semantic-kernel/)
- [Azure Bicep Reference](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)

---
*Last Updated: 2025-07-30*