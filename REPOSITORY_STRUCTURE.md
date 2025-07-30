# Azure AI Learning Hub - Repository Structure

## Overview
This repository contains hands-on labs and implementations for the Azure AI Engineer learning path. Each module is self-contained with its own documentation, source code, and configuration.

## Directory Structure

```
Azure-AI-Learning-Modules/
├── 01-fundamentals/              # Azure AI fundamentals (pending)
├── 02-computer-vision/           # Computer Vision services (pending)
├── 03-natural-language/          # Natural Language Processing
│   ├── 05-Custom-Entity-Extraction/
│   ├── 06-Translate-Text/
│   ├── 07-Speech-Service/
│   └── 08-Speech-Translation/
├── 04-Semantic-Kernel/           # AI Agent with Semantic Kernel SDK
│   ├── src/                      # Source code
│   ├── docs/                     # Documentation
│   └── data/                     # Sample data
├── 04-knowledge-mining/          # Cognitive Search labs
├── 05-Agent-Orchestration/       # Multi-agent systems
│   ├── src/                      # Agent implementations
│   ├── data/                     # Sample log files
│   └── docs/                     # Documentation
├── 05-document-intelligence/     # Form recognition and OCR
├── 06-generative-ai/            # Generative AI applications
├── 07-infrastructure/           # Azure Bicep templates
├── docs/                        # General documentation
├── scripts/                     # Utility scripts
└── templates/                   # Project templates
```

## Module Naming Convention
- Modules are numbered based on their sequence in the learning path
- Some numbers appear multiple times (e.g., 04, 05) representing different tracks
- Each module contains relevant labs and implementations

## Standard Module Structure
Each completed module typically contains:
- `README.md` - Module overview and instructions
- `src/` - Source code implementations
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template
- `data/` - Sample data or test files
- `docs/` - Additional documentation

## Key Files
- `LEARNING_PROGRESS.md` - Tracks completion status (50% complete)
- `README.md` - Repository overview
- `.gitignore` - Excludes sensitive files and build artifacts

## Completed Modules (12/24)
1. Custom Entity Extraction
2. Translate Text
3. Bicep Infrastructure (multiple labs)
4. Speech Service
5. Speech Translation
6. Bicep Conditions and Loops
7. Bicep Modules
8. Semantic Kernel - AI Agents
9. Agent Orchestration

## Environment Setup
Each module includes `.env.example` files showing required configuration. Copy to `.env` and add your Azure credentials.

## Dependencies
- Python 3.8+
- Azure SDK libraries
- Module-specific requirements in `requirements.txt`

## Best Practices
- Never commit `.env` files or credentials
- Use virtual environments for Python modules
- Follow the existing module structure for new implementations
- Document key learnings in module READMEs